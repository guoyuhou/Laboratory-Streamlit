import streamlit as st
from file_operations import edit_markdown, update_github_file
import os
from Cloud_storage import cloud_storage_page
import json
import folium
from streamlit_folium import folium_static

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
            '🏠 主页': self.home_page,
            '👥 团队': self.team_page,
            '🔬 项目': self.projects_page,
            '📚 论文': self.publications_page,
            '📞 联系我们': self.contact_page,
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
            '☁️ 云服务': cloud_storage_page,
            '📂 项目列表': self.display_user_projects,
            '📊 仪表板': self.dashboard
        }

    def display_pages(self):
        pages = {**self.public_pages, **(self.protected_pages if st.session_state.get('username') else {})}
        page_name = st.sidebar.radio('导航', list(pages.keys()))

        if callable(pages[page_name]):
            pages[page_name](st.session_state.get('username'))
        elif isinstance(pages[page_name], dict):
            category_name = st.sidebar.radio('分类', list(pages[page_name].keys()))
            self.execute_file(pages[page_name][category_name])
        else:
            self.execute_file(pages[page_name])

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

    def home_page(self, username):
        st.title("欢迎来到前沿实验室")
        st.write("我们致力于推动科技创新和前沿研究")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("研究方向")
            st.write("- 人工智能")
            st.write("- 量子计算")
            st.write("- 生物技术")
        with col2:
            st.subheader("最新动态")
            st.write("- 发表重要论文")
            st.write("- 获得重大科研项目")
            st.write("- 举办学术研讨会")
        with col3:
            st.subheader("合作伙伴")
            st.write("- 顶尖高校")
            st.write("- 知名企业")
            st.write("- 研究机构")

    def team_page(self, username):
        st.title("团队成员")
        
        members = [
            {"name": "张教授", "title": "实验室主任", "image": "Images/example1.jpg"},
            {"name": "李博士", "title": "高级研究员", "image": "Images/example2.jpg"},
            {"name": "王工程师", "title": "技术专家", "image": "Images/example3.jpg"},
        ]
        
        for member in members:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(member["image"], width=150)
            with col2:
                st.subheader(member["name"])
                st.write(member["title"])
                st.write("简介：...")  # 添加成员简介

    def projects_page(self, username):
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

    def publications_page(self, username):
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

    def contact_page(self, username):
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
