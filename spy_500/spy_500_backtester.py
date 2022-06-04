import time as timefnc
import datetime
import pymysql
import os
from dotenv import load_dotenv

class Backtest_Engine:

    def __init__(self):
        print('Backtest_Engine Running...')
        self.initial_capital = 10000
        self.available_capital = 10000
        self.end_capital = self.initial_capital
        self.buy_commission = 0.0
        self.sell_commission = 0.0
        # Unused for now
        # self.start_date = None
        # self.end_date = datetime.datetime.now()

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


    def get_SMA(self, SMA_list, size):
        i = len(SMA_list)
        window = SMA_list[i-size:]

        return sum(window) / size


    def Strategy(self):
        start = False
        SMA_3_list = []
        SMA_5_list = []
        SMA_10_list = []
        SMA_20_list = []
        SMA_3 = None
        SMA_5 = None
        SMA_10 = None
        SMA_20 = None

        for row in self.rs:
            curr_price = row[5]
            # row(5) is the closing price (가격)
            SMA_3_list.append(row[5])
            SMA_5_list.append(row[5])
            SMA_10_list.append(row[5])
            SMA_20_list.append(row[5])

            # Maintains list size according to SMA
            if len(SMA_3_list) > 3:
                del SMA_3_list[0]
            if len(SMA_5_list) > 5:
                del SMA_5_list[0]
            if len(SMA_10_list) > 10:
                del SMA_10_list[0]
            if len(SMA_20_list) > 20:
                del SMA_20_list[0]

            # Calculate SMAs
            if len(SMA_3_list) == 3:
                SMA_3 = self.get_SMA(SMA_20_list, 3)
            if len(SMA_5_list) == 5:
                SMA_5 = self.get_SMA(SMA_20_list, 5)
            if len(SMA_10_list) == 10:
                SMA_10 = self.get_SMA(SMA_20_list, 10)
            if len(SMA_20_list) == 20:
                SMA_20 = self.get_SMA(SMA_20_list, 20)

            # Buy Condition
            # if (curr_price > SMA_3) or (curr_price > SMA_5) or (curr_price > SMA_10):
            #     self.initial_capital

            # Buy and Hold
        if start is False:
            start = True
            num_stocks_bought = int(self.initial_capital / row[5])

            print(num_stocks_bought)
