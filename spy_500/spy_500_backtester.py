import time as timefnc
import datetime
import pythoncom as pcom
import pymysql
import os
from dotenv import load_dotenv

class Backtest_Engine:

    def __init__(self):
        print('Backtest_Engine Running...')
        initial_capital = 10000
        buy_commission = 0.0
        sell_commission = 0.0
        start_date = None
        end_date = datetime.datetime.now()

        load_dotenv()

        AUTHENTICATION_PASSWORD = os.environ.get('AUTHENTICATION_PASSWORD')

        conn = pymysql.connect(host='127.0.0.1', user='root', password=AUTHENTICATION_PASSWORD, db='spy_500', charset='utf8')

        try:
            curs = conn.cursor()
            query_text = 'SELECT * FROM spy_500_daily'
            curs.execute(query_text)
            rs = curs.fetchall()
            for row in rs:
                print(row)
            print(len(rs))

        finally:
            conn.close()
        # conn.commit()
