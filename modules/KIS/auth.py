import json
import os 
import shutil

def init_KEY(APP_KEY, APP_SECRET):
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "config.json")):
        shutil.copy(os.path.join(os.path.dirname(__file__), "config_example.json"), os.path.join(os.path.dirname(__file__), "config.json"))
    CONFIG = json.load(open(os.path.join(os.path.dirname(__file__), "config.json"), "r"))
    CONFIG["UserConfig"]["APP_KEY"] = APP_KEY
    CONFIG["UserConfig"]["APP_SECRET"] = APP_SECRET
    with open(os.path.join(os.path.dirname(__file__), "config.json"), "w") as f:
        json.dump(CONFIG, f, ensure_ascii=False, indent=4)
    return "config.json 파일이 생성되었습니다."

def delete_KEY():
    if os.path.exists(os.path.join(os.path.dirname(__file__), "config.json")):
        os.remove(os.path.join(os.path.dirname(__file__), "config.json"))
    return "config.json 파일이 삭제되었습니다."