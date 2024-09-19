import streamlit as st
import json
import os
from Cloud_storage import cloud_storage_page

# Load users from configuration file
def load_users(file_path='users.json'):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"配置文件 {file_path} 不存在")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# User Authentication
class AuthManager:
    def __init__(self, users):
        self.users = users

    def authenticate_user(self, username, password):
        user = self.users.get(username)
        if user and user['password'] == password:
            return user
        return None

    def get_user_projects(self, username):
        user = self.users.get(username)
        if user:
            return user.get('projects', [])
        return []

# Page Handling
class PageManager:
    def __init__(self, role=None):
        self.role = role
        self.public_pages = {
            '🏠 主页': 'main_page.py',
            '🖥️ 网页设计': 'Web_Design.md',
            '🛠️ 工具包': {
                '🧰 PyGWalker': os.path.join('工具包', 'PyGWalker.py'),
                '🔧 Storm Genie': os.path.join('工具包', 'Storm_Genie.py'),
                '📄 Papers': os.path.join('工具包', 'Papers.py')
            },
            '❓ 帮助': 'Help.py'
        }
        self.protected_pages = {
            '👤 个人中心': 'Personal_center.py',
            '☁️ 云服务': None,
            '📚 Fig_preservation': {
                '🔍 项目信息': os.path.join('Fig_preservation', 'information.md'),
                '🧪 实验设计': os.path.join('Fig_preservation', 'experi_design.md'),
                '📝 实验日志': os.path.join('Fig_preservation', 'experi_log.md'),
                '🔄 更新日志': os.path.join('Fig_preservation', 'update_log.md'),
            }
        }

    def display_pages(self):
        pages = {**self.public_pages, **(self.protected_pages if st.session_state.get('username') else {})}
        page_name = st.sidebar.radio('导航', list(pages.keys()))

        if page_name == '☁️ 云服务':
            cloud_storage_page()  # Call cloud_storage_page function
        else:
            self.load_page(pages, page_name)

    def load_page(self, pages, page_name):
        if isinstance(pages[page_name], dict):
            category_name = st.sidebar.radio('分类', list(pages[page_name].keys()))
            page_file = pages[page_name][category_name]
        else:
            page_file = pages[page_name]

        if page_file:
            if page_file.endswith('.py'):
                self.execute_python_file(page_file)
            elif page_file.endswith('.md'):
                self.display_markdown(page_file)
            else:
                st.write('所选页面不正确或文件类型不支持')

    def execute_python_file(self, file_path):
        try:
            with open(file_path, encoding='utf-8') as file:
                exec(file.read())
        except Exception as e:
            st.error(f"文件执行错误: {e}")

    def display_markdown(self, file_path):
        try:
            with open(file_path, encoding='utf-8') as file:
                st.markdown(file.read())
        except Exception as e:
            st.error(f"文件读取错误: {e}")

    def display_user_projects(self, username, users):
        user = users.get(username)
        if user:
            st.markdown("## 项目列表")
            st.write("**我的项目:**")
            for project in user.get('projects', []):
                st.write(f"- {project}")

            st.write("**权限带来的项目:**")
            if user['role'] == '导师':
                for u in users.values():
                    if u['role'] in ['研究生', '本科生']:
                        for project in u['projects']:
                            st.write(f"- {project}")
            elif user['role'] == '研究生':
                for u in users.values():
                    if u['role'] == '本科生':
                        for project in u['projects']:
                            st.write(f"- {project}")

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
            PageManager().display_pages()
            if st.sidebar.button("登录以访问更多内容"):
                st.session_state['login_page'] = True
    else:
        st.title("欢迎回来")
        page_manager = PageManager(st.session_state['role'])
        page_manager.display_pages()
        page_manager.display_user_projects(st.session_state['username'], users)

def handle_login(auth_manager):
    st.title("登录要求")
    st.write("请登录以访问更多内容。")
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")
    if st.button("登录"):
        if username and password:
            user = auth_manager.authenticate_user(username, password)
            if user:
                st.session_state['username'] = username
                st.session_state['role'] = user['role']
                st.session_state['login_page'] = False
            else:
                st.error("用户名或密码无效")
        else:
            st.error("用户名和密码不能为空")

if __name__ == "__main__":
    main()
