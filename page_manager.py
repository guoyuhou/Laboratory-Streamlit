import streamlit as st
from file_operations import edit_markdown, update_github_file
import os
from Cloud_storage import cloud_storage_page
from main_page import main_page
import Personal_center
import folium
from streamlit_folium import folium_static
import json

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
            '🔬 项目': lambda: self.projects_page(None),  
            '📚 论文': lambda: self.publications_page(None),  
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
        
        # 创建一个包含所有页面的字典
        all_pages = self.public_pages.copy()
        
        # 如果用户已登录，添加受保护的页面
        if self.role:
            all_pages.update(self.protected_pages)
        
        # 使用单个radio按钮显示所有可用页面
        page_name = st.sidebar.radio('选择页面', list(all_pages.keys()))
        
        # 显示选中的页面
        if page_name in self.public_pages:
            self.public_pages[page_name]()
        elif page_name in self.protected_pages:
            if callable(self.protected_pages[page_name]):
                self.protected_pages[page_name](st.session_state.get('username'))
            else:
                self.execute_file(self.protected_pages[page_name])

    def team_page(self, username=None):
        st.title("研究团队")
        
        # 团队介绍
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f0f8ff, #e6f3ff); padding: 30px; border-radius: 15px; margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.1);">
            <h2 style="color: #003366; font-size: 2.5em; margin-bottom: 20px; text-shadow: 1px 1px 2px #aaa;">团队愿景</h2>
            <p style="font-size: 18px; line-height: 1.8; color: #333;">
            在浩瀚无垠的海洋中探索未知，我们是海洋科学的先锋。我们的团队由充满激情的科研精英组成，致力于揭示海洋的奥秘，保护海洋生态，推动可持续发展。
            我们不仅是研究者，更是海洋的守护者。通过跨学科合作，创新技术应用，我们正在重新定义海洋科学的边界。
            加入我们，与海洋共呼吸，让科学之光照亮深海的每一个角落。
            </p>
        </div>
        """, unsafe_allow_html=True)

        # 团队成员数据
        members = [
            {"name": "陈浩", "title": "实验室主任", "image": "https://images.unsplash.com/photo-1557862921-37829c790f19?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1171&q=80", "description": "海洋生态学教授，专注于海洋生物多样性研究", "quote": "海洋是地球的生命之源，我们的使命是守护这片蓝色家园。"},
            {"name": "李明", "title": "副教授", "image": "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80", "description": "海洋化学专家，研究海洋污染物的迁移转化", "quote": "每一滴水都讲述着海洋的故事，我们要倾听并理解它们。"},
            {"name": "王芳", "title": "博士后", "image": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1169&q=80", "description": "海洋微生物学研究者，探索深海极端环境微生物", "quote": "在最极端的环境中，生命总能找到方式绽放。"},
            {"name": "张伟", "title": "博士生", "image": "https://images.unsplash.com/photo-1607990281513-2c110a25bd8c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1234&q=80", "description": "海洋地质学方向，研究海底地貌演变", "quote": "海底的每一寸变化都是地球历史的见证。"},
        ]
        
        # 使用高级卡片布局展示团队成员
        st.markdown("<h2 style='text-align: center; color: #003366; font-size: 2.5em; margin: 40px 0; text-shadow: 2px 2px 4px #aaa;'>核心成员</h2>", unsafe_allow_html=True)
        cols = st.columns(2)  # 每行显示2个成员
        for i, member in enumerate(members):
            with cols[i % 2]:
                st.markdown(f"""
                <div style="background: linear-gradient(45deg, #ffffff, #f0f8ff); padding: 30px; border-radius: 15px; box-shadow: 0 15px 30px rgba(0,0,0,0.1); margin-bottom: 30px; transition: all 0.3s ease;">
                    <img src="{member['image']}" style="width: 200px; height: 200px; object-fit: cover; border-radius: 50%; display: block; margin: 0 auto; border: 5px solid #fff; box-shadow: 0 0 20px rgba(0,0,0,0.2);">
                    <h3 style="text-align: center; color: #003366; margin-top: 20px; font-size: 1.8em;">{member['name']}</h3>
                    <p style="text-align: center; font-weight: bold; color: #0066cc; font-size: 1.2em;">{member['title']}</p>
                    <p style="text-align: center; color: #333; font-size: 1em; margin: 15px 0;">{member['description']}</p>
                    <blockquote style="font-style: italic; color: #666; border-left: 4px solid #0066cc; padding-left: 15px; margin: 20px 0;">
                        "{member['quote']}"
                    </blockquote>
                </div>
                """, unsafe_allow_html=True)

        # 团队成就
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e6f3ff, #ccebff); padding: 30px; border-radius: 15px; margin-top: 40px; box-shadow: 0 15px 30px rgba(0,0,0,0.1);">
            <h2 style="color: #003366; font-size: 2.5em; margin-bottom: 30px; text-align: center; text-shadow: 2px 2px 4px #aaa;">团队里程碑</h2>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
                <div style="text-align: center; margin: 20px; flex: 1;">
                    <i class="fas fa-trophy" style="font-size: 3em; color: #ffd700;"></i>
                    <h3 style="color: #0066cc; margin-top: 15px;">国家自然科学基金重点项目</h3>
                    <p>连续三年获得支持，总经费超过1000万元</p>
                </div>
                <div style="text-align: center; margin: 20px; flex: 1;">
                    <i class="fas fa-book" style="font-size: 3em; color: #4caf50;"></i>
                    <h3 style="color: #0066cc; margin-top: 15px;">顶级期刊发表</h3>
                    <p>在Nature、Science等期刊发表20余篇研究论文</p>
                </div>
                <div style="text-align: center; margin: 20px; flex: 1;">
                    <i class="fas fa-medal" style="font-size: 3em; color: #ff9800;"></i>
                    <h3 style="color: #0066cc; margin-top: 15px;">国际会议最佳论文奖</h3>
                    <p>连续5年获得海洋科学领域国际会议最佳论文奖</p>
                </div>
                <div style="text-align: center; margin: 20px; flex: 1;">
                    <i class="fas fa-microscope" style="font-size: 3em; color: #9c27b0;"></i>
                    <h3 style="color: #0066cc; margin-top: 15px;">技术应用</h3>
                    <p>开发的海洋环境监测技术已在20个沿海城市成功应用</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 合作伙伴
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f0f8ff, #e6f3ff); padding: 30px; border-radius: 15px; margin-top: 40px; box-shadow: 0 15px 30px rgba(0,0,0,0.1);">
            <h2 style="color: #003366; font-size: 2.5em; margin-bottom: 30px; text-align: center; text-shadow: 2px 2px 4px #aaa;">全球合作网络</h2>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
                <div style="text-align: center; margin: 20px;">
                    <img src="https://images.unsplash.com/photo-1541339907198-e08756dedf3f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80" style="width: 150px; height: 150px; object-fit: cover; border-radius: 50%; box-shadow: 0 10px 20px rgba(0,0,0,0.1);">
                    <p style="margin-top: 15px; font-weight: bold; color: #0066cc;">中国海洋大学</p>
                </div>
                <div style="text-align: center; margin: 20px;">
                    <img src="https://images.unsplash.com/photo-1527100673774-cce25eafaf7f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80" style="width: 150px; height: 150px; object-fit: cover; border-radius: 50%; box-shadow: 0 10px 20px rgba(0,0,0,0.1);">
                    <p style="margin-top: 15px; font-weight: bold; color: #0066cc;">国家海洋局第一海洋研究所</p>
                </div>
                <div style="text-align: center; margin: 20px;">
                    <img src="https://images.unsplash.com/photo-1472214103451-9374bd1c798e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80" style="width: 150px; height: 150px; object-fit: cover; border-radius: 50%; box-shadow: 0 10px 20px rgba(0,0,0,0.1);">
                    <p style="margin-top: 15px; font-weight: bold; color: #0066cc;">美国伍兹霍尔海洋研究所</p>
                </div>
                <div style="text-align: center; margin: 20px;">
                    <img src="https://images.unsplash.com/photo-1484291470158-b8f8d608850d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80" style="width: 150px; height: 150px; object-fit: cover; border-radius: 50%; box-shadow: 0 10px 20px rgba(0,0,0,0.1);">
                    <p style="margin-top: 15px; font-weight: bold; color: #0066cc;">日本东京大学大气与海洋研究所</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 加入我们
        st.markdown("""
        <div style="background: linear-gradient(135deg, #003366, #0066cc); padding: 40px; border-radius: 15px; margin-top: 40px; text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.2);">
            <h2 style="color: #ffffff; font-size: 2.5em; margin-bottom: 20px; text-shadow: 2px 2px 4px #000;">与我们一起探索海洋的奥秘</h2>
            <p style="font-size: 18px; line-height: 1.8; color: #ffffff; margin-bottom: 30px;">
            我们正在寻找充满激情、勇于创新的海洋科学家。如果你梦想着在这片蓝色疆域中留下自己的足迹，
            如果你渴望为保护海洋、造福人类贡献自己的力量，那么，加入我们吧！
            </p>
            <a href="mailto:recruitment@oceanlab.edu.cn" style="background-color: #ffffff; color: #003366; padding: 15px 30px; border-radius: 30px; text-decoration: none; font-weight: bold; font-size: 18px; transition: all 0.3s ease;">
                开启你的海洋之旅
            </a>
        </div>
        """, unsafe_allow_html=True)

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
        
        st.markdown("""
        <style>
        .project-card {
            background-color: #f0f8ff;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .project-title {
            color: #0066cc;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .project-description {
            font-size: 16px;
            color: #333;
            margin-bottom: 15px;
        }
        .project-progress {
            font-style: italic;
            color: #666;
        }
        </style>
        """, unsafe_allow_html=True)
        
        projects = [
            {
                "name": "海洋生态系统监测",
                "description": "利用先进的传感器技术和人工智能算法，实时监测和分析海洋生态系统的变化，为海洋保护和可持续发展提供科学依据。",
                "image": "Images/ocean_ecosystem.jpg",
                "progress": "正在进行数据收集和算法优化"
            },
            {
                "name": "海洋能源开发",
                "description": "研究和开发新型海洋能源技术，包括波浪能、潮汐能和海流能的高效转换系统，推动清洁能源的广泛应用。",
                "image": "Images/ocean_energy.jpg",
                "progress": "完成初步原型设计，准备进行实地测试"
            },
            {
                "name": "深海资源勘探",
                "description": "开发先进的深海探测设备和分析技术，用于发现和评估深海矿产资源，同时最小化对海洋环境的影响。",
                "image": "Images/deep_sea_exploration.jpg",
                "progress": "正在进行设备改进和环境影响评估"
            },
        ]
        
        for project in projects:
            st.markdown(f"""
            <div class="project-card">
                <div class="project-title">{project["name"]}</div>
                <img src="{project["image"]}" style="width:100%; max-width:400px; border-radius:5px; margin-bottom:15px;">
                <div class="project-description">{project["description"]}</div>
                <div class="project-progress">项目进展：{project["progress"]}</div>
            </div>
            """, unsafe_allow_html=True)

    def publications_page(self, username=None):
        st.title("发表论文")
        
        st.markdown("""
        <style>
        .publication-card {
            background-color: #f9f9f9;
            border-left: 5px solid #0066cc;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        .publication-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        }
        .pub-title {
            color: #0066cc;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .pub-authors {
            font-style: italic;
            color: #555;
            margin-bottom: 5px;
        }
        .pub-journal {
            color: #333;
            font-weight: 500;
        }
        .pub-year {
            background-color: #0066cc;
            color: white;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 14px;
            float: right;
        }
        </style>
        """, unsafe_allow_html=True)
        
        publications = [
            {"title": "人工智能在医疗诊断中的应用", "authors": "张三, 李四", "journal": "Nature", "year": 2023},
            {"title": "量子计算在密码学中的突破", "authors": "王五, 赵六", "journal": "Science", "year": 2022},
            {"title": "新型基因编辑技术的伦理考量", "authors": "刘七, 陈八", "journal": "Cell", "year": 2021},
        ]
        
        for pub in publications:
            st.markdown(f"""
            <div class="publication-card">
                <div class="pub-title">{pub['title']}</div>
                <div class="pub-authors">{pub['authors']}</div>
                <div class="pub-journal">{pub['journal']} <span class="pub-year">{pub['year']}</span></div>
            </div>
            """, unsafe_allow_html=True)

    def contact_page(self, username=None):
        st.markdown("""
        <style>
        .contact-container {
            display: flex;
            justify-content: space-between;
            margin-top: 2rem;
        }
        .contact-info, .contact-form {
            width: 48%;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .contact-info h3, .contact-form h3 {
            color: #0066cc;
            margin-bottom: 1rem;
        }
        .contact-item {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
        }
        .contact-icon {
            margin-right: 10px;
            color: #0066cc;
        }
        .map-container {
            height: 300px;
            width: 100%;
            margin-top: 2rem;
        }
        </style>
        """, unsafe_allow_html=True)

        st.title("联系我们")

        st.markdown("""
        <div class="contact-container">
            <div class="contact-info">
                <h3>联系方式</h3>
                <div class="contact-item">
                    <span class="contact-icon">📍</span>
                    <span>地址：山东省威海市文化西路180号</span>
                </div>
                <div class="contact-item">
                    <span class="contact-icon">📞</span>
                    <span>电话：0631-5688000</span>
                </div>
                <div class="contact-item">
                    <span class="contact-icon">✉️</span>
                    <span>邮箱：chenh@mail.sdu.edu.cn</span>
                </div>
                <div class="contact-item">
                    <span class="contact-icon">🌐</span>
                    <span>网站：www.frontierlab.com</span>
                </div>
            </div>
            <div class="contact-form">
                <h3>联系表单</h3>
                <form>
                    <input type="text" placeholder="您的姓名" style="width:100%; margin-bottom:10px; padding:5px;">
                    <input type="email" placeholder="您的邮箱" style="width:100%; margin-bottom:10px; padding:5px;">
                    <textarea placeholder="您的留言" style="width:100%; height:100px; margin-bottom:10px; padding:5px;"></textarea>
                    <button style="background-color:#0066cc; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer;">发送消息</button>
                </form>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="map-container">', unsafe_allow_html=True)
        m = folium.Map(location=[37.5323, 122.0587], zoom_start=15)
        folium.Marker([37.5323, 122.0587], popup="山东大学威海校区").add_to(m)
        folium_static(m)
        st.markdown('</div>', unsafe_allow_html=True)

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
