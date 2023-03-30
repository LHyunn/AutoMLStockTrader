import pandas as pd
import os
import talib

import sys
sys.path.append('/app/modules')
from modules.KIS import public_stock


class StockPriceDataframe():
    def __init__(self, stock_code, **kwargs):
        self.stock_code = stock_code
        self.stock_df = pd.read_csv(f'/app/Database/stock_price/{stock_code}.csv').set_index('Date').sort_values(by='Date')
        self.stock_name = public_stock.get_stock_name(stock_code)
        self.listed_date = public_stock.get_listing_date(stock_code)
        
        
        
    def get_stock_df(self):
        return self.stock_df
    
    def get_stock_name(self):
        return self.stock_name
    
    def get_listed_date(self):
        return self.listed_date
    
    #ma
    def get_stock_df_with_ma(self, ma):
        stock_df = self.stock_df
        stock_df[f"ma{ma}"] = talib.SMA(stock_df["Close"], timeperiod=ma)
        self.stock_df = stock_df
        
    #ema
    def get_stock_df_with_ema(self, ema):
        stock_df = self.stock_df
        stock_df[f"ema{ema}"] = talib.EMA(stock_df["Close"], timeperiod=ema)
        self.stock_df = stock_df
        
    #rsi
    def get_stock_df_with_rsi(self, rsi_period):
        stock_df = self.stock_df
        stock_df[f"rsi{rsi_period}"] = talib.RSI(stock_df["Close"], timeperiod=rsi_period)
        self.stock_df = stock_df
        
    #macd
    def get_stock_df_with_macd(self, fastperiod, slowperiod, signalperiod):
        stock_df = self.stock_df
        stock_df[f"macd{fastperiod}"], stock_df[f"macdsignal{fastperiod}"], stock_df[f"macdhist{fastperiod}"] = talib.MACD(stock_df["Close"], fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
        self.stock_df = stock_df
        
    #stochastic
    def get_stock_df_with_stochastic(self, fastk_period, slowk_period, slowd_period):
        stock_df = self.stock_df
        stock_df[f"slowk{fastk_period}"], stock_df[f"slowd{fastk_period}"] = talib.STOCH(stock_df["High"], stock_df["Low"], stock_df["Close"], fastk_period=fastk_period, slowk_period=slowk_period, slowd_period=slowd_period)
        self.stock_df = stock_df
   
    #bollinger
    def get_stock_df_with_bollinger(self, timeperiod, nbdevup, nbdevdn):
        stock_df = self.stock_df
        stock_df[f"upperband{timeperiod}"], stock_df[f"middleband{timeperiod}"], stock_df[f"lowerband{timeperiod}"] = talib.BBANDS(stock_df["Close"], timeperiod=timeperiod, nbdevup=nbdevup, nbdevdn=nbdevdn)
        self.stock_df = stock_df
    
    #cci
    def get_stock_df_with_cci(self, timeperiod):
        stock_df = self.stock_df
        stock_df[f"cci{timeperiod}"] = talib.CCI(stock_df["High"], stock_df["Low"], stock_df["Close"], timeperiod=timeperiod)
        self.stock_df = stock_df
    
    #adx
    def get_stock_df_with_adx(self, timeperiod):
        stock_df = self.stock_df
        stock_df[f"adx{timeperiod}"] = talib.ADX(stock_df["High"], stock_df["Low"], stock_df["Close"], timeperiod=timeperiod)
        self.stock_df = stock_df
    
    
    #obv
    def get_stock_df_with_obv(self):
        stock_df = self.stock_df
        stock_df["obv"] = talib.OBV(stock_df["Close"], stock_df["Volume"])
        self.stock_df = stock_df
   
        
    #williams
    def get_stock_df_with_williams(self, timeperiod):
        stock_df = self.stock_df
        stock_df[f"williams{timeperiod}"] = talib.WILLR(stock_df["High"], stock_df["Low"], stock_df["Close"], timeperiod=timeperiod)
        self.stock_df = stock_df
    
        
    #aroon
    def get_stock_df_with_aroon(self, timeperiod):
        stock_df = self.stock_df
        stock_df[f"aroonup{timeperiod}"], stock_df[f"aroondown{timeperiod}"] = talib.AROON(stock_df["High"], stock_df["Low"], timeperiod=timeperiod)
        self.stock_df = stock_df
        
        
    #roc
    def get_stock_df_with_roc(self, timeperiod):
        stock_df = self.stock_df
        stock_df[f"roc{timeperiod}"] = talib.ROC(stock_df["Close"], timeperiod=timeperiod)
        self.stock_df = stock_df
    
        
    #mfi
    def get_stock_df_with_mfi(self, timeperiod):
        stock_df = self.stock_df
        stock_df[f"mfi{timeperiod}"] = talib.MFI(stock_df["High"], stock_df["Low"], stock_df["Close"], stock_df["Volume"], timeperiod=timeperiod)
        self.stock_df = stock_df
    
        
    #adxr
    def get_stock_df_with_adxr(self, timeperiod):
        stock_df = self.stock_df
        stock_df[f"adxr{timeperiod}"] = talib.ADXR(stock_df["High"], stock_df["Low"], stock_df["Close"], timeperiod=timeperiod)
        self.stock_df = stock_df
    
        
    #ppo
    def get_stock_df_with_ppo(self, fastperiod, slowperiod, matype):
        stock_df = self.stock_df
        stock_df[f"ppo{fastperiod}"] = talib.PPO(stock_df["Close"], fastperiod=fastperiod, slowperiod=slowperiod, matype=matype)
        self.stock_df = stock_df
    
        
    #mom
    def get_stock_df_with_mom(self, timeperiod):
        stock_df = self.stock_df
        stock_df[f"mom{timeperiod}"] = talib.MOM(stock_df["Close"], timeperiod=timeperiod)
        self.stock_df = stock_df
    
        
    def calc_indicators(self, key, param1, param2, param3):
        if key == "ma":
            self.get_stock_df_with_ma(param1)
        elif key == "ema":
            self.get_stock_df_with_ema(param1)
        elif key == "rsi":
            self.get_stock_df_with_rsi(param1)
        elif key == "macd":
            self.get_stock_df_with_macd(param1, param2, param3)
        elif key == "stochastic":
            self.get_stock_df_with_stochastic(param1, param2, param3)
        elif key == "bollinger":
            self.get_stock_df_with_bollinger(param1, param2, param3)
        elif key == "cci":
            self.get_stock_df_with_cci(param1)
        elif key == "adx":
            self.get_stock_df_with_adx(param1)
        elif key == "obv":
            self.get_stock_df_with_obv()
        elif key == "williams":
            self.get_stock_df_with_williams(param1)
        elif key == "aroon":
            self.get_stock_df_with_aroon(param1)
        elif key == "roc":
            self.get_stock_df_with_roc(param1)
        elif key == "mfi":
            self.get_stock_df_with_mfi(param1)
        elif key == "adxr":
            self.get_stock_df_with_adxr(param1)
        elif key == "ppo":
            self.get_stock_df_with_ppo(param1, param2, param3)
        elif key == "mom":
            self.get_stock_df_with_mom(param1)
        else:
            print("wrong key")
                
    #indicator list = ["ma", "ema", "rsi", "macd", "stochastic", "bollinger", "cci", "adx", "obv", "williams", "aroon", "roc", "mfi", "adxr", "ppo", "mom"]
    
    
    