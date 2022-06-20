# Shows daily data of ETFs (ETFs 일별추이)
import time as timefnc
import pythoncom as pcom
import pymysql
import os
from dotenv import load_dotenv

import sys
sys.setrecursionlimit(1500)

class EC_t1903:
    # Used to check tr status
    tr_success = False
    # Used for methods
    t1903_e = None

    def OnReceiveData(self, code):

        if code == "t1903":

            occurs_count = self.GetBlockCount("t1903OutBlock1")
            cts_date = self.GetFieldData("t1903OutBlock", "date", 0)
            # 종목명
            hname = self.GetFieldData("t1903OutBlock", "hname", 0)
            hname = hname.replace(" ", "_")
            # 업종지수명
            upname = self.GetFieldData("t1903OutBlock", "upname", 0)

            print('occurs_count: {}'.format(occurs_count))
            print('cts_date: {}'.format(cts_date))
            print("hname: {}".format(hname))
            print("upname: {}".format(upname))

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

                print("date: {}".format(type(date)))
                print("price: {}".format(type(price)))
                print("sign: {}".format(type(sign)))
                print("change: {}".format(type(change)))
                print("volume: {}".format(type(volume)))
                print("navdiff: {}".format(type(navdiff)))
                print("nav: {}".format(type(nav)))
                print("navchange: {}".format(type(navchange)))
                print("crate: {}".format(type(crate)))
                print("grate: {}".format(type(grate)))
                print("jisu: {}".format(type(jisu)))
                print("jichange: {}".format(type(jichange)))
                print("jirate: {}".format(type(jirate)))



def t1903_request(shcode=None, date=None, occurs=False):

    timefnc.sleep(3.1)

    EC_t1903.t1903_e.SetFieldData("t1903InBlock", "shcode", 0, shcode)
    EC_t1903.t1903_e.SetFieldData("t1903InBlock", "date", 0, date)

    EC_t1903.t1903_e.Request(occurs)

    EC_t1903.tr_success = False

    while EC_t1903.tr_success == False:
        pcom.PumpWaitingMessages()
