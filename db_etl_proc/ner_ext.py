import time, sys
sys.path.insert(0, '../')
import auth_prop
from custom_log import Logger
import pymysql
from datetime import datetime, timedelta
from python_api.ner4_module import ner_predict
import traceback

class NerExt:
    def __init__(self, logger):
        # time check
        self.start_time = time.time()

        # 로거 호출
        self.logger = logger
        self.logger.debug("start time : %s", str(datetime.today()))

        # MySQL Connection 연결
        mysql_auth = auth_prop.mysql
        self.con = pymysql.connect(host=mysql_auth['host'], user=mysql_auth['user'], password=mysql_auth['passwd']
                                   , db=mysql_auth['db'], charset=mysql_auth['charset'], port=mysql_auth['port'])

        # Connection 으로부터 Cursor 생성
        self.cur = self.con.cursor()

        self.total_count = 0
        self.insert_count = 0
        self.cur_page = 0
        self.newsItemId = ""

    def insert_ner(self, date, start_page=None):
        try:
            page_size = 1000  # 페이지당 데이터 수
            # 전체 데이터 수 구하기 위한 SQL문
            count_sql = """SELECT COUNT(1)
                FROM ABKL_NEWS_MST anm
                WHERE DATE_FORMAT(REGIST_DT, '%%Y-%%m-%%d') = DATE_FORMAT(%s, '%%Y-%%m-%%d')
                    AND NEWS_CNTS != '%%{[contents][0]}'
            """
            self.cur.execute(count_sql, date)
            self.total_count = self.cur.fetchall()[0][0] # 전체 데이터 수
            total_page = round(self.total_count / page_size) # 전체 페이지 수

            for page in range(total_page):
                self.cur_page = page
                self.logger.info("cur_page : "+str(self.cur_page))
                if start_page is not None:
                    if page < int(start_page):
                        continue
                # 데이터 불러오기 위한 SQL문 (페이징처리)
                select_sql = """SELECT NEWSITEMID , NEWS_CNTS
                    FROM ABKL_NEWS_MST anm
                    WHERE DATE_FORMAT(REGIST_DT, '%%Y-%%m-%%d') = DATE_FORMAT(%s, '%%Y-%%m-%%d')
                        AND NEWS_CNTS != '%%{[contents][0]}'
                    ORDER BY REGIST_DT
                    LIMIT %s
                    OFFSET %s
                """
                self.cur.execute(select_sql, (date, page_size, page * page_size))

                # 데이타 Fetch
                rows = self.cur.fetchall()
                self.logger.info("SELECT DONE TIME : " + str(time.time() - self.start_time))

                # keyword insert SQL문
                insert_sql = "INSERT IGNORE INTO ABKL_NEWS_NER_RESULT(NEWSITEMID, NER_SEQ, NER_CD, EXT_WORD) VALUES(%s,%s,%s,%s)"

                for row in rows:
                    self.newsItemId = row[0]
                    # 기사 본문 전처리
                    text = row[1].replace("<![CDATA[","").replace("]]>","").replace("&apos;","\'").replace("&quot;","\"")
                    # 개체명 추출
                    res = ner_predict(text)
                    params = []
                    for idx, ner in enumerate(res):
                        # 키워드와 순번 DB insert
                        self.cur.execute(insert_sql, (row[0], str(idx + 1), ner['label'], ner['word']))
                    self.con.commit()
                    self.insert_count += 1
                    self.logger.info("newsItemId : "+self.newsItemId)

        except Exception as e:  # 에러 처리
            trace_back = traceback.format_exc()
            message = str(e) + "\n" + str(trace_back)
            self.logger.error('[FAIL] %s', message)
            self.logger.error("error page : "+str(self.cur_page))
            self.logger.error("error newsItemId : " + self.newsItemId)
        finally:
            self.cur.close()
            self.con.close()
            self.logger.debug("total_count : %s", str(self.total_count))
            self.logger.debug("insert_count : %s", str(self.insert_count))
            self.logger.debug("TOTAL TIME : %s seconds.", str(time.time() - self.start_time))

if __name__ == '__main__':
    try:
        # 로거 호출
        logger = Logger("./ner_log/").initLogger()
        #객체 생성
        cls = NerExt(logger)

        # 옵션 입력하지 않을 경우 종료
        if len(sys.argv) <= 1:
            logger.error("옵션값을 입력하세요.")
            exit()

        # 옵션값 batch, date_insert
        sys_param = sys.argv[1]
        logger.info("실행옵션 : " + str(sys.argv))

        if sys_param == "batch":
            logger.info("batch 실행 날짜 : " + str(datetime.today() - timedelta(1))[:10])
            cls.insert_ner(str(datetime.today() - timedelta(1))[:10])
        elif sys_param == "date_insert":
            # 날짜 입력값 필요, 날짜 형식 2023-01-01으로 입력 필요
            if len(sys.argv) == 2:
                logger.error("날짜를옵션 값을 입력하세요. ex)2023-01-10")
                exit()

            cls.insert_ner(sys.argv[2])
        elif sys_param == "page_setting":
            # 날짜 입력값 필요, 날짜 형식 2023-01-01으로 입력 필요
            if len(sys.argv) == 2:
                logger.error("날짜를옵션 값을 입력하세요. ex)2023-01-10")
                exit()
            elif len(sys.argv) == 3:
                logger.error("페이지를 입력하세요.")
                exit()

            cls.insert_ner(sys.argv[2], sys.argv[3])
        # 실행 옵션 이상할 경우
        else:
            logger.error("옵션값을 입력하세요.")
            exit()

    except Exception as e:  # 에러 처리
        trace_back = traceback.format_exc()
        message = str(e) + "\n" + str(trace_back)
        logger.error('[FAIL] %s', message)