import pandas as pd
import os
import talib

import sys
sys.path.append('/app/modules')
from KIS import stock


class StockPriceDataframe():
    def __init__(self, stock_code, **kwargs):
        self.stock_code = stock_code
        self.stock_df = pd.read_csv(f'/app/Database/stock_price/{stock_code}.csv').sort_values(by='Date')
        self.stock_name = stock.get_stock_name(stock_code)
        self.listed_date = stock.get_listing_date(stock_code)
        self.get_stock_df_with_indicators(**kwargs)
        
        
    def get_stock_df(self):
        return self.stock_df
    
    def get_stock_name(self):
        return self.stock_name
    
    def get_listed_date(self):
        return self.listed_date
    
    #ma
    def get_stock_df_with_ma(self, ma_list):
        stock_df = self.stock_df
        for ma in ma_list:
            stock_df[f"ma{ma}"] = talib.SMA(stock_df["Close"], timeperiod=ma)
        self.stock_df = stock_df
        
    #ema
    def get_stock_df_with_ema(self, ema_list):
        stock_df = self.stock_df
        for ema in ema_list:
            stock_df[f"ema{ema}"] = talib.EMA(stock_df["Close"], timeperiod=ema)
        self.stock_df = stock_df
        
    #rsi
    def get_stock_df_with_rsi(self, rsi_period):
        stock_df = self.stock_df
        stock_df["rsi"] = talib.RSI(stock_df["Close"], timeperiod=rsi_period)
        self.stock_df = stock_df
        
    #macd
    def get_stock_df_with_macd(self, macd_fastperiod, macd_slowperiod, macd_signalperiod):
        stock_df = self.stock_df
        stock_df["macd"], stock_df["macdsignal"], stock_df["macdhist"] = talib.MACD(stock_df["Close"], fastperiod=macd_fastperiod, slowperiod=macd_slowperiod, signalperiod=macd_signalperiod)
        self.stock_df = stock_df
        
    #stochastic
    def get_stock_df_with_stochastic(self, stochastic_fastk_period, stochastic_slowk_period, stochastic_slowd_period):
        stock_df = self.stock_df
        stock_df["slowk"], stock_df["slowd"] = talib.STOCH(stock_df["High"], stock_df["Low"], stock_df["Close"], fastk_period=stochastic_fastk_period, slowk_period=stochastic_slowk_period, slowk_matype=0, slowd_period=stochastic_slowd_period, slowd_matype=0)
        self.stock_df = stock_df
        
    #bollinger
    def get_stock_df_with_bollinger(self, bollinger_timeperiod, bollinger_nbdevup, bollinger_nbdevdn):
        stock_df = self.stock_df
        stock_df["upperband"], stock_df["middleband"], stock_df["lowerband"] = talib.BBANDS(stock_df["Close"], timeperiod=bollinger_timeperiod, nbdevup=bollinger_nbdevup, nbdevdn=bollinger_nbdevdn, matype=0)
        self.stock_df = stock_df
        
    #cci
    def get_stock_df_with_cci(self, cci_timeperiod):
        stock_df = self.stock_df
        stock_df["cci"] = talib.CCI(stock_df["High"], stock_df["Low"], stock_df["Close"], timeperiod=cci_timeperiod)
        self.stock_df = stock_df
        
    #adx
    def get_stock_df_with_adx(self, adx_timeperiod):
        stock_df = self.stock_df
        stock_df["adx"] = talib.ADX(stock_df["High"], stock_df["Low"], stock_df["Close"], timeperiod=adx_timeperiod)
        self.stock_df = stock_df
    
    #obv
    def get_stock_df_with_obv(self):
        stock_df = self.stock_df
        stock_df["obv"] = talib.OBV(stock_df["Close"], stock_df["Volume"])
        self.stock_df = stock_df
        
    #williams
    def get_stock_df_with_williams(self, williams_timeperiod):
        stock_df = self.stock_df
        stock_df["williams"] = talib.WILLR(stock_df["High"], stock_df["Low"], stock_df["Close"], timeperiod=williams_timeperiod)
        self.stock_df = stock_df
        
    #aroon
    def get_stock_df_with_aroon(self, aroon_timeperiod):
        stock_df = self.stock_df
        stock_df["aroon_up"], stock_df["aroon_down"] = talib.AROON(stock_df["High"], stock_df["Low"], timeperiod=aroon_timeperiod)
        self.stock_df = stock_df
        
    #roc
    def get_stock_df_with_roc(self, roc_timeperiod):
        stock_df = self.stock_df
        stock_df["roc"] = talib.ROC(stock_df["Close"], timeperiod=roc_timeperiod)
        self.stock_df = stock_df
        
    #mfi
    def get_stock_df_with_mfi(self, mfi_timeperiod):
        stock_df = self.stock_df
        stock_df["mfi"] = talib.MFI(stock_df["High"], stock_df["Low"], stock_df["Close"], stock_df["Volume"], timeperiod=mfi_timeperiod)
        self.stock_df = stock_df
        
    #adxr
    def get_stock_df_with_adxr(self, adxr_timeperiod):  
        stock_df = self.stock_df
        stock_df["adxr"] = talib.ADXR(stock_df["High"], stock_df["Low"], stock_df["Close"], timeperiod=adxr_timeperiod)
        self.stock_df = stock_df
        
    #ppo
    def get_stock_df_with_ppo(self, ppo_fastperiod, ppo_slowperiod, ppo_matype):
        stock_df = self.stock_df
        stock_df["ppo"] = talib.PPO(stock_df["Close"], fastperiod=ppo_fastperiod, slowperiod=ppo_slowperiod, matype=ppo_matype)
        self.stock_df = stock_df
        
    #mom
    def get_stock_df_with_mom(self, mom_timeperiod):
        stock_df = self.stock_df
        stock_df["mom"] = talib.MOM(stock_df["Close"], timeperiod=mom_timeperiod)
        self.stock_df = stock_df
        
    #**kwargs에 따라서 함수를 실행시키는 함수
    def get_stock_df_with_indicators(self, **kwargs):
        for key, value in kwargs.items():
            if key == "ema":
                self.get_stock_df_with_ema(value)
            elif key == "rsi":
                self.get_stock_df_with_rsi(value)
            elif key == "macd":
                self.get_stock_df_with_macd(value[0], value[1], value[2])
            elif key == "stochastic":
                self.get_stock_df_with_stochastic(value[0], value[1], value[2])
            elif key == "bollinger":
                self.get_stock_df_with_bollinger(value[0], value[1], value[2])
            elif key == "cci":
                self.get_stock_df_with_cci(value)
            elif key == "adx":
                self.get_stock_df_with_adx(value)
            elif key == "obv":
                self.get_stock_df_with_obv()
            elif key == "williams":
                self.get_stock_df_with_williams(value)
            elif key == "aroon":
                self.get_stock_df_with_aroon(value)
            elif key == "roc":
                self.get_stock_df_with_roc(value)
            elif key == "mfi":
                self.get_stock_df_with_mfi(value)
            elif key == "adxr":
                self.get_stock_df_with_adxr(value)
            elif key == "ppo":
                self.get_stock_df_with_ppo(value[0], value[1], value[2])
            elif key == "mom":
                self.get_stock_df_with_mom(value)
            else:
                print("wrong key")
    
    
    