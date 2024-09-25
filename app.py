import streamlit as st
import json
import os
from Cloud_storage import cloud_storage_page
import pygwalker
import pandas as pd
from pygwalker.api.streamlit import StreamlitRenderer
import base64
import requests
import logging
from user_manager import load_users, AuthManager
from page_manager import PageManager
from st_on_hover_tabs import on_hover_tabs
from PIL import Image
import folium
from streamlit_folium import folium_static
st.set_page_config(
        page_title="Frontier Lab",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# 设置版本信息
VERSION = "1.0.0"

def main():
    
    # 优化自定义CSS
    st.markdown("""
        <style>
        .stApp {
            background-color: #f0f2f6;
            font-family: 'Helvetica Neue', Arial, sans-serif;
        }
        .main .block-container {
            padding: 2rem;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stButton>button {
            background-color: #4a90e2;
            color: white;
            border-radius: 20px;
            padding: 0.6rem 1.2rem;
            font-weight: bold;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(74, 144, 226, 0.3);
        }
        .stButton>button:hover {
            background-color: #357ae8;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(74, 144, 226, 0.4);
        }
        .stTextInput>div>div>input {
            border-radius: 20px;
            border: 2px solid #e0e0e0;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        .stTextInput>div>div>input:focus {
            border-color: #4a90e2;
            box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
        }
        .sidebar .sidebar-content {
            background-color: #ffffff;
            border-right: 1px solid #e0e0e0;
        }
        .stSelectbox {
            border-radius: 20px;
            border: 2px solid #e0e0e0;
        }
        .stMarkdown a {
            color: #4a90e2;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        .stMarkdown a:hover {
            color: #357ae8;
            text-decoration: underline;
        }
        </style>
        """, unsafe_allow_html=True)

    # 显示动画logo
    st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; height: 100px;">
            <img src="Images/sdu_logo2.jpg" alt="SDU Logo" style="max-height: 100%; max-width: 100%; object-fit: contain; animation: pulse 2s infinite;">
        </div>
        <style>
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 检查图片是否存在
    import os
    if not os.path.exists("Images/sdu_logo2.jpg"):
        st.error("无法找到logo图片。请确保 'Images/sdu_logo2.jpg' 文件存在。")

    users = load_users()
    auth_manager = AuthManager(users)

    if 'username' not in st.session_state:
        st.session_state.update({'username': None, 'role': None, 'login_page': False})

    page_manager = PageManager(st.session_state.get('role'), users, auth_manager)

    if st.session_state['username'] is None:
        if st.session_state['login_page']:
            handle_login(auth_manager)
        else:
            page_manager.display_pages()
            if st.sidebar.button("登录以访问更多内容", key="login_button"):
                st.session_state['login_page'] = True
    else:
        page_manager.display_pages()

    # 美化侧边栏内容
    with st.sidebar:
        st.markdown("---")
        st.markdown(
            '<h6 style="text-align: center;">由 <img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16"> 强力驱动</h6>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="display: flex; justify-content: center; margin-top: 0.75em;"><a href="https://moderny-alexander.streamlit.app/" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="支持我们" height="41" width="174"></a></div>',
            unsafe_allow_html=True,
        )
        # 添加版本信息
        st.text(f"版本: {VERSION}")

def handle_login(auth_manager):
    st.markdown("<h1 style='text-align: center; color: #4a90e2;'>欢迎登录</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>请登录以访问更多精彩内容。</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        username = st.text_input("用户名", placeholder="请输入用户名", key="username_input")
        password = st.text_input("密码", type="password", placeholder="请输入密码", key="password_input")
        
        remember_me = st.checkbox("记住我")
        
        if st.button("登录", key="login_submit"):
            if username and password:
                user = auth_manager.authenticate_user(username, password)
                if user:
                    st.balloons()
                    st.success("登录成功！正在跳转...")
                    st.session_state.update({'username': username, 'role': user['role'], 'login_page': False})
                else:
                    st.error("用户名或密码无效")
            else:
                st.warning("用户名和密码不能为空")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("忘记密码？", key="forgot_password"):
            st.info("请联系管理员重置密码")
    with col2:
        if st.button("没有账号？注册", key="register"):
            st.info("请联系管理员创建新账号")

def handle_logout():
    st.session_state.update({'username': None, 'role': None, 'login_page': False})
    st.success("已退出登录")

if __name__ == "__main__":
    main()