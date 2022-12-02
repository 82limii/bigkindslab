import pymysql
from elasticsearch import Elasticsearch
import traceback
import logging
import sys
sys.path.insert(0, '../')
import auth_prop

# 로거 생성
logger = logging.getLogger("insert_log")

# 레벨 설정 - 'INFO' 레벨부터 출력
logger.setLevel(logging.INFO)

# 출력 포매팅 설정 - 시간, 로거이름, 로깅레벨, 메세지
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# 스트림 핸들러 설정 - 콘솔에 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# 파일 핸들러 설정 - 파일에 출력
file_handler = logging.FileHandler('../insert.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
row = 0

mysql_auth = auth_prop.mysql

try:
    # MySQL Connection 연결
    con = pymysql.connect(host=mysql_auth['host'], user=mysql_auth['user'], password=mysql_auth['passwd']
        ,db=mysql_auth['db'], charset=mysql_auth['charset'])

    # Connection 으로부터 Cursor 생성
    cur = con.cursor()

    # SQL문 실행 및 Fetch
    sql = """SELECT NEWSITEMID 
    FROM ABKL_NEWS_SUBJ_REFINE_1 ansr"""
    cur.execute(sql)

    # 데이타 Fetch
    rows = cur.fetchall()
    # 분류된 newsid 배열
    id_arr = []
    for id in rows:
        id_arr.append(id[0])

    print(len(id_arr))

    # news_conts 담을 배열
    conts_arr = []

    # ES 연결
    es = Elasticsearch('http://localhost:9199')

    # 조회할 es 정보
    for idx, id in enumerate(id_arr):
        # err_001
        if len(id) != 26:
            continue
        try:
            if idx!=0 and idx%100==0:
                print(idx)
                # DB에 학습데이터 insert
                for i,conts in enumerate(conts_arr):
                    sql = """INSERT INTO ABKL_NEWS_SUBJ_LEARN_DATA 
                        (NEWSITEMID, NEWS_CNTS, NEWS_BIG_SUBJ_CD, NEWS_SML_SUBJ_CD, NEWS_BIG_SUBJ_NM, NEWS_SML_SUBJ_NM)
                        SELECT ansr.NEWSITEMID , %s AS NEWS_CNTS, ansr.NEWS_BIG_SUBJ_CD , ansr.NEWS_SML_SUBJ_CD , ansc.NEWS_BIG_SUBJ_NM , ansc.NEWS_SML_SUBJ_NM 
                        FROM ABKL_NEWS_SUBJ_REFINE_1 ansr 
                            LEFT OUTER JOIN ABKL_NEWS_SUBJ_CD ansc ON ansr.NEWS_SML_SUBJ_CD = ansc.NEWS_SML_SUBJ_CD 
                        WHERE NEWSITEMID = %s
                        """
                    cur.execute(sql, (conts, id_arr[idx-100+i]))
                    con.commit()
                    conts_arr = []
            
            year = id.split(".")[1][:4]
            index = 'kpf_bigkindslab_v1.1_'+year
            body = {
                "_source": ["NewsItem.NewsComponent.NewsComponent.ContentItem.DataContent"],
                "query": {
                    "match": {
                        "_id": id
                    }
                }
            }

            res = es.search(index=index, body=body)
            # err_002
            if len(res['hits']['hits']) == 0:
                continue
            conts = res['hits']['hits'][0]['_source']['NewsItem']['NewsComponent']['NewsComponent'][0]['ContentItem']['DataContent'].replace("&quot;","\"").replace("&apos;","'")
            conts_arr.append(conts)
        finally:
            row = idx

except Exception as e:
    trace_back = traceback.format_exc()
    message = str(e)+ "\n" + str(trace_back) + "\n row = " + str(row)
    logger.error('[FAIL] %s', message)

finally:
    # DB connection 종료
    con.close