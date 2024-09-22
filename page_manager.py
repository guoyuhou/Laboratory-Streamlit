import streamlit as st
from file_manager import edit_markdown, update_github_file
import os
from Cloud_storage import cloud_storage_page

class PageManager:
    def __init__(self, role, users, auth_manager):
        self.role = role
        self.users = users
        self.auth_manager = auth_manager
        self.github_repo = "your_github_repo"  # 请替换为实际的 GitHub 仓库
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
                st.write('所选页面不正确或文件类型不支持。')
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
        if not os.path.exists(project_folder):
            st.error("项目文件夹不存在。")
            return
        
        markdown_files = ["main_page.md", "experiment_design.md", "experiment_log.md", "papers.md"]
        st.sidebar.markdown("### 项目文件")
        selected_file = st.sidebar.radio("选择Markdown文件", markdown_files)

        if selected_file:
            file_path = os.path.join(project_folder, selected_file)
            self.display_markdown(file_path)

            if st.button("编辑该文件"):
                content = edit_markdown(self.github_repo, f'projects/{project_name}/{selected_file}')
                if content:
                    st.session_state['edit_content'] = content

                    new_content = st.text_area("编辑Markdown内容", value=st.session_state['edit_content'], height=300)

                    if st.button("保存更改"):
                        with st.spinner("正在保存..."):
                            try:
                                update_success = update_github_file(self.github_repo, f'projects/{project_name}/{selected_file}', new_content, "更新Markdown文件")
                                if update_success:
                                    st.success("您的更新已成功提交！")
                                    st.session_state['edit_content'] = new_content  # 更新内容
                                else:
                                    st.error("更新失败，请检查您的输入或权限。")
                            except Exception as e:
                                st.error(f"发生错误: {e}")
