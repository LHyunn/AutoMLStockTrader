import json
import requests
import datetime
import os 
import os
import pandas as pd

def init_KEY(APP_KEY, APP_SECRET):
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "config.json")):
        with open(os.path.join(os.path.dirname(__file__), "config_example.json"), "w") as f:
            json.dump(json.load(open(os.path.join(os.path.dirname(__file__), "config.json"), "r")), f, ensure_ascii=False, indent=4)
        raise Exception("config.json 파일이 생성되었습니다.")
    CONFIG = json.load(open(os.path.join(os.path.dirname(__file__), "config.json"), "r"))
    CONFIG["UserConfig"]["APP_KEY"] = APP_KEY
    CONFIG["UserConfig"]["APP_SECRET"] = APP_SECRET
    with open(os.path.join(os.path.dirname(__file__), "config.json"), "w") as f:
        json.dump(CONFIG, f, ensure_ascii=False, indent=4)
    return True

class Public_API:
    def __init__(self):
        self.CONFIG = json.load(open(os.path.join(os.path.dirname(__file__), "config.json"), "r"))
        self._ACCESS_TOKEN = self.CONFIG["UserConfig"]["ACCESS_TOKEN"]
        self.ACCESS_TOKEN_EXPIRE = self.CONFIG["UserConfig"]["ACCESS_TOKEN_EXPIRE"]
        self._APP_KEY = self.CONFIG["UserConfig"]["APP_KEY"]
        self._APP_SECRET = self.CONFIG["UserConfig"]["APP_SECRET"]
        self.auth_result = self.접근토큰발급()
        
    def 접근토큰발급(self):
        if self.APP_KEY == "" or self.APP_SECRET == "":
            raise Exception("APP_KEY 또는 APP_SECRET이 설정되지 않았습니다.")
        if self.ACCESS_TOKEN == "" or datetime.datetime.strptime(self.ACCESS_TOKEN_EXPIRE,"%Y%m%d%H%M%S") < datetime.datetime.now() :
            headers = {"content-type":"application/json"}
            body = {
                "grant_type" : "client_credentials",
                "appkey" : self.APP_KEY,
                "appsecret" : self.APP_SECRET
                }
            res = requests.post(self.CONFIG["URL"]["접근토큰발급(P)"], headers=headers, data=json.dumps(body))
            try:
                ACCESS_TOKEN = res.json()["access_token"]
            except:
                raise Exception("APP_KEY 또는 APP_SECRET이 잘못되었습니다.")
            ACCESS_TOKEN_EXPIRE = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=1), "%Y%m%d%H%M%S")
            self.CONFIG["UserConfig"]["ACCESS_TOKEN"] = ACCESS_TOKEN
            self.CONFIG["UserConfig"]["ACCESS_TOKEN_EXPIRE"] = ACCESS_TOKEN_EXPIRE
            with open(os.path.join(os.path.dirname(__file__), "config.json"), "w") as f:
                json.dump(self.CONFIG, f, ensure_ascii=False, indent=4)
            return True
        else:
            return True
        
    def 국내주식기간별시세(self, stock_code, start_date, end_date, period_div_code="D"):
        headers = {
            "content-type" : "application/json",
            "authorization" : "Bearer " + self.ACCESS_TOKEN,
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
        res = (requests.get(self.CONFIG["URL"]["국내주식기간별시세(일/주/월/년)"], headers=headers, params=query))
        return res.json()
        
    def 주식현재가시세(self, stock_code):
        headers = {
            "content-type" : "application/json; charset=utf-8",
            "authorization" : "Bearer " + self.ACCESS_TOKEN,
            "appkey" : self.APP_KEY,
            "appsecret" : self.APP_SECRET,
            "tr_id" : "FHKST01010100",
            "custtype" : "P"
        }
        query = {
            "FID_COND_MRKT_DIV_CODE" : "J",
            "FID_INPUT_ISCD" : stock_code
        }
        res = (requests.get(self.CONFIG["URL"]["주식현재가 시세"], headers=headers, params=query))
        return res.json()
        
