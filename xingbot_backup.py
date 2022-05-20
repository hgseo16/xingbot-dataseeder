import win32com.client as wc
# Controls activeX's COM method
import os

import pythoncom as pcom
import time

from dotenv import load_dotenv


class XASessionCallbackEvent:
    # Used to check login status
    login_success = False

    def OnLogin(self, szCode, szMsg):
        print("로그인 결과 수신 %s, %s" % (szCode, szMsg))
        XASessionCallbackEvent.login_success = True


class EventClass_t9945:
    # Used to check tr status
    tr_success = False
    # Used for methods
    t9945_e = None
    # Dict of all hname (종목명) and shcode (단축코드)
    hname_shcode_dict = {}
    # List of all shcode (단축코드)
    shcode_list = []

    def OnReceiveData(self, code):

        print("OnReceiveData")

        if code == "t9945":
            occurs_count = self.GetBlockCount("t9945OutBlock")
            for i in range(occurs_count):
                # Ticker Name (종목명)
                hname = self.GetFieldData("t9945OutBlock", "hname", i)
                # Ticker Code (단축코드/종목코드)
                shcode = self.GetFieldData("t9945OutBlock", "shcode", i)
                EventClass_t9945.hname_shcode_dict.update({hname: shcode})
                EventClass_t9945.shcode_list.append(shcode)

            EventClass_t9945.tr_success = True

            print("Dict of {hname: shcode}: ")
            print(EventClass_t9945.hname_shcode_dict)
            print("List of shcode")
            print(EventClass_t9945.shcode_list)


class EventClass_t8413:
    # Used to check tr status
    tr_success = False
    # Used for methods
    t8413_e = None
    # 수정주가비율 계산에 필요한 변수
    rate_list = []
    # List of dates
    date_list = []
    # List of closing prices
    close_list = []

    def OnReceiveData(self, code):

        if code == "t8413":

            shcode = self.GetFieldData("t8413OutBlock", "shcode", 0)
            cts_date = self.GetFieldData("t8413OutBlock", "cts_date", 0)

            # 수정주가비율부터 모은다
            occurs_count = self.GetBlockCount("t8413OutBlock")

            for i in range(occurs_count):
                inverse_idx = occurs_count - i - 1
                date = self.GetFieldData("t8413OutBlock1", "date", inverse_idx)  # date
                close = self.GetFieldData("t8413OutBlock1", "close", inverse_idx)  # close price
                close = int(close)
                rate = self.GetFieldData("t8413OutBlock1", "rate", inverse_idx)  # 수정주가비율
                rate = float(rate)

                print("계산전: %s" % close)

                # 수정주가 비율의 리스트에 담겨져 있는게 있다면
                if len(EventClass_t8413.rate_list) > 0:
                    # 수정주가 비율 리스트가 있으면 for 문을 돌린다.
                    for ra in EventClass_t8413.rate_list:
                        # 수정주가비율 계산을 한다.
                        close = close * (100 + ra) / 100
                        close = round(close)
                        print("계산후: %s" % close)

                # 수정주가 반영된 리스트를 담아준다
                EventClass_t8413.date_list.append(date)
                EventClass_t8413.close_list.append(close)

                if rate != 0.0:
                    EventClass_t8413.rate_list.append(rate)

            if self.IsNext is True:
                # 다음 과거 데이터로 계산
                Main.t8413_request(shcode=shcode, gubun="2", qrycnt=500, sdate="", edate="9999999", cts_date=cts_date,
                                   comp_yn="N", occurs=self.IsNext)
            else:
                EventClass_t8413.tr_success = True


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
            print("로그인 요청 성공")

        while XASessionCallbackEvent.login_success == False:
            # Runs a loop which checks whether are there messages
            # Inefficient to run other code while in this loop
            pcom.PumpWaitingMessages()
            # Give time as this loop eats up too much CPU
            time.sleep(0.1)

        # Loop up KOSPI Stocks
        EventClass_t9945.t9945_e = wc.DispatchWithEvents("XA_DataSet.XAQuery", EventClass_t9945)
        EventClass_t9945.t9945_e.ResFileName = "C:/eBEST/xingAPI/Res/t9945.res"
        # KOSPI: 1, KOSDAQ: 2
        EventClass_t9945.t9945_e.SetFieldData("t9945InBlock", "gubun", 0, "1")
        EventClass_t9945.t9945_e.Request(False)

        while EventClass_t9945.tr_success == False:
            pcom.PumpWaitingMessages()
            time.sleep(0.1)

        print("Finished listing KOSPI or KOSDAQ Stocks")

        # Look up Day Candles
        EventClass_t8413.t8413_e = wc.DispatchWithEvents("XA_DataSet.XAQuery", EventClass_t8413)
        EventClass_t8413.t8413_e.ResFileName = "C:/eBEST/xingAPI/Res/t8413.res"
        for shcode in EventClass_t9945.shcode_list:
            if shcode == "005930":
                Main.t8413_request(shcode=shcode, gubun="2", qrycnt=500, sdate="", edate="99999999", cts_date="",
                                   comp_yn="N")

    # @staticmethod gets rid of self
    @staticmethod
    def t8413_request(shcode=None, gubun=None, qrycnt=None, sdate=None, edate=None, cts_date=None, comp_yn=None,
                      occurs=False):

        time.sleep(3.1)
        EventClass_t8413.t8413_e.SetFieldData("t8413InBlock", "shcode", 0, shcode)
        EventClass_t8413.t8413_e.SetFieldData("t8413InBlock", "gubun", 0, gubun)
        EventClass_t8413.t8413_e.SetFieldData("t8413InBlock", "qrycnt", 0, qrycnt)
        EventClass_t8413.t8413_e.SetFieldData("t8413InBlock", "sdate", 0, sdate)
        EventClass_t8413.t8413_e.SetFieldData("t8413InBlock", "edate", 0, edate)
        EventClass_t8413.t8413_e.SetFieldData("t8413InBlock", "cts_date", 0, cts_date)
        EventClass_t8413.t8413_e.SetFieldData("t8413InBlock", "comp_yn", 0, comp_yn)

        EventClass_t8413.t8413_e.Request(occurs)

        EventClass_t8413.tr_success = False
        while EventClass_t8413.tr_success == False:
            pcom.PumpWaitingMessages()


if __name__ == "__main__":
    Main()