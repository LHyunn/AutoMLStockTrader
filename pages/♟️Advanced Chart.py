import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from modules.KIS import public_api, public_stock, auth
from modules.stock import stock_indicator
import os
import talib
import numpy as np

if 'data' not in st.session_state:
    data = pd.DataFrame({'colA':[],'colB':[],'colC':[],'colD':[]})
    st.session_state.data = data


st.markdown("# ♟️Advanced Chart")
stock_code_list = os.listdir('/app/Data/stock_price/')
stock_code_list = [x.replace('.csv', '') for x in stock_code_list]
stock_code_list.sort()
notice = st.expander("📌주의사항")
notice.markdown("1. MACD, Stochastic, Bollinger, PPO는 각 3개의 param을 입력해야 합니다.")
notice.markdown("2. OBV는 param을 입력하지 않습니다.")
notice.markdown("3. 0을 입력하면 해당 param은 제외됩니다.")
notice.markdown("4. 기간을 선택하면 해당 기간의 데이터만 보여집니다.")
notice.markdown("5. 값에 대한 유효성 검사는 하지 않습니다.")

stock_code = st.selectbox("종목코드", stock_code_list)
col1, col2 = st.columns([1, 1])
slider = col1.empty()
num_rows = col2.slider('보조지표 수', min_value=0,max_value=20,value=1)


