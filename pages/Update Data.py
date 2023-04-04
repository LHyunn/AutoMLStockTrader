import streamlit as st
import pandas as pd
from modules.KIS import public_api, public_stock, auth, preprocess_res
import datetime
import os


API = public_api.Public_API()
st.title("주가 정보, 재무 정보 업데이트")
st.write("## 주가 정보 업데이트")
st.write("### 주가 정보 업데이트를 위해 아래의 버튼을 눌러주세요.")
button = st.button("주가 정보 업데이트")
if button:
    st.write("### 주가 정보 업데이트를 시작합니다.")
    progress = st.empty()
    progress.progress(0)
    stock_list = public_stock.get_stock_list()
    for i, stock_code in enumerate(stock_list):
        progress.progress((i+1)/len(stock_list))
        stock_info = pd.DataFrame(columns=["Stock_code","Date", "Open", "High", "Low", "Close", "Volume", "Amount", "Change"])
        today = datetime.datetime.today()
        str_today = today.strftime("%Y%m%d")

        first_date = (datetime.datetime.strptime(str_today, "%Y%m%d") - datetime.timedelta(days=140)).strftime("%Y%m%d")

        if os.path.exists(f"/app/Data/stock_price/{stock_code}/{stock_code}_Daily_Price.csv"):
            origin_stock_info = pd.read_csv(f"/app/Data/stock_price/{stock_code}/{stock_code}_Daily_Price.csv", index_col=0)
            last_date = origin_stock_info.index[-1]
            last_date = (datetime.datetime.strptime(str(last_date), "%Y-%m-%d") - datetime.timedelta(days=7)).strftime("%Y%m%d")
            
        while datetime.datetime.strptime(str_today, "%Y%m%d") > datetime.datetime.strptime(str(last_date), "%Y%m%d"):
            print(first_date, str_today)
            res = API.국내주식기간별시세(stock_code, first_date, str_today)
            history_len = len(stock_info)
            stock_info = preprocess_res.save_price_info(res, stock_info)
            if res["rt_cd"] == "0":
                str_today = first_date
                first_date = (datetime.datetime.strptime(str_today, "%Y%m%d") - datetime.timedelta(days=100)).strftime("%Y%m%d")
            else:
                break
            if history_len == len(stock_info):
                break
            


        stock_info["Date"] = [datetime.datetime.strptime(str(i), "%Y%m%d").strftime("%Y-%m-%d") for i in stock_info["Date"]]
        stock_info = stock_info.astype({"Open": float, "High": float, "Low": float, "Close": float, "Volume": int, "Amount": int, "Change": float})
        stock_info.set_index("Date", inplace=True)
        stock_info.sort_index(inplace=True)
        stock_info = stock_info[~stock_info.index.duplicated(keep='first')]
        print(stock_info)
        origin_stock_info.iloc[:,0] = origin_stock_info.iloc[:,0].astype(str)
        origin_stock_info.iloc[:,0] = origin_stock_info.iloc[:,0].str.zfill(6)
        print(origin_stock_info)

        #두 데이터 프레임을 합치고, 중복된 데이터는 stock_info를 기준으로 합친다.
        stock_info = pd.concat([origin_stock_info, stock_info], axis=0)
        stock_info.to_csv(f"/app/Data/stock_price/{stock_code}/{stock_code}_Daily_Price.csv")
    st.write("### 주가 정보 업데이트를 완료했습니다.")
    