from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from modules import config
import json
from modules.KIS import *

if __name__ == "__main__":
    config.set_config()
    st.title("ML Stock Platform")
    st.subheader("머신러닝을 이용한 주식 투자 플랫폼")
    config.init_session()
    
    
    
    