import time, sys
sys.path.insert(0, '../')
from custom_log import Logger
import auth_prop
import pymysql
from elasticsearch import Elasticsearch
import traceback

class NewsIdDBBatch:
    def __init__(self, logger):
        # time check
        self.start_time = time.time()

        # 로거 호출
        self.logger = logger

        # MySQL Connection 연결
        mysql_auth = auth_prop.mysql
        self.con = pymysql.connect(host=mysql_auth['host'], user=mysql_auth['user'], password=mysql_auth['passwd']
                              , db=mysql_auth['db'], charset=mysql_auth['charset'], port=mysql_auth['port'])

        # Connection 으로부터 Cursor 생성
        self.cur = self.con.cursor()

        # NEWS_MST insert 쿼리 => 해당 pk 있을 경우 ignore
        self.sql = "INSERT IGNORE INTO ABKL_NEWS_MST(NEWSITEMID, NEWS_CNTS, PUBLISH_DT, PROVIDER_CD) VALUES(%s,%s,%s,%s)"

        self.doc_count = 0
        self.total_count = 0

    def insert_db(self, type, range, sort):
        # elasticsearch 연결
        # 실제서버
        # host = auth_prop.es
        # 로컬
        host = 'http://localhost:9199'
        es = Elasticsearch(host, timeout=30, max_retries=10, retry_on_timeout=True)

        # 검색 요청 조건
        index = "kpf_bigkindslab_*"
        body = {}

        if sort == 0:
            body = {
                "size":1000,
                "track_total_hits":"true",
                "sort":[{"@timestamp":{"order":"asc"}}],
                "_source":["content", "providerCd", "newsItemId", "date", "@timestamp"],
                "query":{
                    "bool":{
                        "must":[
                            {"range":range},
                            {"query_string": {
                                "default_field": "providerCd",
                                "query": "*01100101* *01100201* *01100301* *01100401* *01100501* *01100611* *01100701* *01100801* *01100901* *01101001* *01101101* *01200101* *01200201* *01300101* *01300201* *01400201* *01400351* *01400401* *01400501* *01400551* *01400601* *01400701* *01500051* *01500151* *01500301* *01500401* *01500501* *01500601* *01500701* *01500801* *01500901* *01600201* *01600301* *01600501* *01600801* *01601001* *01601101* *01700101* *01700201* *02100101* *02100201* *02100311* *02100501* *02100601* *02100701* *02100801* *02100851* *07100501* *07101201* *08100101* *08100201* *08100301* *08100401* *08200101*"
                              }}
                        ]
                    }
                }
            }
        else:
            body = {
                "size": 1000,
                "track_total_hits": "true",
                "sort": [{"@timestamp": {"order": "asc"}}],
                "_source": ["content", "providerCd", "newsItemId", "date", "@timestamp"],
                "query": {
                    "bool": {
                        "must": [
                            {"range": range},
                            {"query_string": {
                                "default_field": "providerCd",
                                "query": "*01100101* *01100201* *01100301* *01100401* *01100501* *01100611* *01100701* *01100801* *01100901* *01101001* *01101101* *01200101* *01200201* *01300101* *01300201* *01400201* *01400351* *01400401* *01400501* *01400551* *01400601* *01400701* *01500051* *01500151* *01500301* *01500401* *01500501* *01500601* *01500701* *01500801* *01500901* *01600201* *01600301* *01600501* *01600801* *01601001* *01601101* *01700101* *01700201* *02100101* *02100201* *02100311* *02100501* *02100601* *02100701* *02100801* *02100851* *07100501* *07101201* *08100101* *08100201* *08100301* *08100401* *08200101*"
                            }}
                        ]
                    }
                },
                "search_after":[sort]
            }

        try:
            # 검색 결과
            logger.info(body)
            resp = es.search(index=index, body=body)

            # 검색 결과 건수
            self.total_count = resp['hits']['total']['value']

            for doc in resp['hits']['hits']:
                # newsdb_logger.info(doc['_source']['newsItemId'])
                self.cur.execute(self.sql, (doc['_source']['newsItemId'], doc['_source']['content'], doc['_source']['date'],
                                  doc['_source']['providerCd']))
                self.con.commit()
                sort = doc['sort'][0]
                self.doc_count += 1
                logger.info("newsItemId : " + str(doc['_source']['newsItemId']))
            # SCROLL API를 통해 나온 결과 저장
            while len(resp['hits']['hits']):
                # search_after 추가한 검색 결과
                body = {
                    "size": 1000,
                    "track_total_hits": "true",
                    "sort": [{"@timestamp": {"order": "asc"}}],
                    "_source": ["content", "providerCd", "newsItemId", "date", "@timestamp"],
                    "query": {
                        "bool": {
                            "must": [
                                {"range": range},
                                {"query_string": {
                                    "default_field": "providerCd",
                                    "query": "*01100101* *01100201* *01100301* *01100401* *01100501* *01100611* *01100701* *01100801* *01100901* *01101001* *01101101* *01200101* *01200201* *01300101* *01300201* *01400201* *01400351* *01400401* *01400501* *01400551* *01400601* *01400701* *01500051* *01500151* *01500301* *01500401* *01500501* *01500601* *01500701* *01500801* *01500901* *01600201* *01600301* *01600501* *01600801* *01601001* *01601101* *01700101* *01700201* *02100101* *02100201* *02100311* *02100501* *02100601* *02100701* *02100801* *02100851* *07100501* *07101201* *08100101* *08100201* *08100301* *08100401* *08200101*"
                                }}
                            ]
                        }
                    },
                    "search_after": [sort]
                }

                # 검색 결과
                resp = es.search(index=index, body=body)

                for doc in resp['hits']['hits']:
                    # newsdb_logger.info(doc['_source']['newsItemId'])
                    self.cur.execute(self.sql, (doc['_source']['newsItemId'], doc['_source']['content'], doc['_source']['date'],
                                      doc['_source']['providerCd']))
                    self.con.commit()
                    sort = doc['sort'][0]
                    self.doc_count += 1
                    logger.info("newsItemId : "+str(doc['_source']['newsItemId']))

        except Exception as e:  # 에러 처리
            trace_back = traceback.format_exc()
            message = str(e) + "\n" + str(trace_back)
            self.logger.error('[FAIL] %s', message)
            self.logger.debug("sort : %s", str(sort))
        finally:
            self.cur.close()
            self.con.close()
            self.logger.debug("total_count : %s", str(self.total_count))
            self.logger.debug("doc_count : %s", str(self.doc_count))
            self.logger.debug("TOTAL TIME : %s seconds.", str(time.time() - self.start_time))

