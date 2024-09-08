import streamlit as st
import os
import sqlite3
from hashlib import sha256
import oss2

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
        st.success("用户注册成功")
    except sqlite3.IntegrityError:
        st.error("用户名已存在")
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

# 页面内容
def display_pages():
    pages = {
        '主页': 'main_page.py',
        '网页设计': 'Web_Design.md',
        '云服务': 'Cloud_storage.py',
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

# 云服务模块
# 从Streamlit的Secrets中读取OSS的密钥和存储桶信息
ACCESS_KEY_ID = st.secrets["oss"]["ACCESS_KEY_ID"]
ACCESS_KEY_SECRET = st.secrets["oss"]["ACCESS_KEY_SECRET"]
ENDPOINT = st.secrets["oss"]["ENDPOINT"]
BUCKET_NAME = st.secrets["oss"]["BUCKET_NAME"]

# 创建OSS认证和存储桶对象
auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, ENDPOINT, BUCKET_NAME)

def list_files():
    return [obj.key for obj in oss2.ObjectIterator(bucket)]

def upload_file():
    st.subheader('上传文件')
    uploaded_file = st.file_uploader("选择要上传的文件")
    if uploaded_file:
        bucket.put_object(uploaded_file.name, uploaded_file)
        st.success(f'文件 {uploaded_file.name} 上传成功')

def download_file():
    st.subheader('下载文件')
    files = list_files()
    file_name = st.selectbox('选择要下载的文件', files)
    if file_name and st.button('下载'):
        obj = bucket.get_object(file_name)
        st.download_button(
            label='下载文件',
            data=obj.read(),
            file_name=file_name,
            mime='application/octet-stream'
        )


# 主函数
def main():
    if 'username' not in st.session_state:
        st.session_state['username'] = None

    if st.session_state['username'] is None:
        st.title("登录要求")
        st.write("请登录以访问应用程序。")

        menu = ["登录", "注册"]
        choice = st.sidebar.selectbox("选择操作", menu)

        if choice == "注册":
            st.subheader("注册")
            username = st.text_input("用户名")
            password = st.text_input("密码", type="password")
            role = st.selectbox("角色", ["用户", "管理员"])
            if st.button("注册"):
                register_user(username, password, role)
        
        elif choice == "登录":
            st.subheader("登录")
            username = st.text_input("用户名")
            password = st.text_input("密码", type="password")
            if st.button("登录"):
                user = authenticate_user(username, password)
                if user:
                    st.session_state['username'] = username
                    st.session_state['role'] = get_user_role(username)
                    st.success(f"欢迎回来, {username}!")
                else:
                    st.error("用户名或密码无效")
    else:
        menu = ["主页", "重置密码", "退出"]
        choice = st.sidebar.selectbox("选择操作", menu)

        if choice == "主页":
            display_pages()  # 登录后才显示页面
        elif choice == "重置密码":
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
        elif choice == "登出":
            st.session_state['username'] = None
            st.session_state['role'] = None
            st.success("您已成功登出。")
            # 通过刷新应用程序重定向到登录页面，但不使用 st.experimental_rerun()
            st.write("正在重定向到登录页面...")
            st.stop()  # 停止进一步执行并重新渲染页面

if __name__ == "__main__":
    main()
