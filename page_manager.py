import streamlit as st
from file_operations import edit_markdown, update_github_file
import os
from Cloud_storage import cloud_storage_page
from main_page import main_page

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = st.secrets["oss"]["GITHUB_TOKEN"]
GITHUB_REPO = st.secrets["oss"]["GITHUB_REPO"] 

class PageManager:
    def __init__(self, role, users, auth_manager):
        self.role = role
        self.users = users
        self.auth_manager = auth_manager
        self.public_pages = self.load_public_pages()
        self.protected_pages = self.load_protected_pages()

    def load_public_pages(self):
        return {
            '🏠 主页': main_page,
            '👥 团队': self.team_page,
            '🔬 项目': lambda: self.projects_page(None),  # 修改这里
            '📚 论文': lambda: self.publications_page(None),  # 修改这里
            '📞 联系我们': self.contact_page,
        }

    def load_protected_pages(self):
        return {
            '👤 个人中心': 'Personal_center.py',
            '☁️ 云服务': lambda username: cloud_storage_page(username),
            '📂 项目列表': self.display_user_projects,
            '📊 仪表板': self.dashboard
        }

    def display_pages(self):
        st.sidebar.title("导航")
        
        # 显示公共页面
        page_name = st.sidebar.radio('公共页面', list(self.public_pages.keys()))
        
        # 如果用户已登录，显示受保护的页面
        if self.role:
            st.sidebar.title("用户功能")
            protected_page_name = st.sidebar.radio('用户功能', list(self.protected_pages.keys()))
            
            if protected_page_name:
                page_name = protected_page_name

        # 显示选中的页面
        if page_name in self.public_pages:
            self.public_pages[page_name]()  # 修改这里，调用函数而不是直接使用函数名
        elif page_name in self.protected_pages:
            if callable(self.protected_pages[page_name]):
                self.protected_pages[page_name](st.session_state.get('username'))
            else:
                self.execute_file(self.protected_pages[page_name])

    def team_page(self, username=None):
        st.title("团队成员")
        
        members = [
            {"name": "张教授", "title": "实验室主任", "image": "Images/example1.jpg"},]
    
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

    def projects_page(self, username=None):
        st.title("研究项目")
        
        projects = [
            {"name": "智能机器人", "description": "开发新一代智能机器人系统", "image": "Images/example1.jpg"},
            {"name": "量子通信", "description": "研究量子通信技术及其应用", "image": "Images/example2.jpg"},
            {"name": "基因编辑", "description": "探索CRISPR基因编辑技术", "image": "Images/example3.jpg"},
        ]
        
        for project in projects:
            with st.expander(project["name"]):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(project["image"], width=200)
                with col2:
                    st.write(project["description"])
                    st.write("项目进展：...")  # 添加项目进展

    def publications_page(self, username=None):
        st.title("发表论文")
        
        publications = [
            {"title": "人工智能在医疗诊断中的应用", "authors": "张三, 李四", "journal": "Nature", "year": 2023},
            {"title": "量子计算在密码学中的突破", "authors": "王五, 赵六", "journal": "Science", "year": 2022},
            {"title": "新型基因编辑技术的伦理考量", "authors": "刘七, 陈八", "journal": "Cell", "year": 2021},
        ]
        
        for pub in publications:
            st.write(f"**{pub['title']}**")
            st.write(f"作者：{pub['authors']}")
            st.write(f"发表于：{pub['journal']}, {pub['year']}")
            st.write("---")

    def contact_page(self, username=None):
        st.title("联系我们")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("联系方式")
            st.write("地址：XX市XX区XX路XX号")
            st.write("电话：123-456-7890")
            st.write("邮箱：contact@frontierlab.com")
        
        with col2:
            st.subheader("实验室位置")
            m = folium.Map(location=[31.2304, 121.4737], zoom_start=15)
            folium.Marker([31.2304, 121.4737], popup="前沿实验室").add_to(m)
            folium_static(m)

    def dashboard(self, username):
        st.title(f"欢迎回来，{username}！")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("最新通知")
            st.info("下周三将举行实验室会议")
            st.info("新的研究项目申请截止日期：2023年12月31日")
        
        with col2:
            st.subheader("个人任务")
            st.success("完成实验报告")
            st.warning("准备下周的演讲")

        st.subheader("实验室资源使用情况")
        resource_usage = {
            "计算集群": 75,
            "存储空间": 60,
            "实验设备": 40
        }
        for resource, usage in resource_usage.items():
            st.write(f"{resource}：")
            st.progress(usage)

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
        markdown_files = ["main_page.md", "experiment_design.md", "experiment_log.md", "papers.md"]
        
        st.sidebar.markdown("### 项目文件")
        selected_file = st.sidebar.radio("选择Markdown文件", markdown_files)
        if selected_file:
            file_path = os.path.join(project_folder, selected_file)
            self.display_markdown(file_path)

            # 直接显示编辑文本框和更新按钮
            content = edit_markdown(GITHUB_REPO, f'projects/{project_name}/{selected_file}')
            if content:
                new_content = st.text_area("编辑Markdown内容", value=content, height=300)
                if st.button("保存更改"):
                    with st.spinner("正在保存..."):
                        try:
                            update_success = update_github_file(GITHUB_REPO, f'projects/{project_name}/{selected_file}', new_content, "更新Markdown文件")
                            if update_success:
                                st.success("您的更新已成功提交！")
                            else:
                                st.error("更新失败，请检查您的输入或权限。")
                        except Exception as e:  
                            st.error(f"发生错误: {e}")
        else:
            st.error("项目文件夹不存在。")
