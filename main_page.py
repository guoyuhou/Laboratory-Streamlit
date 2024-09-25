import streamlit as st
import plotly.express as px
import pandas as pd
import json
import streamlit as st
import plotly.express as px
import pandas as pd
import json
from PIL import Image
import numpy as np

@st.cache
def load_data():
    # 示例数据
    return pd.DataFrame({
        '时间': ['2023-01', '2023-02', '2023-03', '2023-04'],
        '研究成果': [10, 20, 15, 25]
    })

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

    # 添加粒子效果
    st.markdown("""
        <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
        <div id="particles-js" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;"></div>
        <script>
            particlesJS("particles-js", {
                "particles": {
                    "number": {"value": 80},
                    "color": {"value": "#ffffff"},
                    "shape": {"type": "circle"},
                    "opacity": {"value": 0.5, "random": true},
                    "size": {"value": 3, "random": true},
                    "move": {"enable": true, "speed": 1}
                }
            });
        </script>
    """, unsafe_allow_html=True)

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

    # 实验室宣传片
    st.video('videos/elon_mask.mp4')

    st.markdown("""
        <div style='text-align: center; font-size: 20px; font-weight: bold;'>
            向未知之境的探索者致敬<br>
        </div>
    """, unsafe_allow_html=True)

    # 添加交互式3D地球模型
    st.markdown("""
        <div id="earth-container" style="width: 100%; height: 400px;"></div>
        <script src="https://www.webglearth.com/v2/api.js"></script>
        <script>
            var earth = new WE.map('earth-container');
            WE.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(earth);
            earth.setView([0, 0], 2.5);
            
            // 添加实验室位置标记
            var marker = WE.marker([36.0, 120.3]).addTo(earth);
            marker.bindPopup("<b>Cosmos Lab</b><br>青岛", {maxWidth: 120, closeButton: true});

            // 添加动画效果
            (function animate() {
                requestAnimationFrame(animate);
                earth.setCenter([36.0 + Math.random() * 0.1, 120.3 + Math.random() * 0.1]);
            }());
        </script>
    """, unsafe_allow_html=True)

    # 动态数据图表
    st.markdown('<h2 class="section-title">实时数据展示</h2>', unsafe_allow_html=True)
    st.markdown('<div class="section" id="实时数据展示"></div>', unsafe_allow_html=True)

    data = load_data()
    fig = px.line(data, x='时间', y='研究成果', title='实验室研究成果趋势', markers=True)
    st.plotly_chart(fig)

    # 添加实时海洋数据展示
    st.markdown('<h2 class="section-title">实时海洋数据</h2>', unsafe_allow_html=True)
    
    # 模拟实时数据
    ocean_data = pd.DataFrame({
        '时间': pd.date_range(start='2024-01-01', periods=24, freq='H'),
        '温度': np.random.normal(20, 2, 24),
        '盐度': np.random.normal(35, 0.5, 24),
        '溶解氧': np.random.normal(7, 0.3, 24)
    })
    
    fig = px.line(ocean_data, x='时间', y=['温度', '盐度', '溶解氧'], 
                  title='实时海洋环境数据',
                  labels={'value': '数值', 'variable': '参数'})
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

    # 添加团队成员互动功能
    for member, info in team_members.items():
        with st.expander(f"了解更多关于 {member}"):
            st.write(info['description'])
            st.write("研究兴趣:")
            st.write("- 海洋生态系统")
            st.write("- 海洋污染治理")
            st.write("- 海洋资源可持续利用")
            if st.button(f"联系 {member}"):
                st.success(f"已发送邮件给 {member}！")

    # 修改研究项目展示
    st.markdown('<h2 class="section-title">研究项目</h2>', unsafe_allow_html=True)
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

    # 添加交互式项目时间线
    st.markdown('<h2 class="section-title">项目时间线</h2>', unsafe_allow_html=True)
    timeline_data = [
        {"项目": "深海生态系统探索", "开始": "2023-01-01", "结束": "2024-12-31"},
        {"项目": "海洋微塑料污染研究", "开始": "2023-06-01", "结束": "2025-05-31"},
        {"项目": "海洋生物多样性调查", "开始": "2024-03-01", "结束": "2026-02-28"}
    ]
    fig = px.timeline(timeline_data, x_start="开始", x_end="结束", y="项目", color="项目")
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig)

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

    # 添加论文引用统计
    st.markdown('<h3>论文引用统计</h3>', unsafe_allow_html=True)
    citations_data = pd.DataFrame({
        '论文': ['海洋生态学的现状与展望', '海洋污染治理的新方法'],
        '引用次数': [120, 85]
    })
    fig = px.bar(citations_data, x='论文', y='引用次数', title='论文引用统计')
    st.plotly_chart(fig)

    # 联系方式
    st.markdown('<h2 class="section-title">联系方式</h2>', unsafe_allow_html=True)
    st.markdown('<div class="section" id="联系方式"></div>', unsafe_allow_html=True)

    contact_info = {
        'Email': 'chenh@mail.sdu.edu.cn',
        '电话': '+86 123 456 7890',
        '社交媒体': '[Twitter](https://twitter.com/example), [ResearchGate](https://www.researchgate.net/)'
    }

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

    # 添加互动式实验室参观
    st.markdown('<h2 class="section-title">虚拟实验室参观</h2>', unsafe_allow_html=True)
    st.markdown("""
        <div style="width: 100%; height: 400px; background-color: #f0f0f0; display: flex; justify-content: center; align-items: center;">
            <p style="font-size: 24px;">这里将是一个360度全景虚拟实验室参观</p>
        </div>
    """, unsafe_allow_html=True)
    st.write("正在开发中，敬请期待！")

    # 新闻与更新
    st.markdown('<h2 class="section-title">新闻与更新</h2>', unsafe_allow_html=True)
    st.markdown('<div class="section" id="新闻与更新"></div>', unsafe_allow_html=True)

    updates = [
        '2024年1月：实验室获得国家自然科学基金支持。',
        '2024年2月：实验室成员参加国际海洋会议。'
    ]
    for update in updates:  
        st.write(f"- {update}")

    # 添加订阅功能
    st.markdown('<h2 class="section-title">订阅我们的通讯</h2>', unsafe_allow_html=True)
    email = st.text_input("输入您的邮箱地址")
    if st.button("订阅"):
        st.success("感谢您的订阅！")

    # 改进页脚
    st.markdown("""
        <div class="footer">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>© 2024 陈浩实验室. 保留所有权利.</div>
                <div>
                    <a href="#" style="color: white; margin-right: 10px;">隐私政策</a>
                    <a href="#" style="color: white;">使用条款</a>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
