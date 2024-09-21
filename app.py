import streamlit as st
import json
import os
from Cloud_storage import cloud_storage_page
import pygwalker
import pandas as pd
from pygwalker.api.streamlit import StreamlitRenderer
import requests

# Load users from configuration file
def load_users(file_path='users.json'):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"配置文件 {file_path} 不存在")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Update Markdown file on GitHub
def update_markdown_file(file_path, content):
    url = f"https://api.github.com/repos/{st.secrets['github']['GITHUB_REPO']}/contents/{file_path}"
    
    # Get file info to get SHA
    response = requests.get(url, headers={"Authorization": f"token {st.secrets['github']['GITHUB_TOKEN']}"})
    if response.status_code != 200:
        st.error("无法获取文件信息，请检查文件路径或权限。")
        return
    
    file_info = response.json()
    sha = file_info['sha']

    # Submit update
    data = {
        "message": "Update Markdown file from Streamlit app",
        "content": content.encode("utf-8").decode("utf-8"),  # Base64 encoding
        "sha": sha
    }
    
    response = requests.put(url, json=data, headers={"Authorization": f"token {st.secrets['github']['GITHUB_TOKEN']}"})
    if response.status_code == 200:
        st.success("文件更新成功！")
    else:
        st.error("文件更新失败，请检查错误信息。")

# User Authentication
class AuthManager:
    def __init__(self, users):
        self.users = users

    def authenticate_user(self, username, password):
        user = self.users.get(username)
        return user if user and user['password'] == password else None

    def get_user_projects(self, username):
        return self.users.get(username, {}).get('projects', [])

# Page Handling
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
            '📚 Fig_preservation': {
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

        if page_name == '☁️ 云服务':
            cloud_storage_page()
        elif page_name == '📂 项目列表':
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
                st.write('所选页面不正确或文件类型不支持')
        except Exception as e:
            st.error(f"文件处理错误: {e}")

    def display_markdown(self, file_path):
        try:
            with open(file_path, encoding='utf-8') as file:
                st.markdown(file.read())
        except Exception as e:
            st.error(f"文件读取错误: {e}")

    def display_user_projects(self, username):
        user_projects = self.auth_manager.get_user_projects(username)
        st.markdown("## 我的项目")
        if user_projects:
            selected_project = st.selectbox("选择项目查看", user_projects)
            if selected_project:
                self.display_project_files(selected_project)
        else:
            st.write("您还没有项目。")

        # 对于本科生，不显示可访问的项目
        if self.users[username]['role'] != '本科生':
            self.display_permission_based_projects(username)

    def display_permission_based_projects(self, username):
        user = self.users.get(username)
        accessible_projects = self.get_accessible_projects(user, username)
        if accessible_projects:
            selected_project = st.selectbox("选择可访问的项目", accessible_projects, key="accessible_projects")
            if selected_project:
                project_name = selected_project.split(": ")[1]
                self.display_project_files(project_name)
        else:
            st.write("您没有可访问的项目。")

    def get_accessible_projects(self, user, username):
        if not user:
            return []
        
        accessible_projects = []
        if user['role'] == '导师':
            for u, data in self.users.items():
                if data['role'] in ['研究生', '本科生']:
                    accessible_projects.extend(f"{u}: {project}" for project in data.get('projects', []))
        elif user['role'] == '研究生':
            for u, data in self.users.items():
                if data['role'] == '本科生':
                    accessible_projects.extend(f"{u}: {project}" for project in data.get('projects', []))
        else:
            accessible_projects.extend(f"{username}: {project}" for project in user.get('projects', []))
        
        return accessible_projects

    def display_project_files(self, project_name):
        project_folder = f'projects/{project_name}'
        if os.path.exists(project_folder):
            st.sidebar.markdown("### 项目文件")
            if st.sidebar.button("主页", key=f"main_page_{project_name}"):
                self.display_markdown(os.path.join(project_folder, 'main_page.md'))
            if st.sidebar.button("实验设计", key=f"experiment_design_{project_name}"):
                self.display_markdown(os.path.join(project_folder, 'experiment_design.md'))
            if st.sidebar.button("实验日志", key=f"experiment_log_{project_name}"):
                self.display_markdown(os.path.join(project_folder, 'experiment_log.md'))
            if st.sidebar.button("论文", key=f"papers_{project_name}"):
                self.display_markdown(os.path.join(project_folder, 'papers.md'))
        else:
            st.error("项目文件夹不存在。")


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
