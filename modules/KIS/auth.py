import json
import requests
import datetime
import os 

def auth_kis():
    config = json.load(open(os.path.join(os.path.dirname(__file__), "config.json"), "r"))
    ACCESS_TOKEN = config["UserConfig"]["ACCESS_TOKEN"]
    if config["UserConfig"]["ACCESS_TOKEN"] == "" or datetime.datetime.strptime(config["UserConfig"]["ACCESS_TOKEN_EXPIRE"],"%Y%m%d%H%M%S") < datetime.datetime.now() :
        headers = {"content-type":"application/json"}
        body = {
            "grant_type":"client_credentials",
            "appkey":config["UserConfig"]["APP_KEY"],
            "appsecret":config["UserConfig"]["APP_SECRET"]
            }
        URL_BASE = config["URL"]["URL_BASE"]
        PATH = "oauth2/tokenP"
        URL = f"{URL_BASE}/{PATH}"
        res = requests.post(URL, headers=headers, data=json.dumps(body))
        ACCESS_TOKEN = res.json()["access_token"]
        ACCESS_TOKEN_EXPIRE = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=1), "%Y%m%d%H%M%S")
        config["UserConfig"]["ACCESS_TOKEN"] = ACCESS_TOKEN
        config["UserConfig"]["ACCESS_TOKEN_EXPIRE"] = ACCESS_TOKEN_EXPIRE
        with open(os.path.join(os.path.dirname(__file__), "config.json"), "w") as f:
            json.dump(config, f)

    return ACCESS_TOKEN
