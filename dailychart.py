import time
# Controls activeX's COM method
import pythoncom as pcom


# Event class which stores the daily data of a stock

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
                date = self.GetFieldData("t8413OutBlock1", "date", inverse_idx) # date
                close = self.GetFieldData("t8413OutBlock1", "close", inverse_idx) # close price
                close = int(close)
                rate = self.GetFieldData("t8413OutBlock1", "rate", inverse_idx) # 수정주가비율
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
                t8413_request(shcode=shcode, gubun="2", qrycnt=500, sdate="", edate="9999999", cts_date=cts_date, comp_yn="N", occurs=self.IsNext)
            else:
                EventClass_t8413.tr_success = True






# @staticmethod gets rid of self
# @staticmethod
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