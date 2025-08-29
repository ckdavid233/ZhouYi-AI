import streamlit as st
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 页面配置
st.set_page_config(
    page_title="主页",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 重定向到主页
st.switch_page("pages/主页.py")