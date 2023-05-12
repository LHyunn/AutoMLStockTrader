import os
import pandas as pd
import numpy as np

from modules.quantylab.rltrader import settings

COLUMNS_CHART_DATA = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']


def load_data(df, date_from, date_to):
    print("여기는 data_manager.py의 load_data() 함수입니다.")
    print("df.head() : ")
    print(df.head())
    

    # 날짜 오름차순 정렬
    df = df.sort_values(by='Date').reset_index(drop=True)

    # 기간 필터링
    df['Date'] = df['Date'].astype(int)
    df = df[(df['Date'] >= int(date_from)) & (df['Date'] <= int(date_to))]
    df = df.dropna()
    
    # 차트 데이터 분리
    chart_data = df[COLUMNS_CHART_DATA]
    print("chart_data.head() : ")
    print(chart_data.head())
    # 트레이닝 데이터 분리. df에서 차트 데이터를 제외한 나머지 데이터를 트레이닝 데이터로 사용
    training_data = df.drop(columns=COLUMNS_CHART_DATA)
    print("training_data.head() : ")
    print(training_data.head())
    
    
    
    return chart_data, training_data

