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

# GitHub API 设置
GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = st.secrets["oss"]["GITHUB_TOKEN"]
GITHUB_REPO = "guoyuhou/Laboratory-Streamlit"   

# 设置日志
logging.basicConfig(level=logging.INFO)

# 从配置文件加载用户
def load_users(file_path='users.json'):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"配置文件 {file_path} 不存在。")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 用户认证
class AuthManager:
    def __init__(self, users):
        self.users = users

    def authenticate_user(self, username, password):
        user = self.users.get(username)
        return user if user and user['password'] == password else None

    def get_user_projects(self, username):
        return self.users.get(username, {}).get('projects', [])

# 页面处理
class PageManager:
    def __init__(self, role, users, auth_manager):
        self.role = role
        self.users = users
        self.auth_manager = auth_manager
        self.public_pages = self.load_public_pages()
        self.protected_pages = self.load_protected_pages()

    def load_public_pages(self):
        return {
            '🏠 主页': 'main_page.py',
            '🖥️ 网页设计': 'Web_Design.md',
            '🛠️ 工具包': {
                '🧰 PyGWalker': os.path.join('工具包', 'PyGWalker.py'),
                '🔧 Storm Genie': os.path.join('工具包', 'Storm_Genie.py'),
                '📄 Papers': os.path.join('工具包', 'Papers.py')
            },
            '❓ 帮助': 'Help.py'
        }

    def load_protected_pages(self):
        return {
            '👤 个人中心': 'Personal_center.py',
            '☁️ 云服务': None,
            '📚 图示保存': {
                '🔍 项目信息': os.path.join('Fig_preservation', 'information.md'),
                '🧪 实验设计': os.path.join('Fig_preservation', 'experi_design.md'),
                '📝 实验日志': os.path.join('Fig_preservation', 'experi_log.md'),
                '🔄 更新日志': os.path.join('Fig_preservation', 'update_log.md'),
            },
            '📂 项目列表': None
        }

    def display_pages(self):
        pages = {**self.public_pages, **(self.protected_pages if st.session_state.get('username') else {})}
        page_name = st.sidebar.radio('导航', list(pages.keys()))

        if page_name == '📂 项目列表':
            self.display_user_projects(st.session_state['username'])
        else:
            self.load_page(pages, page_name)

    def load_page(self, pages, page_name):
        page_file = self.get_page_file(pages, page_name)
        if page_file:
            self.execute_file(page_file)

    def get_page_file(self, pages, page_name):
        if isinstance(pages[page_name], dict):
            category_name = st.sidebar.radio('分类', list(pages[page_name].keys()))
            return pages[page_name][category_name]
        return pages[page_name]

    def execute_file(self, file_path):
        try:
            if file_path.endswith('.py'):
                with open(file_path, encoding='utf-8') as file:
                    exec(file.read())
            elif file_path.endswith('.md'):
                self.display_markdown(file_path)
            else:
                st.write('所选页面不正确或文件类型不支持。')
        except Exception as e:
            st.error(f"文件处理错误: {e}")

    def display_user_projects(self, username):
        user_projects = self.auth_manager.get_user_projects(username)
        st.markdown("## 我的项目")
        if user_projects:
            selected_project = st.selectbox("选择项目查看", user_projects)
            if selected_project:
                self.display_project_files(selected_project)
        else:
            st.write("您还没有项目。")

        # 上传Markdown文件
        self.upload_markdown_file(selected_project)

    def upload_markdown_file(self, project_name):
        if project_name:
            st.markdown("### 上传Markdown文件")
            uploaded_file = st.file_uploader("上传Markdown文件", type=["md"])
            if uploaded_file is not None:
                # 读取文件内容
                file_content = uploaded_file.read().decode("utf-8")
                st.markdown("### 文件内容预览")
                st.markdown(file_content)

                # 保存文件
                if st.button("保存文件"):
                    project_folder = f'projects/{project_name}'
                    os.makedirs(project_folder, exist_ok=True)
                    file_path = os.path.join(project_folder, uploaded_file.name)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(file_content)
                    st.success(f"文件已保存到: {file_path}")

# Main Application
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
