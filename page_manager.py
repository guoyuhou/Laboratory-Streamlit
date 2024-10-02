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
        st.markdown("""
        <style>
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
            100% { transform: translateY(0px); }
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(0, 102, 204, 0.7); }
            70% { box-shadow: 0 0 0 20px rgba(0, 102, 204, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 102, 204, 0); }
        }
        .team-member {
            background: linear-gradient(45deg, #ffffff, #f0f8ff);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 15px 30px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            transition: all 0.5s ease;
            animation: float 6s ease-in-out infinite;
        }
        .team-member:hover {
            transform: translateY(-10px) scale(1.03);
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }
        .team-member img {
            width: 200px;
            height: 200px;
            object-fit: cover;
            border-radius: 50%;
            display: block;
            margin: 0 auto;
            border: 5px solid #fff;
            box-shadow: 0 0 20px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        .team-member:hover img {
            animation: pulse 2s infinite;
        }
        .team-member h3 {
            text-align: center;
            color: #003366;
            margin-top: 20px;
            font-size: 1.8em;
            transition: all 0.3s ease;
        }
        .team-member:hover h3 {
            color: #0066cc;
            transform: scale(1.1);
        }
        .team-member p {
            text-align: center;
            color: #333;
            font-size: 1em;
            margin: 15px 0;
            opacity: 0.8;
            transition: all 0.3s ease;
        }
        .team-member:hover p {
            opacity: 1;
        }
        .team-member blockquote {
            font-style: italic;
            color: #666;
            border-left: 4px solid #0066cc;
            padding-left: 15px;
            margin: 20px 0;
            transition: all 0.3s ease;
        }
        .team-member:hover blockquote {
            border-left-width: 8px;
            padding-left: 20px;
            color: #0066cc;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("<h2 style='text-align: center; color: #003366; font-size: 2.5em; margin: 40px 0; text-shadow: 2px 2px 4px #aaa;'>核心成员</h2>", unsafe_allow_html=True)
        
        cols = st.columns(2)  # 每行显示2个成员
        for i, member in enumerate(members):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="team-member">
                    <img src="{member['image']}">
                    <h3>{member['name']}</h3>
                    <p style="font-weight: bold; color: #0066cc; font-size: 1.2em;">{member['title']}</p>
                    <p>{member['description']}</p>
                    <blockquote>"{member['quote']}"</blockquote>
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
        <style>
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .partner-logo {
            transition: all 0.3s ease;
        }
        .partner-logo:hover {
            transform: scale(1.1);
            animation: rotate 2s linear infinite;
        }
        </style>
        <div style="background: linear-gradient(135deg, #f0f8ff, #e6f3ff); padding: 30px; border-radius: 15px; margin-top: 40px; box-shadow: 0 15px 30px rgba(0,0,0,0.1);">
            <h2 style="color: #003366; font-size: 2.5em; margin-bottom: 30px; text-align: center; text-shadow: 2px 2px 4px #aaa;">全球合作网络</h2>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
                <div style="text-align: center; margin: 20px;">
                    <img src="https://images.unsplash.com/photo-1541339907198-e08756dedf3f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80" class="partner-logo" style="width: 150px; height: 150px; object-fit: cover; border-radius: 50%; box-shadow: 0 10px 20px rgba(0,0,0,0.1);">
                    <p style="margin-top: 15px; font-weight: bold; color: #0066cc;">中国海洋大学</p>
                </div>
                <div style="text-align: center; margin: 20px;">
                    <img src="https://images.unsplash.com/photo-1527100673774-cce25eafaf7f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80" class="partner-logo" style="width: 150px; height: 150px; object-fit: cover; border-radius: 50%; box-shadow: 0 10px 20px rgba(0,0,0,0.1);">
                    <p style="margin-top: 15px; font-weight: bold; color: #0066cc;">国家海洋局第一海洋研究所</p>
                </div>
                <div style="text-align: center; margin: 20px;">
                    <img src="https://images.unsplash.com/photo-1472214103451-9374bd1c798e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80" class="partner-logo" style="width: 150px; height: 150px; object-fit: cover; border-radius: 50%; box-shadow: 0 10px 20px rgba(0,0,0,0.1);">
                    <p style="margin-top: 15px; font-weight: bold; color: #0066cc;">美国伍兹霍尔海洋研究所</p>
                </div>
                <div style="text-align: center; margin: 20px;">
                    <img src="https://images.unsplash.com/photo-1484291470158-b8f8d608850d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80" class="partner-logo" style="width: 150px; height: 150px; object-fit: cover; border-radius: 50%; box-shadow: 0 10px 20px rgba(0,0,0,0.1);">
                    <p style="margin-top: 15px; font-weight: bold; color: #0066cc;">日本东京大学大气与海洋研究所</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 加入我们
        st.markdown("""
        <style>
        @keyframes wave {
            0% { transform: translateY(0); }
            50% { transform: translateY(-15px); }
            100% { transform: translateY(0); }
        }
        .join-us {
            background: linear-gradient(135deg, #003366, #0066cc);
            padding: 40px;
            border-radius: 15px;
            margin-top: 40px;
            text-align: center;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            position: relative;
            overflow: hidden;
        }
        .join-us::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
            animation: wave 8s linear infinite;
        }
        .join-us-button {
            background-color: #ffffff;
            color: #003366;
            padding: 15px 30px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: bold;
            font-size: 18px;
            transition: all 0.3s ease;
            display: inline-block;
            margin-top: 20px;
        }
        .join-us-button:hover {
            background-color: #003366;
            color: #ffffff;
            transform: scale(1.05);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        </style>
        <div class="join-us">
            <h2 style="color: #ffffff; font-size: 2.5em; margin-bottom: 20px; text-shadow: 2px 2px 4px #000;">与我们一起探索海洋的奥秘</h2>
            <p style="font-size: 18px; line-height: 1.8; color: #ffffff; margin-bottom: 30px;">
            我们正在寻找充满激情、勇于创新的海洋科学家。如果你梦想着在这片蓝色疆域中留下自己的足迹，
            如果你渴望为保护海洋、造福人类贡献自己的力量，那么，加入我们吧！
            </p>
            <a href="mailto:recruitment@oceanlab.edu.cn" class="join-us-button">
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
        @keyframes fadeInScale {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
        @keyframes shimmer {
            0% { background-position: -1000px 0; }
            100% { background-position: 1000px 0; }
        }
        .project-card {
            background-color: #ffffff;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 40px;
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
            transition: all 0.6s cubic-bezier(0.165, 0.84, 0.44, 1);
            animation: fadeInScale 0.8s ease-out;
            position: relative;
            overflow: hidden;
        }
        .project-card::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.3) 50%, rgba(255,255,255,0) 100%);
            transform: rotate(30deg);
            opacity: 0;
            transition: opacity 0.6s;
        }
        .project-card:hover {
            transform: translateY(-15px) scale(1.03);
            box-shadow: 0 20px 40px rgba(0, 0, 102, 0.2);
        }
        .project-card:hover::after {
            animation: shimmer 2s infinite;
            opacity: 1;
        }
        .project-title {
            color: #003366;
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 20px;
            position: relative;
            display: inline-block;
        }
        .project-title::before {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 0;
            height: 3px;
            background: linear-gradient(90deg, #003366, #0066cc);
            transition: width 0.6s ease;
        }
        .project-card:hover .project-title::before {
            width: 100%;
        }
        .project-description {
            font-size: 18px;
            color: #333;
            margin-bottom: 25px;
            line-height: 1.8;
            text-align: justify;
        }
        .project-progress {
            font-style: italic;
            color: #ffffff;
            font-weight: 500;
            display: inline-block;
            padding: 10px 20px;
            background: linear-gradient(45deg, #003366, #0066cc);
            border-radius: 30px;
            box-shadow: 0 5px 15px rgba(0, 102, 204, 0.3);
            transition: all 0.3s ease;
        }
        .project-progress:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0, 102, 204, 0.4);
        }
        .project-image {
            width: 100%;
            max-width: 500px;
            border-radius: 15px;
            margin-bottom: 25px;
            transition: transform 0.5s ease, box-shadow 0.5s ease;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        }
        .project-image:hover {
            transform: scale(1.05) rotate(1deg);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
        }
        .progress-bar {
            background-color: #e6e6e6;
            height: 10px;
            border-radius: 5px;
            margin-top: 20px;
            overflow: hidden;
            position: relative;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #003366, #0066cc);
            border-radius: 5px;
            transition: width 1.5s ease-out;
            position: relative;
        }
        .progress-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(
                45deg,
                rgba(255,255,255,0.2) 25%,
                transparent 25%,
                transparent 50%,
                rgba(255,255,255,0.2) 50%,
                rgba(255,255,255,0.2) 75%,
                transparent 75%,
                transparent
            );
            background-size: 50px 50px;
            animation: stripes 1s linear infinite;
        }
        @keyframes stripes {
            0% { background-position: 0 0; }
            100% { background-position: 50px 0; }
        }
        </style>
        <script>
        function animateProgress(element, targetWidth) {
            element.style.width = '0%';
            setTimeout(() => {
                element.style.width = targetWidth + '%';
            }, 100);
        }
        </script>
        """, unsafe_allow_html=True)
        
        projects = [
            {
                "name": "海洋生态系统监测",
                "description": "利用先进的传感器技术和人工智能算法，实时监测和分析海洋生态系统的变化，为海洋保护和可持续发展提供科学依据。我们的团队正在开发一套革命性的水下传感网络，结合机器学习技术，能够实时捕捉海洋环境的微小变化。",
                "image": "Images/ocean_ecosystem.jpg",
                "progress": "数据收集和算法优化进行中",
                "percent": 65
            },
            {
                "name": "海洋能源开发",
                "description": "研究和开发新型海洋能源技术，包括波浪能、潮汐能和海流能的高效转换系统，推动清洁能源的广泛应用。我们的最新突破是一种模块化的海洋能源转换装置，可以适应不同海域环境，大幅提高能源转换效率。",
                "image": "Images/ocean_energy.jpg",
                "progress": "原型设计完成，准备实地测试",
                "percent": 80
            },
            {
                "name": "深海资源勘探",
                "description": "开发先进的深海探测设备和分析技术，用于发现和评估深海矿产资源，同时最小化对海洋环境的影响。我们正在研发一种革命性的深海无人探测器，配备高精度声呐和光学系统，可以在极端压力下工作。",
                "image": "Images/deep_sea_exploration.jpg",
                "progress": "设备改进和环境影响评估中",
                "percent": 45
            },
        ]
        
        for index, project in enumerate(projects):
            st.markdown(f"""
            <div class="project-card" style="animation-delay: {index * 0.2}s;">
                <h2 class="project-title">{project["name"]}</h2>
                <img src="{project["image"]}" class="project-image" alt="{project["name"]}" loading="lazy">
                <p class="project-description">{project["description"]}</p>
                <div class="project-progress">{project["progress"]}</div>
                <div class="progress-bar">
                    <div class="progress-fill" id="progress-{index}"></div>
                </div>
            </div>
            <script>
                animateProgress(document.getElementById('progress-{index}'), {project["percent"]});
            </script>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <script>
        document.addEventListener('DOMContentLoaded', (event) => {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }
                });
            }, {
                threshold: 0.1
            });

            document.querySelectorAll('.project-card').forEach(card => {
                observer.observe(card);
            });
        });
        </script>
        """, unsafe_allow_html=True)

    def publications_page(self, username=None):
        st.title("发表论文")
        
        st.markdown("""
        <style>
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translate3d(0, 40px, 0);
            }
            to {
                opacity: 1;
                transform: translate3d(0, 0, 0);
            }
        }
        .publication-card {
            background-color: #ffffff;
            border-left: 5px solid #4a90e2;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            transition: all 0.5s cubic-bezier(0.25, 0.8, 0.25, 1);
            animation: fadeInUp 0.6s ease-out;
            animation-fill-mode: both;
        }
        .publication-card:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
        }
        .pub-title {
            color: #4a90e2;
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 15px;
            transition: color 0.3s ease;
        }
        .publication-card:hover .pub-title {
            color: #2c3e50;
        }
        .pub-authors {
            font-style: italic;
            color: #7f8c8d;
            margin-bottom: 10px;
            font-size: 16px;
        }
        .pub-journal {
            color: #34495e;
            font-weight: 600;
            font-size: 18px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .pub-year {
            background-color: #4a90e2;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .publication-card:hover .pub-year {
            background-color: #2c3e50;
            transform: scale(1.1);
        }
        </style>
        <script>
        function animatePublications() {
            const cards = document.querySelectorAll('.publication-card');
            cards.forEach((card, index) => {
                card.style.animationDelay = `${index * 0.2}s`;
            });
        }
        document.addEventListener('DOMContentLoaded', animatePublications);
        </script>
        """, unsafe_allow_html=True)
        
        publications = [
            {"title": "人工智能在医疗诊断中的应用：深度学习模型的突破性进展", "authors": "张三, 李四, 王五", "journal": "Nature Medicine", "year": 2023},
            {"title": "量子计算在密码学中的革命性应用：后量子时代的安全挑战与机遇", "authors": "王五, 赵六, 孙七", "journal": "Science", "year": 2022},
            {"title": "CRISPR-Cas9基因编辑技术的伦理考量：平衡科技进步与社会责任", "authors": "刘七, 陈八, 周九", "journal": "Cell", "year": 2021},
        ]
        
        for pub in publications:
            st.markdown(f"""
            <div class="publication-card">
                <div class="pub-title">{pub['title']}</div>
                <div class="pub-authors">{pub['authors']}</div>
                <div class="pub-journal">
                    <span>{pub['journal']}</span>
                    <span class="pub-year">{pub['year']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    def contact_page(self, username=None):
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
        
        .contact-container {
            font-family: 'Roboto', sans-serif;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            margin-top: 2rem;
            perspective: 1000px;
        }
        .contact-info, .contact-form, .faq-section, .social-media {
            width: 48%;
            padding: 30px;
            background: linear-gradient(145deg, #f0f0f0, #ffffff);
            border-radius: 20px;
            box-shadow: 20px 20px 60px #d0d0d0, -20px -20px 60px #ffffff;
            transition: transform 0.6s;
            transform-style: preserve-3d;
            margin-bottom: 2rem;
        }
        .contact-info:hover, .contact-form:hover, .faq-section:hover, .social-media:hover {
            transform: rotateY(10deg);
        }
        .contact-info h3, .contact-form h3, .faq-section h3, .social-media h3 {
            color: #0066cc;
            margin-bottom: 1.5rem;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .contact-item, .faq-item, .social-item {
            display: flex;
            align-items: center;
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
        }
        .contact-item:hover, .faq-item:hover, .social-item:hover {
            transform: translateX(10px);
        }
        .contact-icon, .faq-icon, .social-icon {
            margin-right: 15px;
            color: #0066cc;
            font-size: 1.5em;
        }
        input, textarea {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: none;
            border-radius: 10px;
            background-color: #f0f0f0;
            transition: all 0.3s ease;
        }
        input:focus, textarea:focus {
            outline: none;
            box-shadow: 0 0 0 2px #0066cc;
        }
        button {
            background-color: #0066cc;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 700;
        }
        button:hover {
            background-color: #004499;
            transform: scale(1.05);
        }
        .faq-answer {
            display: none;
            margin-top: 10px;
            padding: 10px;
            background-color: #f9f9f9;
            border-radius: 5px;
        }
        .social-item a {
            color: #0066cc;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        .social-item a:hover {
            color: #004499;
        }
        .map-container {
            width: 100%;
            height: 300px;
            margin-top: 2rem;
            border-radius: 20px;
            overflow: hidden;
        }
        </style>
        <script>
        document.addEventListener('DOMContentLoaded', (event) => {
            const items = document.querySelectorAll('.contact-item, .faq-item, .social-item');
            items.forEach((item, index) => {
                item.style.opacity = '0';
                item.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    item.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                    item.style.opacity = '1';
                    item.style.transform = 'translateY(0)';
                }, index * 200);
            });

            const form = document.querySelector('form');
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                const button = form.querySelector('button');
                button.innerHTML = '发送中...';
                button.style.backgroundColor = '#004499';
                setTimeout(() => {
                    button.innerHTML = '发送成功！';
                    button.style.backgroundColor = '#00cc66';
                }, 2000);
            });

            const faqItems = document.querySelectorAll('.faq-item');
            faqItems.forEach(item => {
                item.addEventListener('click', () => {
                    const answer = item.querySelector('.faq-answer');
                    answer.style.display = answer.style.display === 'none' ? 'block' : 'none';
                });
            });
        });
        </script>
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
                <div class="contact-item">
                    <span class="contact-icon">🕒</span>
                    <span>工作时间：周一至周五 9:00-17:00</span>
                </div>
            </div>
            <div class="contact-form">
                <h3>联系表单</h3>
                <form>
                    <input type="text" placeholder="您的姓名" required>
                    <input type="email" placeholder="您的邮箱" required>
                    <textarea placeholder="您的留言" required></textarea>
                    <button type="submit">发送消息</button>
                </form>
            </div>
            <div class="faq-section">
                <h3>常见问题</h3>
                <div class="faq-item">
                    <span class="faq-icon">❓</span>
                    <span>如何申请加入实验室？</span>
                    <div class="faq-answer">请发送您的简历和研究兴趣到我们的邮箱。我们会在收到后尽快回复您。</div>
                </div>
                <div class="faq-item">
                    <span class="faq-icon">❓</span>
                    <span>实验室是否提供实习机会？</span>
                    <div class="faq-answer">是的，我们每年夏季都会提供实习机会。请关注我们的网站获取最新信息。</div>
                </div>
                <div class="faq-item">
                    <span class="faq-icon">❓</span>
                    <span>如何获取实验室的最新研究进展？</span>
                    <div class="faq-answer">您可以订阅我们的电子简报或关注我们的社交媒体账号。</div>
                </div>
            </div>
            <div class="social-media">
                <h3>关注我们</h3>
                <div class="social-item">
                    <span class="social-icon">🐦</span>
                    <a href="https://twitter.com/frontierlab" target="_blank">Twitter</a>
                </div>
                <div class="social-item">
                    <span class="social-icon">📘</span>
                    <a href="https://www.facebook.com/frontierlab" target="_blank">Facebook</a>
                </div>
                <div class="social-item">
                    <span class="social-icon">🔬</span>
                    <a href="https://www.researchgate.net/lab/frontierlab" target="_blank">ResearchGate</a>
                </div>
                <div class="social-item">
                    <span class="social-icon">📺</span>
                    <a href="https://www.youtube.com/frontierlab" target="_blank">YouTube</a>
                </div>
            </div>
        </div>
        <div class="map-container">
            <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3238.540494861871!2d122.05945731525902!3d37.53291797980501!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3590f8d5d3b4b1e3%3A0x3f3c3e8d3d3d3d3d!2s山东大学威海校区!5e0!3m2!1szh-CN!2scn!4v1625123456789!5m2!1szh-CN!2scn" width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
        </div>
        """, unsafe_allow_html=True)

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
