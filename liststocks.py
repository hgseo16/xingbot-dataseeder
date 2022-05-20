# Event class which returns a dictionary of all KOSPI or KOSDAQ stocks

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
                EventClass_t9945.hname_shcode_dict.update({hname:shcode})
                EventClass_t9945.shcode_list.append(shcode)

            EventClass_t9945.tr_success = True

            print("Dict of {hname: shcode}: ")
            print(EventClass_t9945.hname_shcode_dict)
            print("List of shcode")
            print(EventClass_t9945.shcode_list)