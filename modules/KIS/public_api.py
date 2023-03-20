import json
import requests
import datetime
import os 
import os
import pandas as pd



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
                self.CONFIG["UserConfig"]["ACCESS_TOKEN"] = "Bearer " + ACCESS_TOKEN
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
                "FID_PERIOD_DIV_CODE" : period_div_code,
                "FID_ORG_ADJ_PRC" : "0"
            }
            
            res = (requests.post(self.CONFIG["URL"]["국내주식기간별시세(일/주/월/년)"], headers=headers, data=json.dumps(query))).json()
            if res["rt_cd"] == "0":
                pass
                
                
            

    
            
                
                
            
            
            return True
        except:
            return False