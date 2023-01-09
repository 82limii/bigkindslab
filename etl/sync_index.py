import pymysql
from datetime import datetime as dt
import sys
sys.path.insert(0, '../')
import auth_prop
from es_module import insert_doc, delete_doc
from db_log_module import ins_suc_log, del_suc_log, err_log

st_dtm = dt.now()

mysql_auth = auth_prop.mysql

# log DB에서 불러오기
# MySQL Connection 연결
con = pymysql.connect(host=mysql_auth['host'], user=mysql_auth['user'], password=mysql_auth['passwd']
                      , db=mysql_auth['db'], charset=mysql_auth['charset'], port=mysql_auth['port'])

# Connection 으로부터 Cursor 생성
cur = con.cursor()

# 동기화 위해 bigkinds에 추가되었지만 bigkindslab에 추가되지 않은 newsitemid 불러오기 (전날 기준)
sql_1 = """
    SELECT abin.NEWSITEMID
    FROM (SELECT NEWSITEMID FROM ABKL_BIGKINDS_INSERT_NEWS WHERE UPDATE_DT = DATE_FORMAT(DATE_ADD(NOW(), INTERVAL -1 day), '%Y%m%d')) abin
        LEFT JOIN (SELECT NEWSITEMID FROM ABKL_BIGKINDSLAB_NEWS  WHERE UPDATE_DT = DATE_FORMAT(DATE_ADD(NOW(), INTERVAL -1 day), '%Y%m%d')) abn ON abin.NEWSITEMID = abn.NEWSITEMID
    WHERE abn.NEWSITEMID IS NULL
"""

cur.execute(sql_1)
rows = cur.fetchall()

ins_id_arr = []
for row in rows:
    ins_id_arr.append(row[0])

# 동기화 위해 bigkinds에 삭제되었지만 bigkindslab에 남아있는 newsitemid 불러오기 (전날 기준)
sql_2 = """
    SELECT abdn.NEWSITEMID
    FROM (SELECT NEWSITEMID FROM ABKL_BIGKINDS_DELETE_NEWS WHERE UPDATE_DT = DATE_FORMAT(DATE_ADD(NOW(), INTERVAL -1 day), '%Y%m%d')) abdn
        LEFT JOIN (SELECT NEWSITEMID FROM ABKL_BIGKINDSLAB_NEWS  WHERE UPDATE_DT = DATE_FORMAT(DATE_ADD(NOW(), INTERVAL -1 day), '%Y%m%d')) abn ON abdn.NEWSITEMID = abn.NEWSITEMID
    WHERE abn.NEWSITEMID IS NOT NULL
"""

cur.execute(sql_2)
rows = cur.fetchall()

del_id_arr = []
for row in rows:
    del_id_arr.append(row[0])

con.close()

# es에 insert해야할 newsitemid 사용하여 xml insert
for ins_id in ins_id_arr:
    ins_id_arr = ins_id.split('.')
    xml_path = '/hadoop/newsml/data/'+ins_id_arr[0]+'/'+ins_id_arr[1][:4]+'/'+ins_id_arr[1][4:6]+'/'+ins_id_arr[1][6:8]+'/'+ins_id+'.xml'
    news_id, index = insert_doc(xml_path)
    end_dtm = dt.now()
    ins_suc_log(news_id, '1', index, st_dtm, end_dtm)

# es에 delete해야할 newsitemid 사용하여 doc delete
for del_id in del_id_arr:
    res, index = delete_doc(del_id)
    end_dtm = dt.now()
    del_suc_log(del_id, '1', index, st_dtm, end_dtm)


