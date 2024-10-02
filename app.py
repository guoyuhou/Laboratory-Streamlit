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
        background: linear-gradient(145deg, #f0f0f0, #ffffff);
        border-radius: 20px;
        box-shadow: 20px 20px 60px #d0d0d0, -20px -20px 60px #ffffff;
        padding: 30px;
        max-width: 400px;
        margin: 0 auto;
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .login-title {
        color: #0066cc;
        text-align: center;
        font-size: 2rem;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .login-input {
        width: 100%;
        padding: 10px;
        margin-bottom: 15px;
        border: none;
        border-radius: 5px;
        background-color: #f5f5f5;
        transition: all 0.3s ease;
    }
    
    .login-input:focus {
        outline: none;
        box-shadow: 0 0 0 2px #0066cc;
    }
    
    .login-button {
        width: 100%;
        padding: 10px;
        background-color: #0066cc;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .login-button:hover {
        background-color: #004499;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .login-options {
        display: flex;
        justify-content: space-between;
        margin-top: 20px;
    }
    
    .login-option {
        color: #0066cc;
        text-decoration: none;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }
    
    .login-option:hover {
        color: #004499;
        text-decoration: underline;
    }
    </style>
    
    <div class="login-container">
        <h1 class="login-title">欢迎登录</h1>
        <p style="text-align: center; margin-bottom: 20px;">请登录以访问更多精彩内容。</p>
        <input type="text" id="username" class="login-input" placeholder="请输入用户名">
        <input type="password" id="password" class="login-input" placeholder="请输入密码">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <input type="checkbox" id="remember-me" style="margin-right: 10px;">
            <label for="remember-me">记住我</label>
        </div>
        <button id="login-button" class="login-button">登录</button>
        <div class="login-options">
            <a href="#" class="login-option" id="forgot-password">忘记密码？</a>
            <a href="#" class="login-option" id="register">没有账号？注册</a>
        </div>
    </div>
    
    <script>
    const loginButton = document.getElementById('login-button');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const forgotPassword = document.getElementById('forgot-password');
    const register = document.getElementById('register');
    
    loginButton.addEventListener('click', () => {
        const username = usernameInput.value;
        const password = passwordInput.value;
        if (username && password) {
            loginButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 登录中...';
            loginButton.disabled = true;
            setTimeout(() => {
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: {username, password}}, '*');
            }, 1000);
        } else {
            alert('用户名和密码不能为空');
        }
    });
    
    forgotPassword.addEventListener('click', () => {
        alert('请联系管理员重置密码');
    });
    
    register.addEventListener('click', () => {
        alert('请联系管理员创建新账号');
    });
    </script>
    """, unsafe_allow_html=True)
    
    result = st.empty()
    
    if 'username' in st.session_state:
        username = st.session_state.username
        password = st.session_state.password
        user = auth_manager.authenticate_user(username, password)
        if user:
            result.success("登录成功！正在跳转...")
            st.balloons()
            st.session_state.update({'username': username, 'role': user['role'], 'login_page': False})
        else:
            result.error("用户名或密码无效")

def handle_logout():
    st.session_state.update({'username': None, 'role': None, 'login_page': False})
    st.success("已退出登录")

if __name__ == "__main__":
    main()