import time as timefnc
import pythoncom as pcom
import pymysql
import os
from dotenv import load_dotenv


# Event class which returns daily data for SPI@SPX
class EventClass_t3518:
    # Used to check tr status
    tr_success = False
    # Used for methods
    t3518_e = None
    # List of all 날짜 (date)
    date_list = []
    # List of all 시간 (time)
    time_list = []
    # List of all 시가 (open)
    open_list = []
    # List of all 고가 (high)
    high_list = []
    # List of all 저가 (low)
    low_list = []
    # List of all 가격 (price)
    price_list = []
    # List of all 전일대비구분 (sign)
    sign_list = []
    # List of all 전일대비 (change)
    change_list = []
    # List of all 등락률 (uprate)
    uprate_list = []
    # List of all 누적거래량 (volume)
    volume_list = []
    # List of all 한국일자 (kodate)
    kodate_list = []
    # List of all 한국시간 (kotime)
    kotime_list = []

    load_dotenv()

    AUTHENTICATION_PASSWORD = os.environ.get('AUTHENTICATION_PASSWORD')

    conn = pymysql.connect(host='127.0.0.1', user='root', password=AUTHENTICATION_PASSWORD, charset='utf8')

    curs = conn.cursor()

    # For Deleting and Recreating db spy_500
    curs.execute('DROP DATABASE IF EXISTS SPY_500')
    curs.execute('CREATE DATABASE SPY_500')
    conn.select_db('SPY_500')
    sql_set_table_daily_data = '''
    CREATE TABLE SPY_500_daily
    (날짜 VARCHAR(30) NOT NULL PRIMARY KEY,
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
    curs.execute(sql_set_table_daily_data)
    conn.commit()

    def OnReceiveData(self, code):

        if code == "t3518":
            occurs_count = self.GetBlockCount("t3518OutBlock1")
            cts_date = self.GetFieldData("t3518OutBlock", "cts_date", 0)
            cts_time = self.GetFieldData("t3518OutBlock", "cts_time", 0)
            print(occurs_count)
            print(cts_date)
            print(cts_time)

            for i in range(occurs_count):
                inverse_idx = occurs_count - i - 1
                date = self.GetFieldData("t3518OutBlock1", "date", inverse_idx)
                time = self.GetFieldData("t3518OutBlock1", "time", inverse_idx)
                open = self.GetFieldData("t3518OutBlock1", "open", inverse_idx)
                high = self.GetFieldData("t3518OutBlock1", "high", inverse_idx)
                low = self.GetFieldData("t3518OutBlock1", "low", inverse_idx)
                price = self.GetFieldData("t3518OutBlock1", "price", inverse_idx)
                sign = self.GetFieldData("t3518OutBlock1", "sign", inverse_idx)
                change = self.GetFieldData("t3518OutBlock1", "change", inverse_idx)
                uprate = self.GetFieldData("t3518OutBlock1", "uprate", inverse_idx)
                volume = self.GetFieldData("t3518OutBlock1", "volume", inverse_idx)
                kodate = self.GetFieldData("t3518OutBlock1", "kodate", inverse_idx)
                kotime = self.GetFieldData("t3518OutBlock1", "kotime", inverse_idx)

                # EventClass_t3518.date_list.append(date)
                # EventClass_t3518.time_list.append(time)
                # EventClass_t3518.open_list.append(open)
                # EventClass_t3518.high_list.append(high)
                # EventClass_t3518.low_list.append(low)
                # EventClass_t3518.price_list.append(price)
                # EventClass_t3518.sign_list.append(sign)
                # EventClass_t3518.change_list.append(change)
                # EventClass_t3518.uprate_list.append(uprate)
                # EventClass_t3518.volume_list.append(volume)
                # EventClass_t3518.kodate_list.append(kodate)
                # EventClass_t3518.kotime_list.append(kotime)

                mysql_spy(date, time, open, high, low, price, sign, change, uprate, volume, kodate, kotime)

            if cts_date != "":
                # 다음 과거 데이터로 계산
                t3518_request(kind="S", symbol="SPI@SPX", cnt=500, jgbn=None, nmin="", cts_date=cts_date,
                              cts_time=cts_time, occurs=self.IsNext)
            else:
                EventClass_t3518.conn.close()
                EventClass_t3518.tr_success = True


def t3518_request(kind=None, symbol=None, cnt=None, jgbn=None, nmin=None, cts_date=None,
                  cts_time=None, occurs=False):
    print('requested')
    timefnc.sleep(3.1)
    EventClass_t3518.t3518_e.SetFieldData("t3518InBlock", "kind", 0, "S")
    EventClass_t3518.t3518_e.SetFieldData("t3518InBlock", "symbol", 0, symbol)
    EventClass_t3518.t3518_e.SetFieldData("t3518InBlock", "cnt", 0, "500")
    EventClass_t3518.t3518_e.SetFieldData("t3518InBlock", "jgbn", 0, "0")
    EventClass_t3518.t3518_e.SetFieldData("t3518InBlock", "nmin", 0, "")
    EventClass_t3518.t3518_e.SetFieldData("t3518InBlock", "cts_date", 0, cts_date)
    EventClass_t3518.t3518_e.SetFieldData("t3518InBlock", "cts_time", 0, cts_time)

    EventClass_t3518.t3518_e.Request(occurs)

    EventClass_t3518.tr_success = False

    while EventClass_t3518.tr_success == False:
        pcom.PumpWaitingMessages()


def mysql_spy(date, time, open, high, low, price, sign, change, uprate, volume, kodate, kotime):

        # curs.execute('DROP DATABASE IF EXISTS SPY_500')
        # curs.execute('CREATE DATABASE SPY_500')
        EventClass_t3518.conn.select_db('SPY_500')
        # curs.execute(sql_set_table_daily_data)
        sql_insert_daily_data = '''
        INSERT INTO SPY_500_DAILY
        (날짜, 시간, 시가, 고가, 저가, 가격, 
        전일대비구분, 전일대비, 등락률, 누적거래량, 한국일자, 한국시간)
        VALUE
        ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})
        '''.format(str(date), str(time), str(open), str(high), str(low), str(price), str(sign), str(change),
                   str(uprate), str(volume), str(kodate), str(kotime))
        EventClass_t3518.curs.execute(sql_insert_daily_data)
        EventClass_t3518.conn.commit()





