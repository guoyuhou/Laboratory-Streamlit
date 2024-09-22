import streamlit as st
import json
import os
import random
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
    st.title("登录要求")
    st.write("请登录以访问更多内容。")
    
    # 用户名输入
    username = st.text_input("用户名", placeholder="请输入用户名", key="username_input")
    
    # 密码输入
    password = st.text_input("密码", type="password", placeholder="请输入密码", key="password_input")
    
    # 验证码
    captcha = generate_captcha()
    st.image(captcha['image'], caption='验证码', use_column_width=True)
    captcha_input = st.text_input("输入验证码", placeholder="请输入验证码")
    
    # 记住我选项
    remember_me = st.checkbox("记住我")

    # 登录按钮
    if st.button("登录"):
        if username and password:
            if captcha_input.lower() == captcha['text']:
                user = auth_manager.authenticate_user(username, password)
                if user:
                    st.session_state.update({'username': username, 'role': user['role'], 'login_page': False})
                else:
                    st.error("用户名或密码无效")
            else:
                st.error("验证码错误")
        else:
            st.error("用户名和密码不能为空")

    # 忘记密码和注册链接
    st.write("[忘记密码？](#)")
    st.write("[没有账号？注册](#)")

def generate_captcha():
    """生成随机验证码和图像"""
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    import io

    text = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5))
    image = Image.new('RGB', (100, 40), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # 使用默认字体
    draw.text((10, 5), text, fill=(0, 0, 0))
    
    # 转换为字节流
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return {'text': text, 'image': img_byte_arr.getvalue()}

if __name__ == "__main__":
    main()
