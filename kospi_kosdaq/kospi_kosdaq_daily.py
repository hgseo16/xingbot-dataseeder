# Shows daily data of ETFs (ETFs 일별추이)

class EventClass_t1903:
    # Used to check tr status
    tr_success = False
    # Used for methods
    t1903_e = None
    # Dict of all hname (종목명) and shcode (단축코드)
    hname_shcode_dict = {}
    # List of all shcode (단축코드)
    shcode_list = []

    def OnReceiveData(self, code):
        print("OnReceiveData")

        if code == "t1903":
            print('ETF 일별추이 Called')
            occurs_count = self.GetBlockCount("t1903OutBlock1")
            date = self.GetFieldData("t1903OutBlock", "date", 0)
            hname = self.GetFieldData("t1903OutBlock", "hname", 0)
            upname = self.GetFieldData("t1903OutBlock", "upname", 0)


