import streamlit as st
import plotly.express as px
import pandas as pd
import streamlit as st
import pandas as pd
import json
from PIL import Image
import folium   
from streamlit_folium import folium_static
from streamlit_lottie import st_lottie
import requests



@st.cache
def load_data():
    # 示例数据
    return pd.DataFrame({
        '时间': ['2023-01', '2023-02', '2023-03', '2023-04'],
        '研究成果': [10, 20, 15, 25]
    })

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def load_data():
    # 这里应该是加载实际数据的代码
    # 为了演示，我们使用一些模拟数据
    import pandas as pd
    import numpy as np
    
    dates = pd.date_range(start='1/1/2023', end='12/31/2023', freq='D')
    data = pd.DataFrame({
        '时间': dates,
        '研究成果': np.cumsum(np.random.randn(len(dates))) + 50
    })
    return data

def main_page():
    # 修改背景样式
    st.markdown("""
        <style>
            body {
                background: linear-gradient(-45deg, #002d72, #0056b3, #00a8e8, #0077be);
                background-size: 400% 400%;
                animation: gradientBG 15s ease infinite;
            }

            @keyframes gradientBG {
                0% {background-position: 0% 50%;}
                50% {background-position: 100% 50%;}
                100% {background-position: 0% 50%;}
            }

            .main-title {
                text-align: center;
                font-size: 3.5rem;
                color: #ffffff;
                padding: 30px;
                background-color: rgba(0, 45, 114, 0.9);
                border-radius: 15px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                margin-top: 30px;   
                letter-spacing: 2px;
                text-transform: uppercase;
            }

            .section-title {
                color: #ffffff;
                border-bottom: 2px solid #ffa500;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }

            .content-box {
                background-color: rgba(255, 255, 255, 0.9);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }

            .nav {
                position: fixed;
                top: 0;
                width: 100%;
                background-color: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 10px;
                text-align: center;
                z-index: 1000;
            }

            .nav a {
                color: white;
                margin: 0 15px;
                text-decoration: none;
                transition: color 0.3s;
            }

            .nav a:hover {
                color: #ffa500;
            }

            .team-member img {
                border-radius: 75px;
                transition: transform 0.2s;
                border: 3px solid #ffffff;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            }

            .team-member img:hover {
                transform: scale(1.1);
            }

            .footer {
                text-align: center;
                padding: 20px;
                background-color: #002d72;
                color: #ffffff;
                position: relative;
                bottom: 0;
                width: 100%;
            }

            .icon {
                margin-right: 5px;
            }

            /* 响应式设计 */
            @media (max-width: 768px) {
                .main-title {
                    font-size: 2.5rem;
                    padding: 20px;
                }
                .section-title {
                    font-size: 1.5rem;
                }
                .content-box {
                    padding: 15px;
                }
                .nav a {
                    margin: 0 10px;
                }
                .team-member img {
                    width: 100px;
                    height: 100px;
                }
            }
        </style>
    """, unsafe_allow_html=True)

    # 添加 Lottie 动画到页面顶部
    lottie_ocean = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_jbrw3hcz.json")
    st_lottie(lottie_ocean, height=300, key="ocean_animation")

    # 导航栏
    st.markdown("""
        <div class="nav">
            <a href="#实验室简介">实验室简介</a>
            <a href="#实时数据展示">实时数据展示</a>
            <a href="#研究团队">研究团队</a>
            <a href="#研究项目">研究项目</a>
            <a href="#发表论文">发表论文</a>
            <a href="#联系方式">联系方式</a>
            <a href="#新闻与更新">新闻与更新</a>
        </div>
    """, unsafe_allow_html=True)

    # 实验室标题
    st.markdown("""
        <h1 class="main-title" style="margin-top: 10px; animation: fadeInDown 1.5s;">
            Cosmos Lab
        </h1>
        <style>
            @keyframes fadeInDown {
                from {opacity: 0; transform: translate3d(0, -100%, 0);}
                to {opacity: 1; transform: translate3d(0, 0, 0);}
            }
        </style>
    """, unsafe_allow_html=True)

    # 修改实验室简介部分
    st.markdown('<h2 class="section-title" style="color: #000000;">实验室简介</h2>', unsafe_allow_html=True)
    
    # 添加 Lottie 动画到实验室简介旁边
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
            <div class="content-box">
                <p>Cosmos Lab 是一个致力于海洋科学前沿研究的世界级实验室。我们的使命是通过创新的科学方法和尖端技术，深入探索海洋生态系统，推动环境保护和可持续资源管理。</p>
                <p>我们的研究涵盖了从微观到宏观的多个层面，包括：</p>
                <ul>
                    <li>海洋生物多样性与生态系统功能</li>
                    <li>气候变化对海洋环境的影响</li>
                    <li>海洋污染监测与治理</li>
                    <li>海洋资源可持续利用</li>
                </ul>
                <p>通过跨学科合作和国际交流，我们致力于为全球海洋科学研究做出重大贡献。</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        lottie_research = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_kkflmtur.json")
        st_lottie(lottie_research, height=300, key="research_animation")
    
    # 悦动的立方体和研究重点
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div class="cube-container" style="width: 200px; height: 200px;">
                <div class="cube">
                    <div class="face front">海洋生态</div>
                    <div class="face back">环境保护</div>
                    <div class="face right">资源利用</div>
                    <div class="face left">气候变化</div>
                    <div class="face top">生物多样性</div>
                    <div class="face bottom">科技创新</div>
                </div>
            </div>
            <div style="width: 60%; padding: 20px;">
                <h3 style="color: #ffffff;">研究重点</h3>
                <div class="content-box">
                    <ul>
                        <li><strong>海洋生态系统动态：</strong>研究海洋生态系统的结构、功能和变化，以及人类活动对其的影响。</li>
                        <li><strong>海洋生物技术：</strong>开发基于海洋生物的新型材料、药物和能源解决方案。</li>
                        <li><strong>海洋环境监测：</strong>利用先进传感器和人工智能技术，实现海洋环境的实时监测和预警。</li>
                    </ul>
                </div>
            </div>
        </div>
        <style>
            .cube-container {
                perspective: 1000px;
                margin: 30px auto;
            }
            .cube {
                width: 100%;
                height: 100%;
                position: relative;
                transform-style: preserve-3d;
                animation: rotate 20s infinite linear;
            }
            .face {
                position: absolute;
                width: 100%;
                height: 100%;
                background: rgba(0, 100, 255, 0.3);
                border: 2px solid rgba(0, 100, 255, 0.7);
                box-shadow: 0 0 20px rgba(0, 100, 255, 0.5);
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 18px;
                color: white;
                text-shadow: 1px 1px 2px black;
            }
            .front  { transform: rotateY(0deg) translateZ(100px); }
            .back   { transform: rotateY(180deg) translateZ(100px); }
            .right  { transform: rotateY(90deg) translateZ(100px); }
            .left   { transform: rotateY(-90deg) translateZ(100px); }
            .top    { transform: rotateX(90deg) translateZ(100px); }
            .bottom { transform: rotateX(-90deg) translateZ(100px); }
            @keyframes rotate {
                0% { transform: rotateX(0deg) rotateY(0deg); }
                100% { transform: rotateX(360deg) rotateY(360deg); }
            }
            .cube:hover {
                animation-play-state: paused;
            }
            .face:hover {
                background: rgba(0, 255, 100, 0.5);
                cursor: pointer;
            }
        </style>
        <script>
            document.querySelector('.cube-container').addEventListener('mousemove', (e) => {
                const cube = document.querySelector('.cube');
                const rect = cube.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;
                cube.style.transform = `rotateY(${x / 5}deg) rotateX(${-y / 5}deg)`;
            });
            document.querySelector('.cube-container').addEventListener('mouseleave', () => {
                document.querySelector('.cube').style.transform = '';
            });
            document.querySelectorAll('.face').forEach(face => {
                face.addEventListener('click', () => {
                    alert('您点击了：' + face.textContent + '。这里可以链接到相关研究内容。');
                });
            });
        </script>
    """, unsafe_allow_html=True)


    # 动态数据图表
    st.markdown('<h2 class="section-title">实时数据展示</h2>', unsafe_allow_html=True)
    st.markdown('<div class="section" id="实时数据展示"></div>', unsafe_allow_html=True)

    data = load_data()
    fig = px.line(data, x='时间', y='研究成果', title='实验室研究成果趋势', markers=True)
    st.plotly_chart(fig)

    # 添加研究重点部分
    st.markdown('<h2 class="section-title">研究重点</h2>', unsafe_allow_html=True)
    research_focus = [
        {
            'title': '海洋生态系统动态',
            'description': '研究海洋生态系统的结构、功能和变化，以及人类活动对其的影响。',
            'icon': '🌊'
        },
        {
            'title': '海洋生物技术',
            'description': '开发基于海洋生物的新型材料、药物和能源解决方案。',
            'icon': '🧬'
        },
        {
            'title': '海洋环境监测',
            'description': '利用先进传感器和人工智能技术，实现海洋环境的实时监测和预警。',
            'icon': '📡'
        }
    ]

    cols = st.columns(len(research_focus))
    for i, focus in enumerate(research_focus):
        with cols[i]:
            st.markdown(f"""
                <div class="content-box" style="text-align: center;">
                    <h3>{focus['icon']} {focus['title']}</h3>
                    <p>{focus['description']}</p>
                </div>
            """, unsafe_allow_html=True)

    # 研究团队
    st.markdown('<h2 class="section-title">研究团队</h2>', unsafe_allow_html=True)
    st.markdown('<div class="section" id="研究团队"></div>', unsafe_allow_html=True)

    team_members = {
        '陈浩': {
            'description': '实验室主任，研究方向:(1)海洋天然产物开发,(2)功能性食品技术(3)营养/药物递送体系构建及传质规律研究',
            'image': 'Images/example1.jpg'
        }, 
        '王普': {
            'description': '博士研究生，研究方向：海洋生物多样性',
            'image': 'Images/example2.jpg'
        },
        '王淑新': {
            'description': '硕士研究生，研究方向：海洋污染治理',
            'image': 'Images/example3.jpg'
        },
        'bro': {
            'description': '硕士研究生，研究方向：海洋污染治理',
            'image': 'Images/example4.jpg'
        }
    }

    # 定义固定的图片尺寸
    IMAGE_SIZE = (200, 200)

    # 创建团队成员展示
    cols = st.columns(len(team_members))
    for i, (member, info) in enumerate(team_members.items()):
        with cols[i]:
            # 使用PIL库调整图片大小
            image = Image.open(info["image"])
            image = image.resize(IMAGE_SIZE)
            st.image(image, caption=member, use_column_width=True)
            st.markdown(f"<strong>{member}</strong><br>{info['description']}", unsafe_allow_html=True)

    # 修改研究项目展示
    st.markdown('<h2 class="section-title">研究项目</h2>', unsafe_allow_html=True)
    lottie_project = load_lottieurl("https://assets3.lottiefiles.com/private_files/lf30_P2uXE5.json")
    st_lottie(lottie_project, height=200, key="project_animation")
    
    projects = [
        {
            'name': '深海生态系统探索',
            'description': '利用先进的水下机器人技术，探索深海生态系统的未知领域。',
            'image': 'https://example.com/deep_sea_project.jpg',
            'link': 'https://example.com/project1'
        },
        {
            'name': '海洋微塑料污染研究',
            'description': '开发新型检测方法，评估微塑料对海洋生态系统的影响。',
            'image': 'https://example.com/microplastics_project.jpg',
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
    st.markdown('<h2 class="section-title">发表论文</h2>', unsafe_allow_html=True)
    st.markdown('<div class="section" id="发表论文"></div>', unsafe_allow_html=True)

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
    st.markdown('<h2 class="section-title">联系方式</h2>', unsafe_allow_html=True)
    st.markdown('<div class="section" id="联系方式"></div>', unsafe_allow_html=True)

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

    # 添加合作伙伴部分
    st.markdown('<h2 class="section-title">合作伙伴</h2>', unsafe_allow_html=True)
    partners = ['国家海洋局', '中国科学院海洋研究所', 'NOAA', 'Woods Hole 海洋研究所']
    st.markdown("""
        <div class="content-box">
            <p>我们与以下机构保持密切合作关系：</p>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
    """, unsafe_allow_html=True)
    for partner in partners:
        st.markdown(f'<div style="text-align: center; margin: 10px;"><img src="https://via.placeholder.com/100x50?text={partner}" alt="{partner}"><p>{partner}</p></div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

    # 新闻与更新
    st.markdown('<h2 class="section-title">新闻与更新</h2>', unsafe_allow_html=True)
    st.markdown('<div class="section" id="新闻与更新"></div>', unsafe_allow_html=True)

    updates = [
        '2024年1月：实验室获得国家自然科学基金支持。',
        '2024年2月：实验室成员参加国际海洋会议。'
    ]
    for update in updates:  
        st.write(f"- {update}")

    # 页脚
    st.markdown('<div class="footer">© 2024 陈浩实验室. 保留所有权利.</div>', unsafe_allow_html=True)
