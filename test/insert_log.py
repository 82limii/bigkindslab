import pymysql
import sys
sys.path.insert(0, '../')
import auth_prop
from custom_log import Logger
import traceback

logger = Logger()

realtime_logger = logger.initLogger()

# log DB에서 불러오기
mysql_auth = auth_prop.mysql

def mysql_con():
    # MySQL Connection 연결
    con = pymysql.connect(host=mysql_auth['host'], user=mysql_auth['user'], password=mysql_auth['passwd']
        ,db=mysql_auth['db'], charset=mysql_auth['charset'])

    # Connection 으로부터 Cursor 생성
    cur = con.cursor()

    return con, cur


def insert_prov(con, cur, prov_cd):
    sql_1 = """
        SELECT COUNT(1)
        FROM ABKL_PROVIDER_CD
        WHERE PROVIDER_CD = %s
    """
    cur.execute(sql_1, (prov_cd))
    rows = cur.fetchall()
    prov_cnt = rows[0][0]

    if prov_cnt == 0:
        sql_2 = """
        INSERT INTO ABKL_PROVIDER_CD
        (PROVIDER_CD)
        VALUES(%s)
        """

        cur.execute(sql_2, (prov_cd))
        con.commit()

def success_log(news_id, wrk_div, index_nm, st_dtm, end_dtm):
    try:
        con, cur = mysql_con()
        prov_cd = news_id.split(".")[0]
        path = news_id.split(".")[1][:8]

        insert_prov(con, cur, prov_cd)

        sql_1 = """
            INSERT INTO ABKL_NEWSML_SUCCESS
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """
        sql_2 = """
            INSERT INTO ABKL_BIGKINDSLAB_NEWS 
            VALUES (%s, %s)
        """

        cur.execute(sql_1, (news_id, prov_cd, path, wrk_div, index_nm, st_dtm, end_dtm))
        cur.execute(sql_2, (news_id, str(end_dtm).replace("-","")[:8]))
        con.commit()
        con.close

    except Exception as e:
        trace_back = traceback.format_exc()
        message = str(e)+ "\n" + str(trace_back)
        realtime_logger.error('[FAIL] %s', message)

def error_log(news_id, st_dtm, err_cd, err_cnts):
    try:
        con, cur = mysql_con()
        prov_cd = news_id.split(".")[0]
        path = news_id.split(".")[1][:8]

        insert_prov(con, cur, prov_cd)

        sql = """
            INSERT INTO ABKL_NEWSML_ERROR
            VALUES (%s,%s,%s,%s,%s,%s)
        """

        cur.execute(sql, (news_id, prov_cd, path, st_dtm, err_cd, err_cnts))
        con.commit()
        con.close

    except Exception as e:
        trace_back = traceback.format_exc()
        message = str(e)+ "\n" + str(trace_back)
        realtime_logger.error('[FAIL] %s', message)