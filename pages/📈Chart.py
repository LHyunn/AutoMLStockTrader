import streamlit as st

import FinanceDataReader as fdr
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px


st.markdown("# 📈Chart")

stock_code = st.text_input("종목코드를 입력하세요.", "005930")

if st.button("조회"):
    stock_data = fdr.DataReader(stock_code)
    st.plotly_chart(px.line(stock_data, x=stock_data.index, y="Close"), use_container_width=True)
    st.dataframe(stock_data, use_container_width=True)