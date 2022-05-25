import time
import pythoncom as pcom

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

    def OnReceiveData(self, code):

        print("OnReceiveData")

        if code == "t3518":
            occurs_count = self.GetBlockCount("t3518OutBlock1")
            cts_date = self.GetFieldData("t3518OutBlock", "cts_date", 0)
            cts_time = self.GetFieldData("t3518OutBlock", "cts_time", 0)

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

                EventClass_t3518.date_list.append(date)
                EventClass_t3518.time_list.append(time)
                EventClass_t3518.open_list.append(open)
                EventClass_t3518.high_list.append(high)
                EventClass_t3518.low_list.append(low)
                EventClass_t3518.price_list.append(price)
                EventClass_t3518.sign_list.append(sign)
                EventClass_t3518.change_list.append(change)
                EventClass_t3518.uprate_list.append(uprate)
                EventClass_t3518.volume_list.append(volume)
                EventClass_t3518.kodate_list.append(kodate)
                EventClass_t3518.kotime_list.append(kotime)

            # print(EventClass_t3518.date_list)
            # print(EventClass_t3518.time_list)
            # print(EventClass_t3518.open_list)
            # print(EventClass_t3518.high_list)
            # print(EventClass_t3518.low_list)
            # print(EventClass_t3518.price_list)
            # print(EventClass_t3518.sign_list)
            # print(EventClass_t3518.change_list)
            # print(EventClass_t3518.uprate_list)
            # print(EventClass_t3518.volume_list)
            # print(EventClass_t3518.kodate_list)
            # print(EventClass_t3518.kotime_list)

            if cts_date != "":
                # 다음 과거 데이터로 계산
                t3518_request(kind="S", symbol="SPI@SPX", cnt=500, jgbn=None, nmin="", cts_date=cts_date,
                  cts_time=cts_time, occurs=self.IsNext)
            else:
                print(len(self.date_list))
                EventClass_t3518.tr_success = True



def t3518_request(kind=None, symbol=None, cnt=None, jgbn=None, nmin=None, cts_date=None,
                  cts_time=None, occurs=False):
    time.sleep(3.1)
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