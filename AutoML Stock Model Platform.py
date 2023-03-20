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
    st.title("AutoML Stock Model Platform")
    config.init_session()
    
    
    
    