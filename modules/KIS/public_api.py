import json
import requests
import datetime
import os 
import os
import pandas as pd

class APIResp:
    #응답코드, 응답헤더, Output, 오류코드, 오류메시지
    def __init__(self, resp):
        self._rescode = resp.status_code
        self._resp = resp
        self._header = self._setHeader()
        self._body = self._setBody()
        self._err_code = self._body.rt_cd
        self._err_message = self._body.msg1

    #
    def getResCode(self):
        return self._rescode

    def _setHeader(self):
        fld = dict()
        for x in self._resp.headers.keys():
            if x.islower():
                fld[x] = self._resp.headers.get(x)
        _th_ = namedtuple('header', fld.keys())

        return _th_(**fld)

    def _setBody(self):
        _tb_ = namedtuple('body', self._resp.json().keys())

        return _tb_(**self._resp.json())

    def getHeader(self):
        return self._header

    def getBody(self):
        return self._body

    def getResponse(self):
        return self._resp

    def isOK(self):
        try:
            if (self.getBody().rt_cd == '0'):
                return True
            else:
                return False
        except:
            return False

    def getErrorCode(self):
        return self._err_code

    def getErrorMessage(self):
        return self._err_message

    def printAll(self):
        # print(self._resp.headers)
        print("<Header>")
        for x in self.getHeader()._fields:
            print(f'\t-{x}: {getattr(self.getHeader(), x)}')
        print("<Body>")
        for x in self.getBody()._fields:
            print(f'\t-{x}: {getattr(self.getBody(), x)}')

    def printError(self):
        print('-------------------------------\nError in response: ', self.getResCode())
        print(self.getBody().rt_cd, self.getErrorCode(), self.getErrorMessage())
        print('-------------------------------')

class Public_API:
    def __init__(self):
        self.CONFIG = json.load(open(os.path.join(os.path.dirname(__file__), "config.json"), "r"))
        self.ACCESS_TOKEN = self.CONFIG["UserConfig"]["ACCESS_TOKEN"]
        self.ACCESS_TOKEN_EXPIRE = self.CONFIG["UserConfig"]["ACCESS_TOKEN_EXPIRE"]
        self.APP_KEY = self.CONFIG["UserConfig"]["APP_KEY"]
        self.APP_SECRET = self.CONFIG["UserConfig"]["APP_SECRET"]
        self.auth_result = self.auth_kis()
        
    def auth_kis(self):  
        if self.ACCESS_TOKEN == "" or datetime.datetime.strptime(self.ACCESS_TOKEN_EXPIRE,"%Y%m%d%H%M%S") < datetime.datetime.now() :
            try:
                headers = {"content-type":"application/json"}
                body = {
                    "grant_type" : "client_credentials",
                    "appkey" : self.APP_KEY,
                    "appsecret" : self.APP_SECRET
                    }
                URL = self.CONFIG["URL"]["접근토큰발급(P)"]
                res = requests.post(URL, headers=headers, data=json.dumps(body))
                ACCESS_TOKEN = res.json()["access_token"]
                ACCESS_TOKEN_EXPIRE = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=1), "%Y%m%d%H%M%S")
                self.CONFIG["UserConfig"]["ACCESS_TOKEN"] = ACCESS_TOKEN
                self.CONFIG["UserConfig"]["ACCESS_TOKEN_EXPIRE"] = ACCESS_TOKEN_EXPIRE
                with open(os.path.join(os.path.dirname(__file__), "config.json"), "w") as f:
                    json.dump(self.CONFIG, f, ensure_ascii=False, indent=4)
                return True
            except:
                return False
        else:
            return True
        
    def 국내주식기간별시세(self, stock_code, start_date, end_date, period_div_code="D"):
        try:
            headers = {
                "content-type" : "application/json",
                "authorization" : self.ACCESS_TOKEN,
                "appkey" : self.APP_KEY,
                "appsecret" : self.APP_SECRET,
                "tr_id" : "FHKST03010100",
                "custtype" : "P"
            }
            
            query = {
                "FID_COND_MRKT_DIV_CODE" : "J",
                "FID_INPUT_ISCD" : stock_code,
                "FID_INPUT_DATE_1" : start_date,
                "FID_INPUT_DATE_2" : end_date,
                "FID_ORG_ADJ_PRC" : "0",
                "FID_PERIOD_DIV_CODE" : period_div_code
            }
            
            res = (requests.post(self.CONFIG["URL"]["국내주식기간별시세(일/주/월/년)"], headers=headers, data=json.dumps(query)))
            return res.json()
                
            
        except:
            return False
        
    def 주식현재가시세(self, stock_code):
        try:
            headers = {
                "content-type" : "application/json; charset=utf-8",
                "authorization" : self.ACCESS_TOKEN,
                "appkey" : self.APP_KEY,
                "appsecret" : self.APP_SECRET,
                "tr_id" : "FHKST01010100",
                "custtype" : "P"
            }
            
            query = {
                "FID_COND_MRKT_DIV_CODE" : "J",
                "FID_INPUT_ISCD" : stock_code
            }
            
            res = (requests.post(self.CONFIG["URL"]["주식현재가 시세"], headers=headers, data=json.dumps(query)))
            if res.status_code == 200:
                ar = APIResp(res)
                return ar.getBody()
                
            
        except:
            return False
        
