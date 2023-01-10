import time, sys
sys.path.insert(0, '../')
import auth_prop
from custom_log import Logger
import pymysql
from datetime import datetime, timedelta
from python_api.keyword_module import keyword_ext
import traceback

class KeywordExt:
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

    def insert_keyword(self, date):
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
                self.total_count = len(rows)
                self.logger.info("SELECT DONE TIME : " + str(time.time() - self.start_time))

                # keyword insert SQL문
                insert_sql = "INSERT IGNORE INTO ABKL_NEWS_KEYWORD_RESULT(NEWSITEMID, KEYWORD_SEQ, KEYWORD) VALUES(%s,%s,%s)"

                for row in rows:
                    # 기사 본문 전처리
                    text = row[1].replace("<![CDATA[", "").replace("]]>", "")
                    # 키워드 추출
                    res = keyword_ext(text)
                    for idx, keyword in enumerate(res):
                        # 키워드와 순번 DB insert
                        self.cur.execute(insert_sql, (row[0], str(idx + 1), keyword))
                    self.con.commit()
                    self.insert_count += 1
                    self.logger.info("newsItemId : "+str(row[0]))

        except Exception as e:  # 에러 처리
            trace_back = traceback.format_exc()
            message = str(e) + "\n" + str(trace_back)
            self.logger.error('[FAIL] %s', message)
        finally:
            self.cur.close()
            self.con.close()
            self.logger.debug("total_count : %s", str(self.total_count))
            self.logger.debug("insert_count : %s", str(self.insert_count))
            self.logger.debug("TOTAL TIME : %s seconds.", str(time.time() - self.start_time))

if __name__ == '__main__':
    try:
        # 로거 호출
        logger = Logger("./keyword_log/").initLogger()
        #객체 생성
        cls = KeywordExt(logger)

        # 옵션 입력하지 않을 경우 종료
        if len(sys.argv) <= 1:
            logger.error("옵션값을 입력하세요.")
            exit()

        # 옵션값 batch, date_insert
        sys_param = sys.argv[1]
        logger.info("실행옵션 : " + str(sys.argv))

        if sys_param == "batch":
            cls.insert_keyword(str(datetime.today() - timedelta(1))[:10])
        elif sys_param == "date_insert":
            # 날짜 입력값 필요, 날짜 형식 2023-01-01으로 입력 필요
            if len(sys.argv) == 2:
                logger.error("날짜를옵션 값을 입력하세요. ex)2023-01-10")
                exit()

            cls.insert_keyword(sys.argv[2])
        # 실행 옵션 이상할 경우
        else:
            logger.error("옵션값을 입력하세요.")
            exit()

    except Exception as e:  # 에러 처리
        trace_back = traceback.format_exc()
        message = str(e) + "\n" + str(trace_back)
        logger.error('[FAIL] %s', message)