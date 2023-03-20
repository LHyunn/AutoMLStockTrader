import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
from modules.KIS import public_api as kis
import FinanceDataReader as fdr

st.markdown("# 📈Chart")
stock_df = kis.get_stock_data()
stock_code_list = stock_df["단축코드"]
stock_code = st.selectbox("종목코드", stock_code_list)

if st.button("조회"):
    stock_ohlcv = fdr.DataReader(stock_code)
    st.plotly_chart(px.line(stock_ohlcv, x=stock_ohlcv.index, y="Close"), use_container_width=True)
    st.dataframe(stock_ohlcv, use_container_width=True)