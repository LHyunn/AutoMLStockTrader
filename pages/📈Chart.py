import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
from modules.KIS import public_api, stock, auth
import FinanceDataReader as fdr

st.markdown("# 📈Chart")
stock_code_list = stock.get_stock_list()
stock_code = st.selectbox("종목코드", stock_code_list)
API = public_api.Public_API()
if st.button("조회"):
    stock_ohlcv = API.주식현재가시세(stock_code)
    st.write(stock_ohlcv)
    #st.plotly_chart(px.line(stock_ohlcv, x=stock_ohlcv.index, y="Close"), use_container_width=True)
    #st.dataframe(stock_ohlcv, use_container_width=True)