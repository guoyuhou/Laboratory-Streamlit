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
            padding: 40px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 10px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            animation: fadeIn 0.5s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .login-title {
            color: #2c3e50;
            font-size: 28px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 30px;
        }
        
        .login-input {
            width: 100%;
            padding: 12px;
            margin-bottom: 20px;
            border: none;
            border-radius: 5px;
            background-color: rgba(255,255,255,0.8);
            transition: all 0.3s ease;
        }
        
        .login-input:focus {
            outline: none;
            box-shadow: 0 0 0 2px #3498db;
        }
        
        .login-button {
            width: 100%;
            padding: 12px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .login-button:hover {
            background-color: #2980b9;
        }
        
        .login-options {
            display: flex;
            justify-content: space-between;
            margin-top: 20px;
        }
        
        .login-option {
            color: #3498db;
            text-decoration: none;
            font-size: 14px;
            transition: all 0.3s ease;
        }
        
        .login-option:hover {
            color: #2980b9;
        }
        </style>
        
        <script>
        function animateLogin() {
            const inputs = document.querySelectorAll('.login-input');
            inputs.forEach((input, index) => {
                setTimeout(() => {
                    input.style.opacity = 1;
                    input.style.transform = 'translateY(0)';
                }, index * 100);
            });
        }
        
        document.addEventListener('DOMContentLoaded', animateLogin);
        </script>
        
        <div class="login-container">
            <h2 class="login-title">欢迎登录</h2>
            <input type="text" class="login-input" id="username" placeholder="请输入用户名" style="opacity: 0; transform: translateY(-20px);">
            <input type="password" class="login-input" id="password" placeholder="请输入密码" style="opacity: 0; transform: translateY(-20px);">
            <button class="login-button" onclick="handleLogin()">登录</button>
            <div class="login-options">
                <a href="#" class="login-option" onclick="forgotPassword()">忘记密码？</a>
                <a href="#" class="login-option" onclick="register()">没有账号？注册</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Streamlit 组件用于获取输入值
        username = st.empty()
        password = st.empty()
        remember_me = st.checkbox("记住我", key="remember_me")

        if st.button("登录", key="login_submit", style="display:none;"):
            username_value = username.text_input("", key="username_input")
            password_value = password.text_input("", type="password", key="password_input")
            if username_value and password_value:
                user = auth_manager.authenticate_user(username_value, password_value)
                if user:
                    st.balloons()
                    st.success("登录成功！正在跳转...")
                    st.session_state.update({'username': username_value, 'role': user['role'], 'login_page': False})
                else:
                    st.error("用户名或密码无效")
            else:
                st.warning("用户名和密码不能为空")

        st.markdown("""
        <script>
        function handleLogin() {
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            if (username && password) {
                document.querySelector('.stButton button').click();
            } else {
                alert('用户名和密码不能为空');
            }
        }

        function forgotPassword() {
            alert('请联系管理员重置密码');
        }

        function register() {
            alert('请联系管理员创建新账号');
        }
        </script>
        """, unsafe_allow_html=True)

def handle_logout():
    st.session_state.update({'username': None, 'role': None, 'login_page': False})
    st.success("已退出登录")
    st.markdown("""
    <style>
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
    .logout-message {
        animation: fadeOut 2s ease-out forwards;
    }
    </style>
    <div class="logout-message">
        <h3>感谢使用，再见！</h3>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()