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
    # CSS 样式
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: auto;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .login-title {
        text-align: center;
        color: #2c3e50;
        font-size: 24px;
        margin-bottom: 20px;
    }
    .stTextInput > div > div > input {
        background-color: #fff;
        border: 1px solid #bdc3c7;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
    }
    .stButton > button {
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #2980b9;
    }
    .forgot-register {
        display: flex;
        justify-content: space-between;
        margin-top: 20px;
    }
    .forgot-register button {
        background: none;
        border: none;
        color: #3498db;
        cursor: pointer;
        font-size: 14px;
    }
    .forgot-register button:hover {
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)

    # JavaScript 动画
    st.markdown("""
    <script>
    document.addEventListener('DOMContentLoaded', (event) => {
        const loginContainer = document.querySelector('.login-container');
        loginContainer.style.opacity = '0';
        loginContainer.style.transform = 'translateY(-20px)';
        setTimeout(() => {
            loginContainer.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            loginContainer.style.opacity = '1';
            loginContainer.style.transform = 'translateY(0)';
        }, 100);
    });
    </script>
    """, unsafe_allow_html=True)

    # 登录表单
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="login-title">欢迎登录</h2>', unsafe_allow_html=True)
        
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

        st.markdown('<div class="forgot-register">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("忘记密码？"):
                st.info("请联系管理员重置密码")
        with col2:
            if st.button("没有账号？注册"):
                st.info("请联系管理员创建新账号")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def handle_logout():
    st.session_state.update({'username': None, 'role': None, 'login_page': False})
    st.success("已退出登录")

if __name__ == "__main__":
    main()