import pymysql
import xlrd
import os
from dotenv import load_dotenv

load_dotenv()

AUTHENTICATION_PASSWORD = os.environ.get('AUTHENTICATION_PASSWORD')

sql_set_table_daily_data = '''
CREATE TABLE SPY_500_daily
                 (ID INT NOT NULL PRIMARY KEY,
                 날짜 VARCHAR(30) NULL,
                 시간 VARCHAR(30) NULL,
                 시가 FLOAT NULL,
                 고가 FLOAT NULL,
                 저가 FLOAT NULL,
                 가격 FLOAT NULL,
                 전일대비구분 FLOAT NULL,
                 전일대비 FLOAT NULL,
                 등락률 FLOAT NULL,
                 누적거래량 FLOAT NULL,
                 한국일자 VARCHAR(30) NULL,
                 한국시간 VARCHAR(30) NULL)
'''

conn = pymysql.connect(host='127.0.0.1', user='root', password=AUTHENTICATION_PASSWORD, charset='utf8')
# workboo = xlrd.open_workbook('삼성전자.xls', encoding_override='cp949')

try:
    curs = conn.cursor()
    curs.execute('DROP DATABASE IF EXISTS SPY_500')
    curs.execute('CREATE DATABASE SPY_500')
    conn.select_db('SPY_500')
    curs.execute(sql_set_table_daily_data)

finally:
    conn.close()
