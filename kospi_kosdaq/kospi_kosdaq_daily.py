# Shows daily data of ETFs (ETFs 일별추이)
import time as timefnc
import pythoncom as pcom
import pymysql
import os
from dotenv import load_dotenv

import sys
sys.setrecursionlimit(1500)

class EC_t1903:
    # Used to check tr status
    tr_success = False
    # Used for methods
    t1903_e = None

    # Initialize DB selection or creation in first loop
    first_loop = True

    # store shcode
    shcode = ''

    # daily, weekly, monthly, 1min, 3min, 5min, 60min
    time_frame = ''

    # Checks whether data is seeded
    first_seed = ''

    # KOSPI / KOSDAQ / ETF
    market = ''

    def OnReceiveData(self, code):

        if code == "t1903":
            print('shcode: {}, time_frame: {}, first_seed: {}, market: {}'.format(self.shcode, self.time_frame, self.first_seed, self.market))

            occurs_count = self.GetBlockCount("t1903OutBlock1")
            cts_date = self.GetFieldData("t1903OutBlock", "date", 0)
            # 종목명
            hname = self.GetFieldData("t1903OutBlock", "hname", 0)
            hname = hname.replace(" ", "_")
            # 업종지수명
            upname = self.GetFieldData("t1903OutBlock", "upname", 0)

            print('occurs_count: {}'.format(occurs_count))
            print('cts_date: {}'.format(cts_date))
            print("hname: {}".format(hname))
            print("upname: {}".format(upname))

            if self.first_loop == True:

                initialize_db(self.market, self.time_frame)
                self.first_loop = False

                # Check whether table exists and create table if it doesn't
                check_table(hname, self.market, self.time_frame)

            print('first loop done')

            for i in range(occurs_count):
                inverse_idx = occurs_count - i - 1
                date = self.GetFieldData("t1903OutBlock1", "date", inverse_idx)
                price = self.GetFieldData("t1903OutBlock1", "price", inverse_idx)
                sign = self.GetFieldData("t1903OutBlock1", "sign", inverse_idx)
                change = self.GetFieldData("t1903OutBlock1", "change", inverse_idx)
                volume = self.GetFieldData("t1903OutBlock1", "volume", inverse_idx)
                navdiff = self.GetFieldData("t1903OutBlock1", "navdiff", inverse_idx)
                nav = self.GetFieldData("t1903OutBlock1", "nav", inverse_idx)
                navchange = self.GetFieldData("t1903OutBlock1", "navchange", inverse_idx)
                crate = self.GetFieldData("t1903OutBlock1", "crate", inverse_idx)
                grate = self.GetFieldData("t1903OutBlock1", "grate", inverse_idx)
                jisu = self.GetFieldData("t1903OutBlock1", "jisu", inverse_idx)
                jichange = self.GetFieldData("t1903OutBlock1", "jichange", inverse_idx)
                jirate = self.GetFieldData("t1903OutBlock1", "jirate", inverse_idx)

                # print("date: {}".format(type(date)))
                # print("price: {}".format(type(price)))
                # print("sign: {}".format(type(sign)))
                # print("change: {}".format(type(change)))
                # print("volume: {}".format(type(volume)))
                # print("navdiff: {}".format(type(navdiff)))
                # print("nav: {}".format(type(nav)))
                # print("navchange: {}".format(type(navchange)))
                # print("crate: {}".format(type(crate)))
                # print("grate: {}".format(type(grate)))
                # print("jisu: {}".format(type(jisu)))
                # print("jichange: {}".format(type(jichange)))
                # print("jirate: {}".format(type(jirate)))

                mysql_etf(hname, self.market, self.time_frame, date, price, sign, change, volume, navdiff, nav, navchange, crate, grate, jisu, jichange, jirate)

            if cts_date != "":
                t1903_request(shcode=EC_t1903.shcode, date=cts_date, time_frame=self.time_frame, first_seed=self.first_seed, market=self.market, occurs=self.IsNext)
            else:
                EC_t1903.conn.close()
                EC_t1903.tr_success = True


def t1903_request(shcode=None, date=None, time_frame='', first_seed=False, market='', occurs=False):

    timefnc.sleep(3.1)

    # Pass type of "market"
    EC_t1903.market = market

    # Pass "time_frame" (daily, 1min, 3min, etc) to method
    EC_t1903.time_frame = time_frame

    # Pass whether it's been "seeded"
    EC_t1903.first_seed = first_seed

    # Pass "shcode"
    EC_t1903.shcode = shcode

    EC_t1903.t1903_e.SetFieldData("t1903InBlock", "shcode", 0, shcode)
    EC_t1903.t1903_e.SetFieldData("t1903InBlock", "date", 0, date)

    EC_t1903.t1903_e.Request(occurs)

    EC_t1903.tr_success = False

    while EC_t1903.tr_success == False:
        pcom.PumpWaitingMessages()



