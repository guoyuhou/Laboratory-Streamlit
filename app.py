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


def main():
    st.set_page_config(
        page_title="Frontier Lab",  # 设置网页标题
        page_icon="🚀",             # 使用火箭emoji作为favicon
        layout="wide",              # 设置页面布局为宽屏
        initial_sidebar_state="collapsed"  # 设置侧边栏初始状态为折叠
    )

    # 优化自定义CSS
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(to right, #f0f4f8, #e0eaf5);
        }
        .stButton>button {
            background-color: #3498db;
            color: white;
            border-radius: 5px;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #2980b9;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        .stTextInput>div>div>input {
            border-radius: 5px;
            border: 1px solid #bdc3c7;
        }
        .stTextInput>div>div>input:focus {
            border-color: #3498db;
            box-shadow: 0 0 5px rgba(52, 152, 219, 0.5);
        }
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
        </style>
        """, unsafe_allow_html=True)

    # 显示logo
    st.logo('Images/sdu_logo2.jpg')

    users = load_users()
    auth_manager = AuthManager(users)

    if 'username' not in st.session_state:
        st.session_state.update({'username': None, 'role': None, 'login_page': False, 'edit_content': ''})

    if st.session_state['username'] is None:
        if st.session_state['login_page']:
            handle_login(auth_manager)
        else:
            PageManager(None, users, auth_manager).display_pages()
            if st.sidebar.button("登录以访问更多内容", key="login_button"):
                st.session_state['login_page'] = True
    else:
        st.sidebar.success(f"欢迎回来，{st.session_state['username']}！")
        page_manager = PageManager(st.session_state['role'], users, auth_manager)
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

def handle_login(auth_manager):
    st.title("欢迎登录")
    st.write("请登录以访问更多精彩内容。")
    
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
        if st.button("忘记密码？"):
            st.info("请联系管理员重置密码")
    with col2:
        if st.button("没有账号？注册"):
            st.info("请联系管理员创建新账号")

def handle_logout():
    st.session_state.update({'username': None, 'role': None, 'login_page': False})
    st.success("已退出登录")


if __name__ == "__main__":
    main()
