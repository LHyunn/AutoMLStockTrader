import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
from modules.KIS import public_api, public_stock, auth
import FinanceDataReader as fdr

st.markdown("# 🔑Set Config.json")
APP_KEY = st.text_input("APP_KEY")
SECRET_KEY = st.text_input("SECRET_KEY")

if st.button("Create New Config.json"):
    st.write(auth.init_KEY(APP_KEY, SECRET_KEY))
