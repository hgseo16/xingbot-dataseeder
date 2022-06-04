import time as timefnc
import datetime
import pythoncom as pcom
import pymysql
import os
from dotenv import load_dotenv

class Backtest_Engine:

    def __init__(self):
        print('Backtest_Engine Running...')
        self.initial_capital = 10000
        self.buy_commission = 0.0
        self.sell_commission = 0.0
        self.start_date = None
        self.end_date = datetime.datetime.now()

        load_dotenv()

        AUTHENTICATION_PASSWORD = os.environ.get('AUTHENTICATION_PASSWORD')

        conn = pymysql.connect(host='127.0.0.1', user='root', password=AUTHENTICATION_PASSWORD, db='spy_500', charset='utf8')

        try:
            curs = conn.cursor()
            query_text = 'SELECT * FROM spy_500_daily'
            curs.execute(query_text)
            self.rs = curs.fetchall()

        finally:
            conn.close()

        self.Strategy()

    def get_SMA(self, SMA_list):
        size = len(SMA_list)
        return sum(SMA_list) / size


    def Strategy(self):
        SMA_5_list = []
        SMA_10_list = []
        SMA_20_list = []
        SMA_5 = None
        SMA_10 = None
        SMA_20 = None

        for row in self.rs:
            SMA_5_list.append()
            SMA_10_list.append()
            SMA_20_list.append()
            print(row)
        print(len(self.rs))