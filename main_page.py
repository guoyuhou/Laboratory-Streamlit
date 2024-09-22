import streamlit as st
import plotly.express as px
import pandas as pd

# 设置页面标题
st.set_page_config(page_title="陈浩实验室", layout="wide")

# 背景动态效果
st.markdown("""
    <style>
        body {
            background-image: url('https://www.example.com/ocean_background.mp4');
            background-size: cover;
            background-position: center;
            height: 100vh;
            overflow: hidden;
        }
        .main-title {
            text-align: center;
            font-size: 3rem;
            color: #ffffff;
            padding: 20px;
            background-color: rgba(0, 45, 114, 0.7);
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        }
        .section {
            padding: 20px;
            border-radius: 10px;
            background-color: rgba(255, 255, 255, 0.8);
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            margin-top: 20px;
        }
        .nav {
            position: fixed;
            top: 0;
            width: 100%;
            background-color: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 10px;
            text-align: center;
            z-index: 1000;
        }
        .nav a {
            color: white;
            margin: 0 15px;
            text-decoration: none;
        }
        .team-member img {
            border-radius: 75px;
            transition: transform 0.2s;
        }
        .team-member img:hover {
            transform: scale(1.1);
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
        <a href="#反馈">反馈</a>
    </div>
""", unsafe_allow_html=True)

# 实验室标题
st.markdown('<h1 class="main-title">陈浩实验室</h1>', unsafe_allow_html=True)

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

# 选择数据视图
view_type = st.selectbox("选择数据视图", ["趋势图", "柱状图"])

if view_type == "趋势图":
    fig = px.line(data, x='时间', y='研究成果', title='实验室研究成果趋势', markers=True)
else:
    fig = px.bar(data, x='时间', y='研究成果', title='实验室研究成果柱状图')

st.plotly_chart(fig)

# 研究团队
st.header('研究团队')
st.markdown('<div class="section" id="研究团队"></div>', unsafe_allow_html=True)

team_members = {
    '陈浩': {
        'description': '实验室主任，研究方向：海洋生态学',
        'image': 'https://via.placeholder.com/150?text=陈浩'
    },
    '李四': {
        'description': '博士研究生，研究方向：海洋生物多样性',
        'image': 'https://via.placeholder.com/150?text=李四'
    },
    '王五': {
        'description': '硕士研究生，研究方向：海洋污染治理',
        'image': 'https://via.placeholder.com/150?text=王五'
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
    st.write(f"**{key}**: {value}")

# 新闻与更新
st.header('新闻与更新')
st.markdown('<div class="section" id="新闻与更新"></div>', unsafe_allow_html=True)

updates = [
    '2024年1月：实验室获得国家自然科学基金支持。',
    '2024年2月：实验室成员参加国际海洋会议。'
]
for update in updates:
    st.write(f"- {update}")

# 反馈区域
st.header('反馈')
st.markdown('<div class="section" id="反馈"></div>', unsafe_allow_html=True)

feedback = st.text_area("请留下您的反馈意见：")
if st.button("提交"):
    if feedback:
        st.success("感谢您的反馈！")
    else:
        st.warning("反馈不能为空。")

# 页脚
st.markdown('<div class="footer" style="text-align: center; padding: 20px; background-color: #002d72; color: #ffffff;">© 2024 陈浩实验室. 保留所有权利.</div>', unsafe_allow_html=True)
