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
                background-color: #000000;
                color: #ffffff;
                font-family: 'Orbitron', sans-serif;
            }

            .main-title {
                font-size: 4rem;
                text-align: center;
                color: #00ffff;
                animation: glow 2s ease-in-out infinite alternate;
            }

            @keyframes glow {
                from {
                    text-shadow: 0 0 5px #00ffff, 0 0 10px #00ffff;
                }
                to {
                    text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 30px #00ffff;
                }
            }

            .section-title {
                color: #00ffff;
                border-bottom: 2px solid #00ffff;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }

            .content-box {
                background-color: rgba(0, 255, 255, 0.1);
                border: 1px solid #00ffff;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
                transition: all 0.3s ease;
            }

            .content-box:hover {
                transform: translateY(-5px);
                box-shadow: 0 5px 15px rgba(0, 255, 255, 0.5);  
            }

            .team-member-img {
                width: 150px;
                height: 150px;
                border-radius: 50%;
                object-fit: cover;
                border: 3px solid #00ffff;
                transition: all 0.3s ease;
            }

            .team-member-img:hover {
                transform: scale(1.1);
                box-shadow: 0 0 20px rgba(0, 255, 255, 0.7);
            }

            /* 新增：星空背景 */
            #stars {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: -1;
            }

            /* 新增：粒子效果 */
            #particles-js {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: -1;
            }

            /* 新增：3D翻转卡片效果 */
            .flip-card {
                background-color: transparent;
                width: 300px;
                height: 200px;
                perspective: 1000px;
                margin: 20px auto;
            }

            .flip-card-inner {
                position: relative;
                width: 100%;
                height: 100%;
                text-align: center;
                transition: transform 0.6s;
                transform-style: preserve-3d;
            }

            .flip-card:hover .flip-card-inner {
                transform: rotateY(180deg);
            }

            .flip-card-front, .flip-card-back {
                position: absolute;
                width: 100%;
                height: 100%;
                backface-visibility: hidden;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 10px;
            }

            .flip-card-front {
                background-color: rgba(0, 255, 255, 0.2);
                color: #00ffff;
            }

            /* 新增：圆形团队照片 */
            .team-member-img {
                width: 150px;
                height: 150px;
                border-radius: 50%;
                object-fit: cover;
                border: 3px solid #0066cc;
            }
        </style>

        <!-- 添加粒子效果库 -->
        <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>

        <!-- 添加星空背景 -->
        <canvas id="stars"></canvas>

        <!-- 添加粒子效果容器 -->
        <div id="particles-js"></div>

        <script>
            // 星空背景动画
            const canvas = document.getElementById('stars');
            const ctx = canvas.getContext('2d');
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;

            const stars = [];
            for (let i = 0; i < 200; i++) {
                stars.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    radius: Math.random() * 1.5,
                    vx: Math.floor(Math.random() * 50) - 25,
                    vy: Math.floor(Math.random() * 50) - 25
                });
            }

            function draw() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.globalCompositeOperation = "lighter";
                for (let i = 0; i < stars.length; i++) {
                    const s = stars[i];
                    ctx.fillStyle = "#00ffff";
                    ctx.beginPath();
                    ctx.arc(s.x, s.y, s.radius, 0, 2 * Math.PI);
                    ctx.fill();
                    s.x += s.vx / 100;
                    s.y += s.vy / 100;
                    if (s.x < 0 || s.x > canvas.width) s.vx = -s.vx;
                    if (s.y < 0 || s.y > canvas.height) s.vy = -s.vy;
                }
                requestAnimationFrame(draw);
            }
            draw();

            // 粒子效果配置
            particlesJS("particles-js", {
                particles: {
                    number: { value: 80, density: { enable: true, value_area: 800 } },
                    color: { value: "#00ffff" },
                    shape: { type: "circle" },
                    opacity: { value: 0.5, random: false },
                    size: { value: 3, random: true },
                    line_linked: { enable: true, distance: 150, color: "#00ffff", opacity: 0.4, width: 1 },
                    move: { enable: true, speed: 6, direction: "none", random: false, straight: false, out_mode: "out", bounce: false }
                },
                interactivity: {
                    detect_on: "canvas",
                    events: { onhover: { enable: true, mode: "repulse" }, onclick: { enable: true, mode: "push" }, resize: true },
                    modes: { repulse: { distance: 100, duration: 0.4 }, push: { particles_nb: 4 } }
                },
                retina_detect: true
            });
        </script>
    """, unsafe_allow_html=True)

# 实验室简介
def lab_introduction():
    st.markdown('<h2 class="section-title">实验室简介</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
            <div class="content-box">
                <p>Cosmos Lab 是一个致力于海洋科学前沿研究的世界级实验室。我们通过创新的科学方法和尖端技术，深入探索海洋生态系统，推动环境保护和可持续资源管理。</p>
                <p>我们的主要研究方向包括：</p>
                <ul>
                    <li>海洋生物多样性与生态系统功能</li>
                    <li>气候变化对海洋环境的影响</li>
                    <li>海洋污染监测与治理</li>
                </ul>
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
                <h3 style="color: #0066cc;">研究重点</h3>
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
                background: rgba(0, 102, 204, 0.3);
                border: 2px solid rgba(0, 102, 204, 0.7);
                box-shadow: 0 0 20px rgba(0, 102, 204, 0.5);
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 18px;
                color: #0066cc;
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
                background: rgba(0, 102, 204, 0.5);
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

# 研究重点
def research_focus():
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
                <div class="content-box hover-effect card-3d">
                    <div class="card-3d-inner">
                        <div class="card-3d-front">
                            <h3>{focus['icon']} {focus['title']}</h3>
                        </div>
                        <div class="card-3d-back">
                            <p>{focus['description']}</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# 研究团队
def research_team():
    st.markdown('<h2 class="section-title">研究团队</h2>', unsafe_allow_html=True)
    team_members = {
        '陈浩': {
            'description': '实验室主任，研究方向:(1)海洋天然产物开发,(2)功能性食品技术(3)营养/药物递送体系构建及传质规律研究',
            'image': 'https://img1.baidu.com/it/u=1978093910,2102820411&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=313'
        }, 
        '王普': {
            'description': '博士研究生，研究方向：海洋生物多样性',
            'image': 'https://img2.baidu.com/it/u=2521851051,2189866243&fm=253&fmt=auto&app=138&f=JPEG?w=889&h=500'
        },
        '王淑新': {
            'description': '硕士研究生，研究方向：海洋污染治理',
            'image': 'https://img0.baidu.com/it/u=1407750889,3441968730&fm=253&fmt=auto&app=120&f=JPEG?w=1200&h=799'
        },
        '张明': {
            'description': '硕士研究生，研究方向：海洋污染治理',
            'image': 'https://img2.baidu.com/it/u=1814268193,3619863984&fm=253&fmt=auto&app=138&f=JPEG?w=632&h=500'
        }
    }

    cols = st.columns(len(team_members))
    for i, (member, info) in enumerate(team_members.items()):
        with cols[i]:
            st.markdown(f"""
                <div class="content-box hover-effect" style="text-align: center;">
                    <img src="{info['image']}" class="team-member-img">
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
            <div class="content-box hover-effect" style="display: flex; align-items: center;">
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
            <div class="content-box hover-effect">
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
                <div class="content-box hover-effect" style="display: flex; align-items: center;">
                    <span class="icon">🔗</span><strong>{key}:</strong> {value}
                </div>
            """, unsafe_allow_html=True)

# 合作伙伴
def partners():
    st.markdown('<h2 class="section-title">合作伙伴</h2>', unsafe_allow_html=True)
    partners = ['国家海洋局', '中国科学院海洋研究所', 'NOAA', 'Woods Hole 海洋研究所']
    st.markdown("""
        <div class="content-box hover-effect">
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
        st.markdown(f"""
            <div class="content-box hover-effect">
                <p>- {update}</p>
            </div>
        """, unsafe_allow_html=True)

# 页脚
def footer():
    st.markdown('<div class="footer">© 2024 陈浩实验室. 保留所有权利.</div>', unsafe_allow_html=True)

# 主函数
def main_page():
    set_page_style()
    
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
    
    lab_introduction()
    research_focus()
    research_team()
    research_projects()
    published_papers()
    contact_info()
    partners()
    news_and_updates()
    footer()

    # 新增：滚动动画效果
    st.markdown("""
        <script>
            function isElementInViewport(el) {
                var rect = el.getBoundingClientRect();
                return (
                    rect.top >= 0 &&
                    rect.left >= 0 &&
                    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
                );
            }

            function handleScroll() {
                var elements = document.querySelectorAll('.content-box');
                elements.forEach(function(element) {
                    if (isElementInViewport(element)) {
                        element.style.opacity = '1';

                        element.style.transform = 'translateY(0)';
                    }
                });
            }

            window.addEventListener('scroll', handleScroll);
            handleScroll(); // 初始检查
        </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main_page()