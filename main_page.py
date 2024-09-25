import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from streamlit_lottie import st_lottie
import requests

# 辅助函数
def load_lottieurl(url: str):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

def load_data():
    # 模拟数据加载
    dates = pd.date_range(start='1/1/2023', end='12/31/2023', freq='D')
    data = pd.DataFrame({
        '时间': dates,
        '研究成果': np.cumsum(np.random.randn(len(dates))) + 50
    })
    return data

# 页面样式
def set_page_style():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
            
            body {
                background: linear-gradient(45deg, #000000, #0a192f);
                color: #ffffff;
                font-family: 'Orbitron', sans-serif;
            }

            .main-title {
                font-size: 4rem;
                text-align: center;
                color: #64ffda;
                text-shadow: 0 0 10px #64ffda, 0 0 20px #64ffda, 0 0 30px #64ffda;
                animation: glow 2s ease-in-out infinite alternate;
            }

            @keyframes glow {
                from {
                    text-shadow: 0 0 5px #64ffda, 0 0 10px #64ffda, 0 0 15px #64ffda;
                }
                to {
                    text-shadow: 0 0 10px #64ffda, 0 0 20px #64ffda, 0 0 30px #64ffda;
                }
            }

            .section-title {
                color: #ccd6f6;
                border-bottom: 2px solid #64ffda;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }

            .content-box {
                background-color: rgba(10, 25, 47, 0.7);
                border: 1px solid #64ffda;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 0 15px rgba(100, 255, 218, 0.3);
            }

            .nav {
                background-color: rgba(10, 25, 47, 0.9);
                padding: 10px;
                border-bottom: 1px solid #64ffda;
            }

            .nav a {
                color: #64ffda;
                margin: 0 15px;
                text-decoration: none;
                transition: all 0.3s ease;
            }

            .nav a:hover {
                color: #ffffff;
                text-shadow: 0 0 5px #64ffda;
            }

            /* 新增：悬浮效果 */
            .hover-effect {
                transition: all 0.3s ease;
            }

            .hover-effect:hover {
                transform: translateY(-5px);
                box-shadow: 0 5px 15px rgba(100, 255, 218, 0.5);
            }

            /* 新增：粒子背景 */
            #particles-js {
                position: fixed;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                z-index: -1;
            }

            /* 新增：3D卡片效果 */
            .card-3d {
                perspective: 1000px;
            }

            .card-3d-inner {
                transition: transform 0.6s;
                transform-style: preserve-3d;
            }

            .card-3d:hover .card-3d-inner {
                transform: rotateY(180deg);
            }

            .card-3d-front, .card-3d-back {
                position: absolute;
                width: 100%;
                height: 100%;
                backface-visibility: hidden;
            }

            .card-3d-back {
                transform: rotateY(180deg);
            }
        </style>
        <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
        <script>
            particlesJS.load('particles-js', 'assets/particles.json', function() {
                console.log('particles.js loaded');
            });
        </script>
        <div id="particles-js"></div>
    """, unsafe_allow_html=True)

# 导航栏
def create_navigation():
    st.markdown("""
        <div class="nav">
            <a href="#实验室简介">实验室简介</a>
            <a href="#研究重点">研究重点</a>
            <a href="#研究团队">研究团队</a>
            <a href="#研究项目">研究项目</a>
            <a href="#联系方式">联系方式</a>
        </div>
    """, unsafe_allow_html=True)

# 实验室简介
def lab_introduction():
    st.markdown('<h2 class="section-title">实验室简介</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
            <div class="content-box hover-effect">
                <p>Cosmos Lab 是一个致力于探索宇宙奥秘的前沿实验室。我们运用尖端科技和创新方法，深入研究宇宙的起源、结构和演化。</p>
                <p>我们的主要研究方向包括：</p>
                <ul>
                    <li>暗物质和暗能量</li>
                    <li>引力波探测</li>
                    <li>系外行星和宜居性</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        lottie_space = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_KUFdS6.json")
        st_lottie(lottie_space, height=300, key="space_animation")

# 研究重点
def research_focus():
    st.markdown('<h2 class="section-title">研究重点</h2>', unsafe_allow_html=True)
    research_areas = [
        {
            'title': '暗物质探测',
            'description': '利用先进的粒子探测器和数据分析技术，揭示暗物质的本质。',
            'icon': '🔭'
        },
        {
            'title': '引力波天文学',
            'description': '通过LIGO等设备，探测和分析引力波信号，开启多信使天文学新时代。',
            'icon': '🌊'
        },
        {
            'title': '系外行星研究',
            'description': '搜寻和研究系外行星，评估其宜居性，探索地外生命的可能性。',
            'icon': '🪐'
        }
    ]

    cols = st.columns(len(research_areas))
    for i, area in enumerate(research_areas):
        with cols[i]:
            st.markdown(f"""
                <div class="content-box hover-effect card-3d">
                    <div class="card-3d-inner">
                        <div class="card-3d-front">
                            <h3>{area['icon']} {area['title']}</h3>
                        </div>
                        <div class="card-3d-back">
                            <p>{area['description']}</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# 研究团队
def research_team():
    st.markdown('<h2 class="section-title">研究团队</h2>', unsafe_allow_html=True)
    team_members = {
        '陈浩': {
            'description': '实验室主任，研究方向：理论宇宙学',
            'image': 'https://example.com/images/chen_hao.jpg'
        },
        '王普': {
            'description': '首席科学家，研究方向：引力波物理',
            'image': 'https://example.com/images/wang_pu.jpg'
        },
        '张明': {
            'description': '高级研究员，研究方向：系外行星探测',
            'image': 'https://example.com/images/zhang_ming.jpg'
        }
    }

    cols = st.columns(len(team_members))
    for i, (member, info) in enumerate(team_members.items()):
        with cols[i]:
            st.markdown(f"""
                <div class="content-box hover-effect" style="text-align: center;">
                    <img src="{info['image']}" style="width:150px; height:150px; border-radius:50%; object-fit:cover;">
                    <h3>{member}</h3>
                    <p>{info['description']}</p>
                </div>
            """, unsafe_allow_html=True)

# 研究项目
def research_projects():
    st.markdown('<h2 class="section-title">研究项目</h2>', unsafe_allow_html=True)
    
    projects = [
        {
            'name': '深海生态系统探索',
            'description': '利用先进的水下机器人技术，探索深海生态系统的未知领域。',
            'image': 'https://example.com/images/deep_sea_project.jpg',
            'link': 'https://example.com/project1'
        },
        {
            'name': '海洋微塑料污染研究',
            'description': '开发新型检测方法，评估微塑料对海洋生态系统的影响。',
            'image': 'https://example.com/images/microplastics_project.jpg',
            'link': 'https://example.com/project2'
        }
    ]

    for project in projects:
        st.markdown(f"""
            <div class="content-box" style="display: flex; align-items: center;">
                <img src="{project['image']}" style="width: 150px; height: 150px; object-fit: cover; margin-right: 20px; border-radius: 10px;">
                <div>
                    <h3>{project['name']}</h3>
                    <p>{project['description']}</p>
                    <a href="{project['link']}" target="_blank">了解更多 →</a>
                </div>
            </div>
        """, unsafe_allow_html=True)

# 发表论文
def published_papers():
    st.markdown('<h2 class="section-title">发表论文</h2>', unsafe_allow_html=True)
    papers = [
        {
            'title': '海洋生态学的现状与展望',
            'link': 'https://example.com/paper1'
        },
        {
            'title': '海洋污染治理的新方法',
            'link': 'https://example.com/paper2'
        }
    ]

    for paper in papers:
        st.markdown(f"""
            <div class="section">
                <p><a href="{paper['link']}">{paper['title']}</a></p>
            </div>
        """, unsafe_allow_html=True)

# 联系方式
def contact_info():
    st.markdown('<h2 class="section-title">联系方式</h2>', unsafe_allow_html=True)
    contact_info = {
        'Email': 'chenh@mail.sdu.edu.cn',
        '电话': '+86 123 456 7890',
        '社交媒体': '[Twitter](https://twitter.com/example), [ResearchGate](https://www.researchgate.net/)'
    }

    col1, col2 = st.columns([1, 2])
    with col1:
        lottie_contact = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_u25cckyh.json")
        st_lottie(lottie_contact, height=200, key="contact_animation")
    with col2:
        for key, value in contact_info.items():
            st.markdown(f"""
                <div style="display: flex; align-items: center;">
                    <span class="icon">🔗</span><strong>{key}:</strong> {value}
                </div>
            """, unsafe_allow_html=True)

# 合作伙伴
def partners():
    st.markdown('<h2 class="section-title">合作伙伴</h2>', unsafe_allow_html=True)
    partners = ['国家海洋局', '中国科学院海洋研究所', 'NOAA', 'Woods Hole 海洋研究所']
    st.markdown("""
        <div class="content-box">
            <p>我们与以下机构保持密切合作关系：</p>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
    """, unsafe_allow_html=True)
    for partner in partners:
        st.markdown(f'<div style="text-align: center; margin: 10px;"><img src="https://example.com/images/{partner.lower().replace(" ", "_")}.jpg" alt="{partner}" style="width: 100px; height: 50px; object-fit: contain;"><p>{partner}</p></div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

# 新闻与更新
def news_and_updates():
    st.markdown('<h2 class="section-title">新闻与更新</h2>', unsafe_allow_html=True)
    updates = [
        '2024年1月：实验室获得国家自然科学基金支持。',
        '2024年2月：实验室成员参加国际海洋会议。'
    ]
    for update in updates:  
        st.write(f"- {update}")

# 页脚
def footer():
    st.markdown('<div class="footer">© 2024 陈浩实验室. 保留所有权利.</div>', unsafe_allow_html=True)

# 主函数
def main_page():
    set_page_style()
    create_navigation()
    
    st.markdown("""
        <h1 class="main-title">
            Cosmos Lab
        </h1>
    """, unsafe_allow_html=True)
    
    lab_introduction()
    research_focus()
    research_team()
    research_projects()
    published_papers()
    contact_info()
    partners()
    news_and_updates()
    footer()

if __name__ == "__main__":
    main_page()
