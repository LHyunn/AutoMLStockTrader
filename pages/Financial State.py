from modules import config
from modules.KIS import public_stock
import streamlit as st
import os
import pandas as pd


col1, col2, col3, col4, col5= st.columns([3,3,3,3,2])
annual = col1.selectbox("분기/연간", os.listdir("/app/Data/Info/Sort By Time"), label_visibility="collapsed")
consolidated = col2.selectbox("별도/연결", os.listdir(f"/app/Data/Info/Sort By Time/{annual}"), label_visibility="collapsed")
document = col3.selectbox("재무제표/포괄손익계산서", ["재무제표", "포괄손익계산서"], label_visibility="collapsed")
year = col4.selectbox("목록", ["-".join(file.split("-")[:-2]) for file in os.listdir(f"/app/Data/Info/Sort By Time/{annual}/{consolidated}/") if document in file], label_visibility="collapsed")
button = col5.button("조회")
if button:
    file_list = [file for file in os.listdir(f"/app/Data/Info/Sort By Time/{annual}/{consolidated}/") if document in file and year in file]
    dataframe = pd.read_csv(f"/app/Data/Info/Sort By Time/{annual}/{consolidated}/{file_list[0]}")
    #첫번째 열을 문자열로 변환
    dataframe.iloc[:,0] = dataframe.iloc[:,0].astype(str)
    dataframe.iloc[:,0] = dataframe.iloc[:,0].str.zfill(6)
    #첫번째 열의 이름을 종목코드로 변경
    dataframe.rename(columns={dataframe.columns[0]:"종목코드"}, inplace=True)
    #종목코드를 인덱스로 설정
    dataframe.set_index("종목코드", inplace=True)
    #모든 컬럼이 none이면 삭제
    dataframe.dropna(axis=1, how="all", inplace=True)
    #매출액 기준 정렬
    dataframe.sort_values(by="매출액", ascending=False, inplace=True)
    st.dataframe(dataframe, height=2000, use_container_width=True)
