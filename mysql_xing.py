import pymysql
import xlrd
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

# sql_value ='''
# CREATE TABLE 삼성전자
#                  (ID INT NOT NULL PRIMARY KEY,
#                  날짜 VARCHAR(30) NULL,
#                  시간 VARCHAR(30) NULL,
#                  시가 INT NULL,
#                  고가 INT NULL,
#                  저가 INT NULL,
#                  종가 INT NULL,
#                  5평선 FLOAT NULL,
#                  10평선 FLOAT NULL,
#                  20평선 FLOAT NULL,
#                  60평선 FLOAT NULL,
#                  120평선 FLOAT NULL,
#                  거래량 INT NULL,
#                  5평선거래량 FLOAT NULL,
#                  20평선거래량 FLOAT NULL,
#                  60평선거래량 FLOAT NULL,
#                  120평선거래량 FLOAT NULL)
# '''

sql_daily_data ='''
CREATE TABLE 삼성전자
                 (ID INT NOT NULL PRIMARY KEY,
                 날짜 VARCHAR(30) NULL,
                 시가 INT NULL,
                 고가 INT NULL,
                 저가 INT NULL,
                 종가 INT NULL,
                 거래량 INT NULL,
                 거래대금 FLOAT NULL,
                 수정구분 FLOAT NULL,
                 수정비율 FLOAT NULL,
                 수정주가반영항목 FLOAT NULL,
                 수정비율반영거래대금 FLOAT NULL,
                 종가등락구분 VARCHAR(30) NULL)
'''

conn = pymysql.connect(host='127.0.0.1', user='root', password=AUTHENTICATION_PASSWORD, charset='utf8')
# workboo = xlrd.open_workbook('삼성전자.xls', encoding_override='cp949')

try:
    curs = conn.cursor()
    curs.execute('DROP DATABASE IF EXISTS 일봉')
    curs.execute('CREATE DATABASE 일봉')
    conn.select_db('일봉')
    curs.execute(sql_daily_data)

finally:
    conn.close()