def mysql_etf(hname, market, time_frame, date, price, sign, change, volume, navdiff, nav, navchange, crate, grate, jisu, jichange, jirate):

    EC_t1903.conn.select_db('{}_{}'.format(market, time_frame))

    print(hname)

    sql_insert_daily_data = '''
    INSERT INTO {}
    (일자, 현재가, 전일대비구분, 전일대비, 누적거래량, NAV대비, 
    NAV, NAV전일대비, 추적오차, 괴리, 지수, 지수전일대비, 지수전일대비율)
    VALUE
    ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})
    '''.format(hname, str(date), str(price),
               str(sign), str(change), str(volume),
               str(navdiff), str(nav), str(navchange),
               str(crate), str(grate), str(jisu),
               str(jichange), str(jirate))

    print(sql_insert_daily_data)
    EC_t1903.curs.execute(sql_insert_daily_data)
    EC_t1903.conn.commit()


def initialize_db(market, time_frame):

    load_dotenv()

    AUTHENTICATION_PASSWORD = os.environ.get('AUTHENTICATION_PASSWORD')

    EC_t1903.conn = pymysql.connect(host='127.0.0.1', user='root', password=AUTHENTICATION_PASSWORD, charset='utf8')

    EC_t1903.curs = EC_t1903.conn.cursor()

    # For Deleting and Recreating db spy_500
    # curs.execute('DROP DATABASE IF EXISTS KODEX_LEVERAGE')

    # to check if db exists
    EC_t1903.curs.execute("SHOW DATABASES LIKE '{}_{}'".format(market, time_frame))
    db_check = EC_t1903.curs.fetchall()
    print(db_check)

    if db_check == (): # db doesn't exist
        print('db doesn\'t exist')
        EC_t1903.curs.execute("CREATE DATABASE `{}_{}`".format(market, time_frame))
        EC_t1903.conn.select_db("{}_{}".format(market, time_frame))
        # sql_set_table_daily_data = '''
        # CREATE TABLE `{}`
        # (일자 VARCHAR(30) NOT NULL PRIMARY KEY,
        # 현재가 FLOAT NULL,
        # 전일대비구분 FLOAT NULL,
        # 전일대비 FLOAT NULL,
        # 누적거래량 FLOAT NULL,
        # NAV대비 FLOAT NULL,
        # NAV FLOAT NULL,
        # NAV전일대비 FLOAT NULL,
        # 추적오차 FLOAT NULL,
        # 괴리 FLOAT NULL,
        # 지수 FLOAT NULL,
        # 지수전일대비 FLOAT NULL,
        # 지수전일대비율 FLOAT NULL)
        # '''.format(time_frame)

        # EC_t1903.conn.select_db("{}_{}".format(market, time_frame))
        EC_t1903.conn.commit()

    else: # db exist
        print('db exist')
        # EC_t1903.curs.execute("DROP DATABASE IF EXISTS {}_{}".format(market, time_frame))
        # EC_t1903.curs.execute("CREATE DATABASE {}_{}".format(market, time_frame))
        # print("CREATE DATABASE {}_{}".format(market, time_frame))
        EC_t1903.conn.select_db("{}_{}".format(market, time_frame))
        EC_t1903.conn.commit()

def check_table(hname, market, time_frame):

    # Select DB
    EC_t1903.conn.select_db("{}_{}".format(market, time_frame))

    show_tables = '''
    SHOW TABLES LIKE '{}'
    '''.format(hname)

    print(show_tables)
    EC_t1903.curs.execute(show_tables)

    table = EC_t1903.curs.fetchall()
    print(table)

    if table == (): # Table doesn't exist
        # Create Table

        # Query in string for creating hname table
        sql_set_table_daily_data = '''
           CREATE TABLE `{}`
           (일자 VARCHAR(30) NOT NULL PRIMARY KEY,
           현재가 FLOAT NULL,
           전일대비구분 FLOAT NULL,
           전일대비 FLOAT NULL,
           누적거래량 FLOAT NULL,
           NAV대비 FLOAT NULL,
           NAV FLOAT NULL,
           NAV전일대비 FLOAT NULL,
           추적오차 FLOAT NULL,
           괴리 FLOAT NULL,
           지수 FLOAT NULL,
           지수전일대비 FLOAT NULL,
           지수전일대비율 FLOAT NULL)
           '''.format(hname)
        print(sql_set_table_daily_data)
        EC_t1903.curs.execute(sql_set_table_daily_data)
        EC_t1903.conn.commit()

        print('---Table Created---')
        print(hname)
        print(market)
        print(time_frame)
        print('-------')

    else: # Table exist
        return