
import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
from modules.KIS import public_stock
from modules.stock import stock_indicator
import os

st.markdown("# 📈Chart")
stock_code_list = os.listdir('/app/Data/stock_price/')
stock_code_list = [x.replace('_Daily_Price.csv', '') for x in stock_code_list]
stock_code_list.sort()
stock_code = st.selectbox("종목코드", stock_code_list)
stock_name = public_stock.get_stock_name(stock_code)
if stock_code is not None:
    st.markdown(f"### {stock_name}({stock_code})")
    stock_df = pd.read_csv(f'/app/Data/stock_price/{stock_code}_Daily_Price.csv')
    stock_df = stock_df.sort_values(by='Date')
    stock_df = stock_df.set_index('Date')
    start_date, end_date = st.select_slider("기간 선택", options=stock_df.index, value=(stock_df.index[0], stock_df.index[-1]))
    stock_df = stock_df.loc[start_date:end_date]
    stock_price_df = stock_df[['Close']]
    st.line_chart(stock_price_df, use_container_width=True)
    


