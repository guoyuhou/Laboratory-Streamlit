import streamlit as st
import plotly.express as px
import pandas as pd

# 背景动态效果
st.markdown("""
    <style>
        body {
            background: linear-gradient(to bottom, rgba(0, 45, 114, 0.8), rgba(255, 255, 255, 0.8)), url('https://www.example.com/ocean_background.jpg');
            background-size: cover;
            height: 100vh;
            overflow: hidden;
            animation: backgroundAnimation 30s ease infinite;
        }

        @keyframes backgroundAnimation {
            0% { background-position: 0% 50%; }
            100% { background-position: 100% 50%; }
        }

        .main-title {
            text-align: center;
            font-size: 3rem;
            color: #ffffff;
            padding: 20px;
            background-color: rgba(0, 45, 114, 0.8);
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
            margin-top: 20px;
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
    </style>
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
st.markdown('<h1 class="main-title" style="margin-top: 10px;">Frontier Lab</h1>', unsafe_allow_html=True)

# 实验室简介
st.header('实验室简介')
st.markdown("""
    <div class="section" id="实验室简介">
        <p>本实验室专注于海洋科学的前沿研究，致力于海洋生态、环境保护及资源管理等领域。我们通过多学科的合作，推动科学研究和技术创新。</p>
    </div>
""", unsafe_allow_html=True)

# 动态数据图表
st.header('实时数据展示')
st.markdown('<div class="section" id="实时数据展示"></div>', unsafe_allow_html=True)

# 示例数据
data = pd.DataFrame({
    '时间': ['2023-01', '2023-02', '2023-03', '2023-04'],
    '研究成果': [10, 20, 15, 25]
})

# 只保留折线图
fig = px.line(data, x='时间', y='研究成果', title='实验室研究成果趋势', markers=True)
st.plotly_chart(fig)

# 研究团队
st.header('研究团队')
st.markdown('<div class="section" id="研究团队"></div>', unsafe_allow_html=True)

team_members = {
    '陈浩': {
        'description': '实验室主任，研究方向:(1)海洋天然产物开发,(2)功能性食品技术(3)营养/药物递送体系构建及传质规律研究',
        'image': 'Images/example1.jpg'
    },
    '王普': {
        'description': '博士研究生，研究方向：海洋生物多样性',
        'image': 'https://www.bing.com/images/search?view=detailV2&ccid=IFLzeDgH&id=BE43D136CC57CD35C51FA21C1B77AD355914388C&thid=OIP.IFLzeDgHm6qo85f0AkzqUwHaJ3&mediaurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.2052f37838079baaa8f397f4024cea53%3frik%3djDgUWTWtdxscog%26riu%3dhttp%253a%252f%252fweb4708.w2.magic2008.cn%252fuFile%252f4708%252fproduct%252f201282215326422.jpg%26ehk%3dtW5hCMOv1Z0YmsqyDfZyG066dmsFB4HaeYrNG4CKb5g%253d%26risl%3d%26pid%3dImgRaw%26r%3d0&exph=666&expw=500&q=%e5%bd%ad%e4%ba%8e%e6%99%8f&simid=608027620347943218&FORM=IRPRST&ck=615E42CC409B18A0EB4B485E23973D0F&selectedIndex=53&itb=0'
    },
    '王淑新': {
        'description': '硕士研究生，研究方向：海洋污染治理',
        'image': 'https://via.placeholder.com/150?text=王淑欣'
    },
    'bro': {
        'description': '硕士研究生，研究方向：海洋污染治理',
        'image': 'https://via.placeholder.com/150?text=王淑欣'
    }
}

# 创建团队成员展示
cols = st.columns(len(team_members))
for i, (member, info) in enumerate(team_members.items()):
    with cols[i]:
        st.markdown(f'<div class="team-member"><img src="{info["image"]}" alt="{member}" /><br><strong>{member}</strong><br>{info["description"]}</div>', unsafe_allow_html=True)

# 研究项目
st.header('研究项目')
st.markdown('<div class="section" id="研究项目"></div>', unsafe_allow_html=True)

projects = [
    {
        'name': '海洋生态系统恢复',
        'description': '研究海洋生态系统的恢复过程及其对环境的影响。',
        'link': 'https://example.com/project1'
    },
    {
        'name': '海洋污染监测',
        'description': '开发新的监测技术以评估海洋污染情况。',
        'link': 'https://example.com/project2'
    }
]

for project in projects:
    st.markdown(f"""
        <div class="section">
            <h3>{project['name']}</h3>
            <p>{project['description']}</p>
            <a href="{project['link']}">了解更多</a>
        </div>
    """, unsafe_allow_html=True)

# 发表论文
st.header('发表论文')
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
st.header('联系方式')
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

# 新闻与更新
st.header('新闻与更新')
st.markdown('<div class="section" id="新闻与更新"></div>', unsafe_allow_html=True)

updates = [
    '2024年1月：实验室获得国家自然科学基金支持。',
    '2024年2月：实验室成员参加国际海洋会议。'
]
for update in updates:
    st.write(f"- {update}")

# 页脚
st.markdown('<div class="footer">© 2024 陈浩实验室. 保留所有权利.</div>', unsafe_allow_html=True)
