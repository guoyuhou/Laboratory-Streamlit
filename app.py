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
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    .login-container {
        font-family: 'Roboto', sans-serif;
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        -webkit-backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .login-title {
        color: #2c3e50;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .login-input {
        width: 100%;
        padding: 0.75rem;
        margin-bottom: 1rem;
        border: none;
        border-radius: 5px;
        background-color: rgba(255, 255, 255, 0.8);
        transition: all 0.3s ease;
    }
    
    .login-input:focus {
        outline: none;
        box-shadow: 0 0 0 2px #3498db;
    }
    
    .login-button {
        width: 100%;
        padding: 0.75rem;
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 1rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .login-button:hover {
        background-color: #2980b9;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .login-options {
        display: flex;
        justify-content: space-between;
        margin-top: 1rem;
    }
    
    .login-option {
        color: #34495e;
        text-decoration: none;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }
    
    .login-option:hover {
        color: #3498db;
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-container">
        <h1 class="login-title">欢迎登录</h1>
        <p style="text-align: center; color: #7f8c8d;">请登录以访问更多精彩内容</p>
    </div>
    """, unsafe_allow_html=True)
    
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
                
                # 添加登录成功动画
                st.markdown("""
                <style>
                @keyframes successAnimation {
                    0% { transform: scale(1); }
                    50% { transform: scale(1.1); }
                    100% { transform: scale(1); }
                }
                .success-message {
                    animation: successAnimation 0.5s ease-in-out;
                }
                </style>
                <div class="success-message">
                    <h2 style="text-align: center; color: #27ae60;">登录成功！</h2>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("用户名或密码无效")
        else:
            st.warning("用户名和密码不能为空")

    st.markdown("""
    <div class="login-options">
        <a href="#" class="login-option" onclick="showResetPassword()">忘记密码？</a>
        <a href="#" class="login-option" onclick="showRegister()">没有账号？注册</a>
    </div>
    
    <script>
    function showResetPassword() {
        alert("请联系管理员重置密码");
    }
    
    function showRegister() {
        alert("请联系管理员创建新账号");
    }
    </script>
    """, unsafe_allow_html=True)

def handle_logout():
    st.session_state.update({'username': None, 'role': None, 'login_page': False})
    st.success("已退出登录")
    
    # 添加退出登录动画
    st.markdown("""
    <style>
    @keyframes logoutAnimation {
        0% { opacity: 1; transform: translateY(0); }
        100% { opacity: 0; transform: translateY(-20px); }
    }
    .logout-message {
        animation: logoutAnimation 0.5s ease-in-out forwards;
    }
    </style>
    <div class="logout-message">
        <h2 style="text-align: center; color: #3498db;">已安全退出登录</h2>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()