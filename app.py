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
            background-color: white;
            font-family: 'Helvetica Neue', Arial, sans-serif;
        }
        .main .block-container {
            padding-top: 1rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 1rem;
        }
        .stButton>button {
            background-color: #4a90e2;
            color: white;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #357ae8;
        }
        .stTextInput>div>div>input {
            border-radius: 4px;
            border: 1px solid #e0e0e0;
        }
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
        .stSelectbox {
            border-radius: 4px;
            border: 1px solid #e0e0e0;
        }
        .stMarkdown a {
            color: #4a90e2;
            text-decoration: none;
        }
        .stMarkdown a:hover {
            text-decoration: underline;
        }
        </style>
        """, unsafe_allow_html=True)

    # 显示logo
    st.logo('Images/sdu_logo2.jpg')

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
            '<h6 style="text-align: center;">由 <img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16"> 强力驱动 Made by ModernY</h6>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="display: flex; justify-content: center; margin-top: 0.75em;"><a href="https://moderny-alexander.streamlit.app/" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="支持我们" height="41" width="174"></a></div>',
            unsafe_allow_html=True,
        )
        # 添加版本信息
        st.text(f"版本: {VERSION}")

    # 主题切换
    st.sidebar.title("主题切换")
    theme = st.sidebar.radio("选择主题", ["Light", "Dark"])
    set_theme(theme)

def handle_login(auth_manager):
    st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 30px;
            background-color: #f8f9fa;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .login-title {
            text-align: center;
            color: #333;
            font-size: 24px;
            margin-bottom: 20px;
        }
        .login-input {
            margin-bottom: 15px;
        }
        .login-button {
            width: 100%;
            background-color: #007bff;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .login-button:hover {
            background-color: #0056b3;
        }
        .login-footer {
            text-align: center;
            margin-top: 20px;
            font-size: 14px;
        }
        .login-footer a {
            color: #007bff;
            text-decoration: none;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="login-title">欢迎登录</h2>', unsafe_allow_html=True)

    username = st.text_input("用户名", placeholder="请输入用户名", key="username_input")
    password = st.text_input("密码", type="password", placeholder="请输入密码", key="password_input")
    
    remember_me = st.checkbox("记住我")
    
    col1, col2 = st.columns(2)
    with col1:
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
    with col2:
        if st.button("返回主页", key="return_home"):
            st.session_state['login_page'] = False
            st.snow()
    st.markdown('<div class="login-footer">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<a href="#" onclick="alert(\'请联系管理员重置密码\')">忘记密码？</a>', unsafe_allow_html=True)
    with col2:
        st.markdown('<a href="#" onclick="alert(\'请联系管理员创建新账号\')">没有账号？注册</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def handle_logout():
    st.session_state.update({'username': None, 'role': None, 'login_page': False})
    st.success("已退出登录")

def set_theme(theme):
    if theme == "Light":
        st.markdown("""
            <style>
            body { background-color: white; color: black; }
            .sidebar .sidebar-content { background-color: #f8f9fa; }
            .stButton>button { background-color: #007bff; color: white; }
            .stTextInput>div>input { background-color: white; color: black; }
            </style>
        """, unsafe_allow_html=True)
    elif theme == "Dark":
        st.markdown("""
            <style>
            body { background-color: #2e2e2e; color: white; }
            .sidebar .sidebar-content { background-color: #333; }
            .stButton>button { background-color: #444; color: white; }
            .stTextInput>div>input { background-color: #555; color: white; }
            </style>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()