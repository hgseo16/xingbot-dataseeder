from login import *
from dotenv import load_dotenv
from liststocks import *
from dailychart import *
# from spy_500.spy_500_seeder import *
from spy_500.mysql_spy import *
from spy_500.spy_500_backtester import *

from kospi_kosdaq.kospi_kosdaq_daily import *

from liststocks import *

import time
import os
import win32com.client as wc

class Main():

    def __init__(self):
        print("실행")

        # Create XASession Object
        self.XASession = wc.DispatchWithEvents("XA_Session.XASession", XASessionCallbackEvent)

        # If connection to server fails: False, Paper Trading Server(모의서버): demo, Actual Server(실서버): hts
        if self.XASession.ConnectServer("hts.ebestsec.co.kr", 20001) == True:
            print("실서버 연결 완료")
        # if self.XASession.ConnectServer("demo.ebestsec.co.kr", 20001) == True:
        #     print("모의투자 서버 연결 완료")
        else:
            nErrCode = self.XASession.GetLastError()
            print(nErrCode)
            strErrMsg = self.XASession.GetErrorMessage(nErrCode)
            print(strErrMsg)

        # Login

        load_dotenv()

        ID = os.environ.get('ID')
        PASSWORD = os.environ.get('PASSWORD')
        AUTHENTICATION_PASSWORD = os.environ.get('AUTHENTICATION_PASSWORD')

        if self.XASession.Login(ID, PASSWORD, AUTHENTICATION_PASSWORD, 0, False):
            print("로그인 요청")

        while XASessionCallbackEvent.login_success == False:
            # Runs a loop which checks whether are there messages
            # Inefficient to run other code while in this loop
            pcom.PumpWaitingMessages()
            # Give time as this loop eats up too much CPU
            time.sleep(0.1)

        # Look up Day Candles for SPI@SPX and Stores them in mySQL
        # SPY_t3518 = EventClass_t3518
        # SPY_t3518.t3518_e = wc.DispatchWithEvents("XA_DataSet.XAQuery", SPY_t3518)
        # SPY_t3518.t3518_e.ResFileName = "C:/eBEST/xingAPI/Res/t3518.res"
        # t3518_request(kind='S', symbol='SPI@SPX', cnt='500', jgbn='0', nmin='', cts_date='', cts_time='', occurs=False)

        # Backtests w/ SPY
        # Backtest_Engine()


        # Implement calling for ETF data
        # KODEX 레버리지 (122630)
        KODEX_LEVERAGE_t1903 = EC_t1903
        KODEX_LEVERAGE_t1903.t1903_e = wc.DispatchWithEvents("XA_DataSet.XAQuery", KODEX_LEVERAGE_t1903)
        KODEX_LEVERAGE_t1903.t1903_e.ResFileName = "C:/eBEST/xingAPI/Res/t1903.res"
        t1903_request(shcode="122630", date="", time_frame="daily")

        # KODEX 200 선물인버스2X (252670)
        KODEX_200_INVERSE2X_t1903 = EC_t1903
        KODEX_200_INVERSE2X_t1903.t1903_e = wc.DispatchWithEvents("XA_DataSet.XAQuery", KODEX_200_INVERSE2X_t1903)
        KODEX_200_INVERSE2X_t1903.t1903_e.ResFileName = "C:/eBEST/xingAPI/Res/t1903.res"
        t1903_request(shcode="252670", date="", time_frame="daily")


if __name__ == "__main__":
    start = time.time()
    # print(start)
    Main()
    end = time.time()
    print(f"Runtime of the program is {end - start}")