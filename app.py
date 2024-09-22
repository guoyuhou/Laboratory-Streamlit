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

def main():
    users = load_users()
    auth_manager = AuthManager(users)
    
    if 'username' not in st.session_state:
        st.session_state.update({'username': None, 'role': None, 'login_page': False, 'edit_content': ''})

    if st.session_state['username'] is None:
        if st.session_state['login_page']:
            handle_login(auth_manager)
        else:
            PageManager(None, users, auth_manager).display_pages()
            if st.sidebar.button("登录以访问更多内容"):
                st.session_state['login_page'] = True
    else:
        page_manager = PageManager(st.session_state['role'], users, auth_manager)
        page_manager.display_pages()

def handle_login(auth_manager):
    st.markdown("<h2 style='text-align: center;'>欢迎登录</h2>", unsafe_allow_html=True)
    st.write("请登录以访问更多内容。")

    # 用户名和密码输入框
    col1, col2 = st.columns([1, 1])
    with col1:
        username = st.text_input("用户名", placeholder="请输入用户名", key="username_input")
    with col2:
        password = st.text_input("密码", type="password", placeholder="请输入密码", key="password_input")

    # 登录按钮
    if st.button("登录", key="login_button", help="点击登录"):
        if username and password:
            user = auth_manager.authenticate_user(username, password)
            if user:
                st.session_state.update({'username': username, 'role': user['role'], 'login_page': False})
                st.success("登录成功！", icon="✅")
            else:
                st.error("用户名或密码无效")
        else:
            st.error("用户名和密码不能为空")

    # 添加一些样式
    st.markdown("""
        <style>
            .stButton button {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                cursor: pointer;
            }
            .stButton button:hover {
                background-color: #0056b3;
            }
            .css-1xarl7p {
                padding: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
