import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
from modules.KIS import public_api, stock, auth
import os
import talib


st.markdown("# 📈Chart")
stock_code_list = os.listdir('/app/Database/stock_price/')
stock_code_list = [x.replace('.csv', '') for x in stock_code_list]
stock_code_list.sort()
stock_code = st.selectbox("종목코드", stock_code_list)
if stock_code is not None:
    stock_df = pd.read_csv(f'/app/Database/stock_price/{stock_code}.csv')
    #20000101 to 2000-01-01
    stock_df["Date"]=stock_df["Date"].astype(str)
    stock_df["Date"]=stock_df["Date"].str.slice(0,4)+"-"+stock_df["Date"].str.slice(4,6)+"-"+stock_df["Date"].str.slice(6,8)
    stock_df = stock_df.sort_values(by='Date')
    stock_df["ma5"] = talib.SMA(stock_df["Close"], timeperiod=5)
    stock_df["ma20"] = talib.SMA(stock_df["Close"], timeperiod=20)
    stock_df["ma60"] = talib.SMA(stock_df["Close"], timeperiod=60)
    
    stock_df = stock_df[-200:]
    fig = go.Figure(data=go.Candlestick(x=stock_df['Date'],
                    open=stock_df['Open'],
                    high=stock_df['High'],
                    low=stock_df['Low'],
                    close=stock_df['Close']))
    fig.add_trace(go.Scatter(x=stock_df['Date'], y=stock_df['ma5'], name='ma5'))
    fig.add_trace(go.Scatter(x=stock_df['Date'], y=stock_df['ma20'], name='ma20'))
    fig.add_trace(go.Scatter(x=stock_df['Date'], y=stock_df['ma60'], name='ma60'))
    fig.update_layout(title=f'{stock_code} Chart', xaxis_title='Date', yaxis_title='Price')
    
    st.plotly_chart(fig, use_container_width=True)
