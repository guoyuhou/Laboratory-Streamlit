import streamlit as st  
import os  
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import sqlite3
from hashlib import sha256

def pages():  
    pages = {  
        '主页': 'main_page.py',  
        '网页设计': 'Web_Design.md',  
        'Fig_preservation': { 
            '项目信息': os.path.join('Fig_preservation', 'information.md'),  
            '实验设计': os.path.join('Fig_preservation', 'experi_design.md'),
            '实验日志': os.path.join('Fig_preservation', 'experi_log.md'),
            '更新日志': os.path.join('Fig_preservation', 'update_log.md'),
        }  
    }  
  
    page_name = st.sidebar.radio('导航', list(pages.keys()))  
    page_file = None  
  
    if page_name == '主页':  
        page_file = pages[page_name]  
        # 如果主页是 Python 脚本，你可能需要特别处理它  
        if page_file.endswith('.py'):  
            with open(page_file, encoding='utf-8') as file:  
                exec(file.read())  
    elif page_name == '网页设计' or page_name.startswith('Fig_preservation'):  
        page_file = pages[page_name] if not isinstance(pages[page_name], dict) else pages[page_name][st.sidebar.radio('分类', list(pages[page_name].keys()))]  
        if page_file.endswith('.md'):  
            with open(page_file, encoding='utf-8') as file:  
                md_content = file.read()  
                st.markdown(md_content)  
  
    if not page_file or (not page_file.endswith('.py') and not page_file.endswith('.md')):  
        st.write('所选页面不正确或文件类型不支持')  
  
pages()
'''
# Authenticator block
def Authenticator_block():  
    with open('config.yaml') as file:  
        config = yaml.load(file, Loader=SafeLoader)  

    authenticator = stauth.Authenticate(  
        config['credentials'],  
        config['cookie']['name'],  
        config['cookie']['key'],  
        config['cookie']['expiry_days'],  
        config['pre-authorized']  
    )  

    # Correct usage of location parameter
    name, authentication_status, username = authenticator.login('Login', 'main')

    if authentication_status:
        st.session_state['authentication_status'] = True
        st.session_state['name'] = name
        st.session_state['username'] = username
        st.write(f'Welcome *{name}*')
        st.title('个人中心')

        if authenticator.reset_password(username):
            st.success('Password modified successfully')
    elif authentication_status is False:
        st.session_state['authentication_status'] = False
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.session_state['authentication_status'] = None
        st.warning('Please enter your username and password')

    if authentication_status:
        # Correct usage of logout
        authenticator.logout('Logout', 'main')

Authenticator_block()
'''

import streamlit as st
import sqlite3
from hashlib import sha256

# 数据库连接
def get_db_connection():
    conn = sqlite3.connect('user_db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

# 创建数据库和表
def initialize_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL)''')
    conn.commit()
    conn.close()

initialize_db()

# 哈希密码
def hash_password(password):
    return sha256(password.encode()).hexdigest()

# 用户注册
def register_user(username, password, role):
    conn = get_db_connection()
    hashed_password = hash_password(password)
    try:
        conn.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                     (username, hashed_password, role))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error("Username already exists")
    finally:
        conn.close()

# 用户登录
def authenticate_user(username, password):
    conn = get_db_connection()
    hashed_password = hash_password(password)
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                        (username, hashed_password)).fetchone()
    conn.close()
    return user

# 获取用户角色
def get_user_role(username):
    conn = get_db_connection()
    user = conn.execute('SELECT role FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user['role'] if user else None

# 登录检查
def check_login():
    if 'username' not in st.session_state:
        st.session_state['username'] = None

# 主函数
def main():
    check_login()
    
    if st.session_state['username'] is None:
        st.title("Login Required")
        st.write("Please log in to access the app.")
        
        menu = ["Login", "Register"]
        choice = st.sidebar.selectbox("Select Activity", menu)
        
        if choice == "Register":
            st.subheader("Register")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            role = st.selectbox("Role", ["user", "admin"])
            if st.button("Register"):
                register_user(username, password, role)
                st.success("User registered successfully")
        
        elif choice == "Login":
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                user = authenticate_user(username, password)
                if user:
                    st.session_state['username'] = username
                    st.session_state['role'] = get_user_role(username)
                    st.success(f"Welcome {username}!")
                else:
                    st.error("Invalid username or password")
    
    else:
        st.title("Streamlit Authentication App")
        st.write(f"Logged in as {st.session_state['username']}.")
        
        menu = ["Home", "Reset Password"]
        choice = st.sidebar.selectbox("Select Activity", menu)
        
        if choice == "Home":
            st.subheader("Welcome to the app")
            st.write("You are now logged in. Please use the sidebar to navigate.")
            if st.session_state.get('role') == "admin":
                st.write("You have admin privileges.")
                # Add additional admin functionality here
        
        elif choice == "Reset Password":
            st.subheader("Reset Password")
            new_password = st.text_input("New Password", type="password")
            if st.button("Reset Password"):
                if new_password:
                    conn = get_db_connection()
                    hashed_password = hash_password(new_password)
                    conn.execute('UPDATE users SET password = ? WHERE username = ?', 
                                 (hashed_password, st.session_state['username']))
                    conn.commit()
                    conn.close()
                    st.success("Password reset successfully")
                else:
                    st.error("Please enter a new password")

if __name__ == "__main__":
    main()