if stock_code is not None:
    stock_info = stock_indicator.StockPriceDataframe(stock_code)
    stock_df = stock_info.stock_df
    
    form = st.form(key='my_form')
    
    expander = form.expander("보조지표 선택")
    start_date, end_date = slider.select_slider("기간 선택", options=stock_df.index, value=(stock_df.index[0], stock_df.index[-1]))

    container = expander.container()
    def add_row(row):
        with container:
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            col1.selectbox('Indicator', key=f'input_indicator_{row}', options=["ma", "ema", "rsi", "macd", "stochastic", "bollinger", "cci", "adx", "obv", "williams", "aroon", "roc", "mfi", "adxr", "ppo", "mom"])
            col2.slider('Param1', min_value=0, max_value=365, key=f'slider_indicator_params_1_{row}')
            col3.slider('Param2', min_value=0, max_value=365, key=f'slider_indicator_params_2_{row}')
            col4.slider('Param3', min_value=0, max_value=365, key=f'slider_indicator_params_3_{row}')
    if num_rows > 0:
        for r in range(num_rows):
            add_row(r)
    
    
    
    submit_button = form.form_submit_button(label='조회하기')
    if submit_button:
        kwargs = {}
        for r in range(num_rows):
            index = r
            key = st.session_state[f'input_indicator_{r}']
            param1 = st.session_state[f'slider_indicator_params_1_{r}']
            #값이 0이면 None으로 변경
            param2 = st.session_state[f'slider_indicator_params_2_{r}'] if st.session_state[f'slider_indicator_params_2_{r}'] != 0 else None
            param3 = st.session_state[f'slider_indicator_params_3_{r}'] if st.session_state[f'slider_indicator_params_3_{r}'] != 0 else None
            kwargs[index] = {'key':key, 'param1':param1, 'param2':param2, 'param3':param3}
    
        for index, value in kwargs.items():
            stock_info.calc_indicators(key = value['key'], param1 = value['param1'], param2 = value['param2'], param3 = value['param3'])
        stock_df = stock_info.stock_df
        stock_df.dropna(inplace=True)
        df_download = stock_info.stock_df.copy()
        origin_df = stock_df[['Open', 'High', 'Low', 'Close', 'Volume']]
        #df_download의 값들을 이전 행에 대한 변화율로 변경
        df_download = df_download.pct_change(periods=1)
        #column명 변경
        df_download.columns = [f"{x}_change" for x in df_download.columns]
        #컬럼 제거
        df_download.drop(['Stock_code_change', 'Change_change'], axis=1, inplace=True)
        #두개의 dataframe을 합침
        df_download = pd.concat([origin_df, df_download], axis=1)
        #결측치 제거    
        df_download.dropna(inplace=True)
        #0으로 나누는 경우가 있어서 inf가 생기는 경우가 있음
        df_download = df_download.replace([np.inf, -np.inf], np.nan)
        #결측치 제거
        
        st.download_button(label="Download", data=df_download.to_csv().encode('utf-8'), file_name=f"{stock_code}.csv", mime="text/csv")
        #####after calculate indicator
        stock_df = stock_df.loc[start_date:end_date]
        fig = make_subplots(rows=15, cols=1, shared_xaxes=True, vertical_spacing=0.01)
        fig.add_trace(go.Candlestick(x=stock_df.index,
                        open=stock_df['Open'],
                        high=stock_df['High'],
                        low=stock_df['Low'],
                        close=stock_df['Close']), row=1, col=1)
        fig.update_layout(xaxis_rangeslider_visible=False)
        
        now_row = 2
        for index, value in kwargs.items():
            
            if value['key'] == "ma":
                fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df[f"ma{value['param1']}"], name=f"{value['key']}{value['param1']}"), row=1, col=1)
            elif value['key'] == "ema":
                fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df[f"ema{value['param1']}"], name=f"{value['key']}{value['param1']}"), row=1, col=1)
            elif value['key'] == "rsi":
                fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df[f"rsi{value['param1']}"], name=f"{value['key']}{value['param1']}"), row=2, col=1)
                
            elif value['key'] == "cci":
                fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df[f"cci{value['param1']}"], name=f"{value['key']}{value['param1']}"), row=3, col=1)
                
            elif value['key'] == "adx":
                fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df[f"adx{value['param1']}"], name=f"{value['key']}{value['param1']}"), row=4, col=1)
                
            elif value['key'] == "obv":
                fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df[f"obv{value['param1']}"], name=f"{value['key']}{value['param1']}"), row=5, col=1)
                
            elif value['key'] == "roc":
                fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df[f"roc{value['param1']}"], name=f"{value['key']}{value['param1']}"), row=6, col=1)
                
            elif value['key'] == "mfi":
                fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df[f"mfi{value['param1']}"], name=f"{value['key']}{value['param1']}"), row=7, col=1)
                
            elif value['key'] == "adxr":
                fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df[f"adxr{value['param1']}"], name=f"{value['key']}{value['param1']}"), row=8, col=1)
                
            elif value['key'] == "ppo":
                fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df[f"ppo{value['param1']}"], name=f"{value['key']}{value['param1']}"), row=9, col=1)
                
            elif value['key'] == "mom":
                fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df[f"mom{value['param1']}"], name=f"{value['key']}{value['param1']}"), row=10, col=1)
                
            elif value['key'] == "williams":
                fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df[f"williams{value['param1']}"], name=f"{value['key']}{value['param1']}"), row=11, col=1)
                
            elif value['key'] == "aroon":
          
                fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df[f"aroonup{value['param1']}"], name=f"{value['key']}{value['param1']}"), row=12, col=1)
                fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df[f"aroondown{value['param1']}"], name=f"{value['key']}{value['param1']}"), row=12, col=1)
                
            elif value['key'] == "macd":
            
                fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df[f"macd{value['param1']}"], name=f"{value['key']}_macd"), row=13, col=1)
                fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df[f"macdsignal{value['param1']}"], name=f"{value['key']}_signal"), row=13, col=1)
                fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df[f"macdhist{value['param1']}"], name=f"{value['key']}_hist"), row=13, col=1)
                
            elif value['key'] == "stochastic":
            
                fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df[f"slowk{value['param1']}"], name=f"{value['key']}_slowk"), row=14, col=1)
                fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df[f"slowd{value['param1']}"], name=f"{value['key']}_slowd"), row=14, col=1)
                
            elif value['key'] == "bollinger":
            
                fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df[f"upperband{value['param1']}"], name=f"{value['key']}_upperband"), row=1, col=1)
                fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df[f"middleband{value['param1']}"], name=f"{value['key']}_middleband"), row=1, col=1)
                fig.add_trace(go.Scatter(x=stock_df.index, y=stock_df[f"lowerband{value['param1']}"], name=f"{value['key']}_lowerband"), row=1, col=1)
                
            
                

        
        fig = fig.update_layout(height=3000*now_row)
        st.plotly_chart(fig, use_container_width=True)
        
        
        
