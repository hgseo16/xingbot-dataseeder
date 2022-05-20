# Login event handler

class XASessionCallbackEvent:
    # Used to check login status
    login_success = False

    def OnLogin(self, szCode, szMsg):
        print("로그인 결과 수신 %s, %s" % (szCode, szMsg))
        XASessionCallbackEvent.login_success = True


