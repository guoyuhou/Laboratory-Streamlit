import streamlit as st
import os
import pandas as pd
import sqlite3
from pygwalker.api.streamlit import StreamlitRenderer
from Cloud_storage import cloud_storage_page
from hashlib import sha256

def get_db_connection():
    conn = sqlite3.connect('user_db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL,
                        email TEXT,
                        phone TEXT)''')
    conn.commit()
    conn.close()

initialize_db()

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    conn = get_db_connection()
    hashed_password = hash_password(password)
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                        (username, hashed_password)).fetchone()
    conn.close()
    return user

def get_user_role(username):
    conn = get_db_connection()
    user = conn.execute('SELECT role FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user['role'] if user else None

def display_pages(role):
    pages = {
        '🏠 主页': 'main_page.py',
        '🖥️ 网页设计': 'Web_Design.md',
        '🛠️ 工具包': {
            'PyGWalker': os.path.join('工具包', 'PyGWalker.py'),
            'Storm Genie': os.path.join('工具包', 'Storm_Genie.py'),
            'Papers': os.path.join('工具包', 'Papers.py')
        },
        '👤 个人中心': 'Personal_center.py'
    }

    if role == '管理员':
        pages['📚 Fig_preservation'] = {
            '🔍 项目信息': os.path.join('Fig_preservation', 'information.md'),
            '🧪 实验设计': os.path.join('Fig_preservation', 'experi_design.md'),
            '📝 实验日志': os.path.join('Fig_preservation', 'experi_log.md'),
            '🔄 更新日志': os.path.join('Fig_preservation', 'update_log.md'),
        }

    page_name = st.sidebar.radio('导航', list(pages.keys()))
    if page_name == '☁️ 云服务' and role:
        cloud_storage_page()  # 调用 cloud_storage_page 函数
    else:
        page_file = pages[page_name] if not isinstance(pages[page_name], dict) else pages[page_name][st.sidebar.radio('分类', list(pages[page_name].keys()))]
        if page_file.endswith('.py'):
            try:
                with open(page_file, encoding='utf-8') as file:
                    exec(file.read())
            except Exception as e:
                st.error(f"文件执行错误: {e}")
        elif page_file.endswith('.md'):
            try:
                with open(page_file, encoding='utf-8') as file:
                    st.markdown(file.read())
            except Exception as e:
                st.error(f"文件读取错误: {e}")
        else:
            st.write('所选页面不正确或文件类型不支持')

def main():
    if 'username' not in st.session_state:
        st.session_state['username'] = None
        st.session_state['role'] = None
        st.session_state['login_page'] = False

    if st.session_state['username'] is None:
        if st.session_state['login_page']:
            st.title("登录要求")
            st.write("请登录以访问更多内容。")
            username = st.text_input("用户名")
            password = st.text_input("密码", type="password")
            if st.button("登录"):
                if username and password:
                    user = authenticate_user(username, password)
                    if user:
                        st.session_state['username'] = username
                        st.session_state['role'] = get_user_role(username)
                        st.session_state['login_page'] = False
                    else:
                        st.error("用户名或密码无效")
                else:
                    st.error("用户名和密码不能为空")
        else:
            st.title("欢迎来到实验室应用")
            display_pages(None)
            if st.sidebar.button("登录以访问更多内容"):
                st.session_state['login_page'] = True
                st.experimental_rerun()  # Ensure the login page is displayed
    else:
        st.title("欢迎回来")
        display_pages(st.session_state['role'])

        menu = ["🔒 重置密码", "🚪 退出"]
        choice = st.sidebar.selectbox("选择操作", menu)

        if choice == "🔒 重置密码":
            st.subheader("重置密码")
            new_password = st.text_input("新密码", type="password")
            if st.button("重置密码"):
                if new_password:
                    conn = get_db_connection()
                    hashed_password = hash_password(new_password)
                    conn.execute('UPDATE users SET password = ? WHERE username = ?',
                                 (hashed_password, st.session_state['username']))
                    conn.commit()
                    conn.close()
                    st.success("密码重置成功")
                else:
                    st.error("请输入新密码")
        elif choice == "🚪 退出":
            st.session_state['username'] = None
            st.session_state['role'] = None
            st.session_state['login_page'] = False
            st.success("您已成功登出。")
            st.write("正在重定向到主页...")
            st.experimental_rerun()  # Re-run to update state and redirect

if __name__ == "__main__":
    main()
