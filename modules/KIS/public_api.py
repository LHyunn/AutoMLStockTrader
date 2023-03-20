import json
import requests
import datetime
import os 


class Auth:
    def __init__(self):
        self.CONFIG = json.load(open(os.path.join(os.path.dirname(__file__), "config.json"), "r"))
        self.ACCESS_TOKEN = self.CONFIG["UserConfig"]["ACCESS_TOKEN"]
        self.ACCESS_TOKEN_EXPIRE = self.CONFIG["UserConfig"]["ACCESS_TOKEN_EXPIRE"]
        self.APP_KEY = self.CONFIG["UserConfig"]["APP_KEY"]
        self.APP_SECRET = self.CONFIG["UserConfig"]["APP_SECRET"]
        self.URL = self.CONFIG["URL"]["접근토큰발급(P)"]
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
                PATH = self.CONFIG["URL"]["접근토큰발급(P)"]
                URL = f"{PATH}"
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
        
class Public_API:
    pass



        



