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
        initial_sidebar_state="expanded"  # 设置侧边栏初始状态为展开
    )

    # 使用自定义CSS美化界面
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(to right, #f6f9fc, #e9f1f7);
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
        }
        .stTextInput>div>div>input {
            border-radius: 5px;
        }
        </style>
        """, unsafe_allow_html=True)

    # 使用列布局使logo居中
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image('Images/sdu_logo2.jpg', width=300)

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
        page_manager = PageManager(st.session_state['role'], users, auth_manager)
        page_manager.display_pages()

    # 美化侧边栏内容
    with st.sidebar:
        st.markdown("---")
        st.markdown(
            '<h6 style="text-align: center;">Made with ❤️ using <img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16"> by @Diary</h6>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="display: flex; justify-content: center; margin-top: 0.75em;"><a href="https://moderny-alexander.streamlit.app/" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a></div>',
            unsafe_allow_html=True,
        )

def handle_login(auth_manager):
    st.title("欢迎登录")
    st.write("请登录以访问更多精彩内容。")
    
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("用户名", placeholder="请输入用户名", key="username_input")
    with col2:
        password = st.text_input("密码", type="password", placeholder="请输入密码", key="password_input")
    
    col3, col4, col5 = st.columns([1,1,2])
    with col3:
        remember_me = st.checkbox("记住我")
    with col4:
        if st.button("登录", key="login_submit"):
            if username and password:
                user = auth_manager.authenticate_user(username, password)
                if user:
                    st.balloons()
                    st.success("登录成功！")
                    st.session_state.update({'username': username, 'role': user['role'], 'login_page': False})
                else:
                    st.error("用户名或密码无效")
            else:
                st.warning("用户名和密码不能为空")

    st.markdown("---")
    col6, col7 = st.columns(2)
    with col6:
        st.markdown("[忘记密码？](#)", help="点击此处重置密码")
    with col7:
        st.markdown("[没有账号？注册](#)", help="点击此处创建新账号")

if __name__ == "__main__":
    main()
