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
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components

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
            padding-top: 2rem;
            padding-right: 2rem;
            padding-left: 2rem;
            padding-bottom: 2rem;
        }
        .stButton>button {
            background-color: #4a90e2;
            color: white;
            border-radius: 25px;
            padding: 0.75rem 1.5rem;
            font-weight: bold;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(50, 50, 93, 0.11), 0 1px 3px rgba(0, 0, 0, 0.08);
        }
        .stButton>button:hover {
            background-color: #357ae8;
            transform: translateY(-2px);
            box-shadow: 0 7px 14px rgba(50, 50, 93, 0.1), 0 3px 6px rgba(0, 0, 0, 0.08);
        }
        .stTextInput>div>div>input {
            border-radius: 20px;
            border: 2px solid #e0e0e0;
            padding: 10px 15px;
            transition: all 0.3s ease;
        }
        .stTextInput>div>div>input:focus {
            border-color: #4a90e2;
            box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
        }
        .sidebar .sidebar-content {
            background-color: #ffffff;
            box-shadow: 2px 0 5px rgba(0,0,0,0.1);
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
        .login-container {
            background-color: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(50, 50, 93, 0.11), 0 1px 3px rgba(0, 0, 0, 0.08);
            max-width: 400px;
            margin: auto;
        }
        .login-title {
            text-align: center;
            color: #333;
            font-size: 24px;
            margin-bottom: 1.5rem;
        }
        .login-input {
            margin-bottom: 1rem;
        }
        .login-checkbox {
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        .login-button {
            width: 100%;
        }
        .login-divider {
            margin: 1.5rem 0;
            text-align: center;
            position: relative;
        }
        .login-divider::before {
            content: "";
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            border-top: 1px solid #e0e0e0;
        }
        .login-divider span {
            background-color: white;
            padding: 0 10px;
            position: relative;
            color: #777;
        }
        .login-options {
            display: flex;
            justify-content: space-between;
            margin-top: 1rem;
        }
        .login-option {
            color: #4a90e2;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .login-option:hover {
            color: #357ae8;
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
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="login-title">欢迎登录</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #777;">请登录以访问更多精彩内容。</p>', unsafe_allow_html=True)
    
    # 添加Lottie动画
    lottie_url = "https://assets5.lottiefiles.com/packages/lf20_jcikwtux.json"
    st_lottie(lottie_url, height=200)
    
    username = st.text_input("用户名", placeholder="请输入用户名", key="username_input")
    password = st.text_input("密码", type="password", placeholder="请输入密码", key="password_input")
    
    remember_me = st.checkbox("记住我", key="remember_me")
    
    if st.button("登录", key="login_submit"):
        if username and password:
            user = auth_manager.authenticate_user(username, password)
            if user:
                st.balloons()
                st.success("登录成功！正在跳转...")
                st.session_state.update({'username': username, 'role': user['role'], 'login_page': False})
                
                # 添加成功登录的动画效果
                components.html(
                    """
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.7.1/gsap.min.js"></script>
                    <div id="success-animation" style="width: 100px; height: 100px; margin: auto;">
                        <svg viewBox="0 0 52 52">
                            <circle cx="26" cy="26" r="25" fill="none" stroke="#4CAF50" stroke-width="2"/>
                            <path fill="none" stroke="#4CAF50" stroke-width="2" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
                        </svg>
                    </div>
                    <script>
                        gsap.set("#success-animation", {scale: 0, opacity: 0});
                        gsap.to("#success-animation", {duration: 0.5, scale: 1, opacity: 1, ease: "back.out(1.7)"});
                        gsap.to("#success-animation circle", {duration: 0.6, strokeDasharray: 157, strokeDashoffset: 0, ease: "power2.out"});
                        gsap.to("#success-animation path", {duration: 0.6, strokeDasharray: 38, strokeDashoffset: 0, ease: "power2.out", delay: 0.3});
                    </script>
                    """,
                    height=150,
                )
            else:
                st.error("用户名或密码无效")
        else:
            st.warning("用户名和密码不能为空")

    st.markdown('<div class="login-divider"><span>或</span></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="login-option" onclick="alert(\'请联系管理员重置密码\')">忘记密码？</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="login-option" onclick="alert(\'请联系管理员创建新账号\')">没有账号？注册</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def handle_logout():
    st.session_state.update({'username': None, 'role': None, 'login_page': False})
    st.success("已退出登录")

if __name__ == "__main__":
    main()