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

import streamlit as st
from auth_manager import AuthManager, load_users
from page_manager import PageManager

def main():
    users = load_users()
    auth_manager = AuthManager(users)
    if 'username' not in st.session_state:
        st.session_state.update({'username': None, 'role': None, 'login_page': False})

    if st.session_state['username'] is None:
        if st.session_state['login_page']:
            handle_login(auth_manager)
        else:
            st.title("欢迎来到实验室应用")
            PageManager(None, users, auth_manager).display_pages()
            if st.sidebar.button("登录以访问更多内容"):
                st.session_state['login_page'] = True
    else:
        st.title("欢迎回来")
        page_manager = PageManager(st.session_state['role'], users, auth_manager)
        page_manager.display_pages()

def handle_login(auth_manager):
    st.title("登录要求")
    st.write("请登录以访问更多内容。")
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")
    if st.button("登录"):
        if username and password:
            user = auth_manager.authenticate_user(username, password)
            if user:
                st.session_state.update({'username': username, 'role': user['role'], 'login_page': False})
            else:
                st.error("用户名或密码无效")
        else:
            st.error("用户名和密码不能为空")

if __name__ == "__main__":
    main()
