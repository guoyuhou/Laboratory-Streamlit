import streamlit as st
import os
import sqlite3
from hashlib import sha256
from Cloud_storage import cloud_storage_page

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
    # Pages accessible without login
    public_pages = {
        '🏠 主页': 'main_page.py',
        '🖥️ 网页设计': 'Web_Design.md',
        '🛠️ 工具包': {
            'PyGWalker': os.path.join('工具包', 'PyGWalker.py'),
            'Storm Genie': os.path.join('工具包', 'Storm_Genie.py'),
            'Papers': os.path.join('工具包', 'Papers.py')
        },
        '帮助': 'Help.py'
    }
    
    # Pages accessible with login
    protected_pages = {
        '👤 个人中心': 'Personal_center.py',
        '☁️ 云服务': None
    }
    
    if role == '管理员':
        protected_pages['📚 Fig_preservation'] = {
            '🔍 项目信息': os.path.join('Fig_preservation', 'information.md'),
            '🧪 实验设计': os.path.join('Fig_preservation', 'experi_design.md'),
            '📝 实验日志': os.path.join('Fig_preservation', 'experi_log.md'),
            '🔄 更新日志': os.path.join('Fig_preservation', 'update_log.md'),
        }

    # Combine public and protected pages based on login state
    pages = {**public_pages, **(protected_pages if st.session_state.get('username') else {})}
    
    page_name = st.sidebar.radio('导航', list(pages.keys()))
    
    if page_name == '☁️ 云服务':
        cloud_storage_page()  # Call cloud_storage_page function
    else:
        if role == '管理员' and page_name == '📚 Fig_preservation':
            category_name = st.sidebar.radio('分类', list(pages[page_name].keys()))
            page_file = pages[page_name][category_name]
        else:
            page_file = pages[page_name] if not isinstance(pages[page_name], dict) else pages[page_name][st.sidebar.radio('分类', list(pages[page_name].keys()))]
        
        if page_file:
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
                        st.experimental_rerun()  # Ensure the login page is properly updated
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

if __name__ == "__main__":
    main()
