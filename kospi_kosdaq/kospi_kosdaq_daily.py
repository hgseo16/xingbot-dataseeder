# Shows daily data of ETFs (ETFs 일별추이)
import time as timefnc
import pythoncom as pcom
import pymysql
import os
from dotenv import load_dotenv

class EventClass_t1903:
    # Used to check tr status
    tr_success = False
    # Used for methods
    t1903_e = None

    load_dotenv()

    AUTHENTICATION_PASSWORD = os.environ.get('AUTHENTICATION_PASSWORD')

    conn = pymysql.connect(host='127.0.0.1', user='root', password=AUTHENTICATION_PASSWORD, charset='utf8')

    curs = conn.cursor()

    # For Deleting and Recreating db spy_500
    curs.execute('DROP DATABASE IF EXISTS KODEX_LEVERAGE')
    curs.execute('CREATE DATABASE KODEX_LEVERAGE')
    conn.select_db('KODEX_LEVERAGE')

    sql_set_table_daily_data = '''
    CREATE TABLE KODEX_LEVERAGE_daily
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
    '''
    curs.execute(sql_set_table_daily_data)
    conn.commit()


    def OnReceiveData(self, code):
        print("OnReceiveData")

        if code == "t1903":
            print('ETF 일별추이 Called')
            occurs_count = self.GetBlockCount("t1903OutBlock1")
            cts_date = self.GetFieldData("t1903OutBlock", "date", 0)
            print("CTS_DATE: {}".format(cts_date))
            hname = self.GetFieldData("t1903OutBlock", "hname", 0)
            upname = self.GetFieldData("t1903OutBlock", "upname", 0)
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


                mysql_etf(date, price, sign, change, volume, navdiff, nav, navchange, crate, grate, jisu, jichange, jirate)

            if cts_date != "":
                t1903_request(shcode='122630', date=cts_date, occurs=self.IsNext)
            else:
                EventClass_t1903.conn.close()
                EventClass_t1903.tr_success = True


def t1903_request(shcode=None, date=None, occurs=False):
    timefnc.sleep(3.1)
    EventClass_t1903.t1903_e.SetFieldData("t1903InBlock", "shcode", 0, shcode)
    EventClass_t1903.t1903_e.SetFieldData("t1903InBlock", "date", 0, date)
    print("Inserted Date: {}".format(date))

    EventClass_t1903.t1903_e.Request(occurs)

    EventClass_t1903.tr_success = False

    while EventClass_t1903.tr_success == False:
        pcom.PumpWaitingMessages()

def mysql_etf(date, price, sign, change, volume, navdiff, nav, navchange, crate, grate, jisu, jichange, jirate):

        # curs.execute('DROP DATABASE IF EXISTS SPY_500')
        # curs.execute('CREATE DATABASE SPY_500')
        EventClass_t1903.conn.select_db('KODEX_LEVERAGE')
        # curs.execute(sql_set_table_daily_data)
        sql_insert_daily_data = '''
        INSERT INTO KODEX_LEVERAGE_daily
        (일자, 현재가, 전일대비구분, 전일대비, 누적거래량, NAV대비, 
        NAV, NAV전일대비, 추적오차, 괴리, 지수, 지수전일대비, 지수전일대비율)
        VALUE
        ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})
        '''.format(str(date), str(price), str(sign), str(change), str(volume), str(navdiff), str(nav), str(navchange),
                   str(crate), str(grate), str(jisu), str(jichange), str(jirate))
        EventClass_t1903.curs.execute(sql_insert_daily_data)
        EventClass_t1903.conn.commit()


