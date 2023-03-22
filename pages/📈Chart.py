import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
from modules.KIS import public_api, stock
import FinanceDataReader as fdr

st.markdown("# 📈Chart")
stock_code_list = stock.get_stock_list()
stock_code = st.selectbox("종목코드", stock_code_list)
public_api.init_KEY(APP_KEY="PS3RGjPgZhiW28Tq89ba75qkGPCiUGp0b6kf", APP_SECRET="oDe/hWTSx8CL7OP/tLhI8UMiPwNyumhXHnfd3iatGDNqB/N1vfSdSldqFAxD3CHd9rhZIjkafOSPIzVi48vmdMrweaGOMVvkao8kam12pCGcYd5pkVGUiZhW8A969j6FiJNVj1zkLYsILfB6gbot+jf9ZBdshzbR5F+f3XfEzB5EGyl9+wU=")
API = public_api.Public_API()
if st.button("조회"):
    stock_ohlcv = API.주식현재가시세(stock_code)
    st.write(stock_ohlcv)
    #st.plotly_chart(px.line(stock_ohlcv, x=stock_ohlcv.index, y="Close"), use_container_width=True)
    #st.dataframe(stock_ohlcv, use_container_width=True)