if __name__ == '__main__':
    try:
        # 로거 호출
        logger = Logger().initLogger()
        # 객체 생성
        cls = NewsIdDBBatch(logger)
        print(sys.argv)
        if len(sys.argv) == 1:
            logger.error("옵션값을 입력하세요.")
            exit()

        # 옵션값 batch, sort_omi, date_insert
        sys_param = sys.argv[1]
        logger.info("실행옵션 : "+str(sys.argv))
        if sys_param == 'batch':
            range = {
                "@timestamp": {
                    "gte": "now-2d/d",
                    "lte": "now-1d/d"
                }
            }
            cls.insert_db(sys_param, range, 0)
        elif sys_param == 'sort_omi':
            if len(sys.argv) == 2:
                logger.error("날짜 옵션값을 입력하세요. ex) 2021-01-04~2021-04-05")
                exit()
            elif len(sys.argv) == 3:
                logger.error("이어서 진행할 sort값을 입력하세요.")
                exit()
            else:
                # 날짜형식 2023-01-01~2023-01-04 형식으로 입력해야 함
                dt = sys.argv[2]
                start_dt = dt.split("~")[0]
                end_dt = dt.split("~")[1]

                range = {
                    "@timestamp": {
                        "gte": start_dt,
                        "lte": end_dt
                    }
                }
                sort = sys.argv[3]
                cls.insert_db(sys_param, range, int(sort))
        elif sys_param == 'date_insert':
            print(len(sys.argv))
            if len(sys.argv) != 3:
                logger.error("날짜 옵션값을 입력하세요. ex) 2021-01-04~2021-04-05")
                exit()
            else:
                # 날짜형식 2023-01-01~2023-01-04 형식으로 입력해야 함
                dt = sys.argv[2]
                start_dt = dt.split("~")[0]
                end_dt = dt.split("~")[1]

                range = {
                    "@timestamp": {
                        "gte": start_dt,
                        "lte": end_dt
                    }
                }
                cls.insert_db(sys_param, range, 0)
        else:
            logger.error("옵션값을 입력하세요.")
            exit()

    except Exception as e:  # 에러 처리
        trace_back = traceback.format_exc()
        message = str(e) + "\n" + str(trace_back)
        logger.error('[FAIL] %s', message)