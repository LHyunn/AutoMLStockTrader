import streamlit as st
from .KIS import public_api as kis


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
    with st.expander("KIS 인증 및 종목코드 업데이트"):
        if kis.Auth().auth_result:
            st.success("KIS 인증에 성공하였습니다.")
            pass
        else:
            st.error("KIS 인증에 실패하였습니다. 관리자에게 문의하세요.")
            pass
        
        if kis.update_stock_code():
            st.success("종목코드 업데이트에 성공하였습니다.")
            pass
        else:
            st.error("종목코드 업데이트에 실패하였습니다. 관리자에게 문의하세요.")
            pass
        
    
    

    
    
def set_sidebar():
    """
    Streamlit 사이드바 설정.
    """
    st.sidebar.title("2023 캡스톤디자인")

    menu = st.sidebar.selectbox("",("Home", "Data", "Model", "Result"))

    return menu
