import streamlit as st
from .KIS import auth


def set_config():
    """
    Streamlit 기본 설정.
    """
    st.set_page_config(
        page_title="ML기반 주가 예측 모델 플랫폼",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
        'About': "제작자 : 이창현,  https://www.notion.so/dns05018/L-Hyun-s-Portfolio-f1c904bf9f2445fb96909da6eb3d450d?pvs=4"
    }
    )
    
def init_session():
    auth_token = auth.auth_kis()
    if 'key' not in st.session_state:
        st.session_state.key = auth_token

    
    
def set_sidebar():
    """
    Streamlit 사이드바 설정.
    """
    st.sidebar.title("2023 캡스톤디자인")

    menu = st.sidebar.selectbox("",("Home", "Data", "Model", "Result"))

    return menu
