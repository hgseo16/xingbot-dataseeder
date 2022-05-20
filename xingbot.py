from login import *
from dotenv import load_dotenv
from liststocks import *
from dailychart import *

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

        # print("ID: %s, PASSWORD: %s, AUTHENTICATION_PASSWORD: %s" % (ID, PASSWORD, AUTHENTICATION_PASSWORD))

        if self.XASession.Login(ID, PASSWORD, AUTHENTICATION_PASSWORD, 0, False):
            print("로그인 요청 성공")

        while XASessionCallbackEvent.login_success == False:
            # Runs a loop which checks whether are there messages
            # Inefficient to run other code while in this loop
            pcom.PumpWaitingMessages()
            # Give time as this loop eats up too much CPU
            time.sleep(0.1)


        # Loop up KOSPI Stocks
        Kospi_t9945 = EventClass_t9945
        Kospi_t9945.t9945_e = wc.DispatchWithEvents("XA_DataSet.XAQuery", Kospi_t9945)
        Kospi_t9945.t9945_e.ResFileName = "C:/eBEST/xingAPI/Res/t9945.res"
        # KOSPI: 1, KOSDAQ: 2
        Kospi_t9945.t9945_e.SetFieldData("t9945InBlock", "gubun", 0, "1")
        Kospi_t9945.t9945_e.Request(False)

        while Kospi_t9945.tr_success == False:
            pcom.PumpWaitingMessages()
            time.sleep(0.1)

        print("Finished listing KOSPI  Stocks")

        # # Loop up KOSDAQ Stocks
        # Kosdaq_t9945 = EventClass_t9945
        # Kosdaq_t9945.t9945_e = wc.DispatchWithEvents("XA_DataSet.XAQuery", Kosdaq_t9945)
        # Kosdaq_t9945.t9945_e.ResFileName = "C:/eBEST/xingAPI/Res/t9945.res"
        # # KOSPI: 1, KOSDAQ: 2
        # Kosdaq_t9945.t9945_e.SetFieldData("t9945InBlock", "gubun", 0, "2")
        # Kosdaq_t9945.t9945_e.Request(False)
        #
        # while Kosdaq_t9945.tr_success == False:
        #     pcom.PumpWaitingMessages()
        #     time.sleep(0.1)
        #
        # print("Finished listing KOSDAQ  Stocks")

        # Look up Day Candles
        Kospi_t8413 = EventClass_t8413
        Kospi_t8413.t8413_e = wc.DispatchWithEvents("XA_DataSet.XAQuery", Kospi_t8413)
        Kospi_t8413.t8413_e.ResFileName = "C:/eBEST/xingAPI/Res/t8413.res"
        for shcode in Kospi_t9945.shcode_list:
            if shcode == "005930":
                t8413_request(shcode=shcode, gubun="2", qrycnt=500, sdate="", edate="99999999", cts_date="", comp_yn="N")


if __name__ == "__main__":
    Main()