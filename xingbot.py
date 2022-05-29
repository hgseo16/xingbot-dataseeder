from login import *
from dotenv import load_dotenv
from liststocks import *
from dailychart import *
from spy_500.spy_500_seeder import *
from spy_500.mysql_spy import *

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

        # Look up Day Candles for SPI@SPX
        SPY_t3518 = EventClass_t3518
        SPY_t3518.t3518_e = wc.DispatchWithEvents("XA_DataSet.XAQuery", SPY_t3518)
        SPY_t3518.t3518_e.ResFileName = "C:/eBEST/xingAPI/Res/t3518.res"
        t3518_request(kind='S', symbol='SPI@SPX', cnt='500', jgbn='0', nmin='', cts_date='', cts_time='', occurs=False)
        mysql_spy(EventClass_t3518.date_list, EventClass_t3518.time_list, EventClass_t3518.open_list, EventClass_t3518.high_list, EventClass_t3518.low_list, EventClass_t3518.price_list, EventClass_t3518.sign_list, EventClass_t3518.change_list, EventClass_t3518.uprate_list, EventClass_t3518.volume_list, EventClass_t3518.kodate_list, EventClass_t3518.kotime_list)

if __name__ == "__main__":
    Main()