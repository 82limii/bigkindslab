# 실행 시간 기준 00:05
# 날짜 검색 기준 전날 00:00 ~ 24:00
from datetime import date, timedelta
import glob
import pymysql
from elasticsearch import Elasticsearch
from newsml_to_json import make_json
import sys
sys.path.insert(0, '../')
import auth_prop


today = date.today()
yesterday = date.today() - timedelta(1)

# es에 추가하는 def
es = Elasticsearch('http://localhost:9199')

mapping = {
    "settings" : {
        "number_of_shards": 6,
        "number_of_replicas": 1
    }
}

def add_doc(xml_path):
    # xml -> json 변환
    json_dict = make_json(xml_path)
    print(json_dict)
    index = "kpf_bigkindslab_v1.1_" + json_dict['NewsEnvelope']['DateAndTime'][:4]
    news_id = json_dict['NewsItem']['Identification']['NewsIdentifier']['NewsItemId']
    print(news_id)
    # index가 존재하는 지 확인
    # index 없을 경우 index 생성 후 doc 추가
    if es.indices.exists(index=index)==False:
        es.indices.create(index=index, body=mapping)

    result = es.index(index=index, doc_type="_doc", body=json_dict, id='test') 

# add_doc('../data/01100201.20211111000455001.xml')

# 모든 파일 scan 하여 file_data_arr에 담아두기 dict형태
file_arr = glob.glob('../data/newsml/*/*/*/*/*.xml')
file_dict_list = []
for file in file_arr :
    file_dict = dict()
    file_dict['xml_path'] = file
    file_dict['NewsItemId'] = file.split('/')[5].replace(".xml","")
    file_dict_list.append(file_dict)

print(len(file_dict_list))

# log DB에서 불러오기
mysql_auth = auth_prop.mysql
# MySQL Connection 연결
con = pymysql.connect(host=mysql_auth['host'], user=mysql_auth['user'], password=mysql_auth['passwd']
    ,db=mysql_auth['db'], charset=mysql_auth['charset'])

# Connection 으로부터 Cursor 생성
cur = con.cursor()

# SQL문 실행 및 Fetch
sql = """
    SELECT NEWSITEMID
    FROM tb_batch_log 
    WHERE date(batch_date) BETWEEN %s AND %s
        AND status_cd = 'FAIL'
"""
cur.execute(sql, (str(yesterday), str(yesterday)))

# 데이타 Fetch
rows = cur.fetchall()

# 전날의 es insert 실패 아이디 목록
fail_id_list = []

for row in rows:
    fail_id_list.append(row[0])


# log DB에서 에러 발생한 NewsItemId xml읽고 추가
for fail_id in fail_id_list:
    for file_dict in file_dict_list:
        if fail_id == file_dict['NewsItemId']:
            add_doc(file_dict['xml_path'])


# es에서 불러오기
es = Elasticsearch('http://localhost:9199')
index = 'kpf_bigkindslab_v1.1_'+str(yesterday)[:4]

body = {
    "_source":"_id",
    "query":{
        "range":{
            "@timestamp": {
                "gte": str(yesterday),
                "lte": str(yesterday)
            }
        }
    }
}

es_results = es.search(index="kpf_bigkindslab_v1.1_202111", body=body) # 향후 인덱스명 위에 만든 인덱스로 교체

es_id_list = []

for result in es_results['hits']['hits']:
    es_id_list.append(result['_id'])

# NewsItemId 값 비교 (파일 scan, es)
# 파일 scan에 있지만 es에 등록되지 않은 NewsItemId 찾아 xml 읽어낸 후 es에 추가
for file_dict in file_dict_list:
    flag = True
    for es_id in es_id_list:
        if file_dict['NewsItemId'] == es_id:
            flag = False

    if flag:
        add_doc(file_dict['xml_path'])
