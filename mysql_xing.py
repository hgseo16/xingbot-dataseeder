import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

AUTHENTICATION_PASSWORD = os.environ.get('AUTHENTICATION_PASSWORD')

# conn = pymysql.connect(host='127.0.0.1', user='root', password=AUTHENTICATION_PASSWORD, db='world', charset='utf8')
#
# try:
#     curs = conn.cursor()
#     sql = 'SELECT * FROM city'
#     curs.execute(sql)
#     rs = curs.fetchall()
#     for row in rs:
#         print(row)
# finally:
#     conn.close()

conn = pymysql.connect(host='127.0.0.1', user='root', password=AUTHENTICATION_PASSWORD, charset='utf8')

try:
    curs = conn.cursor()
    curs.execute('DROP DATABASE IF EXISTS 틱봉')
    curs.execute('CREATE DATABASE 틱봉')
    conn.select_db('틱봉')
    curs.execute('CREATE TABLE 삼성전자'
                 '(ID INT NOT NULL PRIMARY KEY,'
                 '날짜 INT NULL,'
                 '시간 INT NULL,'
                 '시가 INT NULL,'
                 '고가 INT NULL,'
                 '저가 INT NULL,'
                 '종가 INT NULL,'
                 '5평선 INT NULL,'
                 '10평선 INT NULL,'
                 '20평선 INT NULL,'
                 '60평선 INT NULL,'
                 '120평선 INT NULL,'
                 '거래량 INT NULL,'
                 '5평선거래량 INT NULL,'
                 '20평선거래량 INT NULL,'
                 '60평선거래량 INT NULL,'
                 '1200평선거래량 INT NULL)')

finally:
    conn.close()
