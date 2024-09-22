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

# 定义主题选项
THEMES = {
    "默认": {
        "background_color": "#f4f4f4",
        "text_color": "#333",
        "sidebar_color": "#001f3f",
        "button_color": "#007bff",
        "button_hover_color": "#0056b3"
    },
    "暗黑": {
        "background_color": "#1e1e1e",
        "text_color": "#f4f4f4",
        "sidebar_color": "#2b2b2b",
        "button_color": "#4a90e2",
        "button_hover_color": "#357ab7"
    },
    "明亮": {
        "background_color": "#ffffff",
        "text_color": "#000000",
        "sidebar_color": "#e1e1e1",
        "button_color": "#28a745",
        "button_hover_color": "#218838"
    }
}

def apply_theme(theme):
    """应用用户选择的主题"""
    st.markdown(f"""
    <style>
        body {{
            background-color: {theme['background_color']};
            color: {theme['text_color']};
            font-family: 'Arial', sans-serif;
        }}
        .sidebar .sidebar-content {{
            background-color: {theme['sidebar_color']};
            color: {theme['text_color']};
        }}
        .stButton button {{
            background-color: {theme['button_color']};
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 15px;
            cursor: pointer;
        }}
        .stButton button:hover {{
            background-color: {theme['button_hover_color']};
        }}
    </style>
    """, unsafe_allow_html=True)

def main():
    users = load_users()
    auth_manager = AuthManager(users)
    
    if 'username' not in st.session_state:
        st.session_state.update({'username': None, 'role': None, 'login_page': False, 'edit_content': ''})

    # 主题选择
    selected_theme = st.sidebar.selectbox("选择主题", list(THEMES.keys()))
    apply_theme(THEMES[selected_theme])

    if st.session_state['username'] is None:
        if st.session_state['login_page']:
            handle_login(auth_manager)
        else:
            st.title("欢迎来到实验室应用")
            PageManager(None, users, auth_manager).display_pages()
            if st.sidebar.button("登录以访问更多内容"):
                st.session_state['login_page'] = True
    else:
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
