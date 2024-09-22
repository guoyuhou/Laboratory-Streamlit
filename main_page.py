import streamlit as st

# 设置页面标题
st.set_page_config(page_title="陈浩实验室", layout="wide")

# 实验室主页
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 3rem;
            color: #ffffff;
            padding: 20px;
            background-color: #002d72; /* 深蓝色背景 */
            border-radius: 10px;
        }
        .subtitle {
            text-align: center;
            font-size: 1.5rem;
            color: #ffffff;
            margin-bottom: 40px;
        }
        .section {
            padding: 20px;
            border-radius: 10px;
            background-color: #f4f4f4; /* 浅灰背景 */
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        .team-member {
            text-align: center;
            margin: 20px;
        }
        .project, .paper {
            margin: 20px 0;
            padding: 10px;
            border-radius: 10px;
            background-color: #ffffff; /* 白色背景 */
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .footer {
            text-align: center;
            padding: 20px;
            background-color: #002d72;
            color: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)

# 实验室标题和欢迎语
st.markdown('<h1 class="main-title">陈浩实验室</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">欢迎访问山东大学威海校区海洋学院陈浩老师实验室</p>', unsafe_allow_html=True)

# 实验室简介
st.header('实验室简介')
st.markdown("""
    <div class="section">
        <p>本实验室专注于海洋科学的前沿研究，致力于海洋生态、环境保护及资源管理等领域。</p>
    </div>
""", unsafe_allow_html=True)

# 研究团队
st.header('研究团队')
team_members = {
    '陈浩': {
        'description': '实验室主任，研究方向：海洋生态学',
        'image': 'https://via.placeholder.com/150?text=陈浩'  # 示例图片链接
    },
    '李四': {
        'description': '博士研究生，研究方向：海洋生物多样性',
        'image': 'https://via.placeholder.com/150?text=李四'  # 示例图片链接
    },
    '王五': {
        'description': '硕士研究生，研究方向：海洋污染治理',
        'image': 'https://via.placeholder.com/150?text=王五'  # 示例图片链接
    }
}

# 创建团队成员展示
cols = st.columns(len(team_members))
for i, (member, info) in enumerate(team_members.items()):
    with cols[i]:
        st.markdown(f'<div class="team-member"><img src="{info["image"]}" alt="{member}" style="border-radius: 75px;" /><br><strong>{member}</strong><br>{info["description"]}</div>', unsafe_allow_html=True)

# 研究项目
st.header('研究项目')
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
        <div class="project">
            <h3>{project['name']}</h3>
            <p>{project['description']}</p>
            <a href="{project['link']}">了解更多</a>
        </div>
    """, unsafe_allow_html=True)

# 发表论文
st.header('发表论文')
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
        <div class="paper">
            <p><a href="{paper['link']}">{paper['title']}</a></p>
        </div>
    """, unsafe_allow_html=True)

# 联系方式
st.header('联系方式')
contact_info = {
    'Email': 'chenh@mail.sdu.edu.cn',
    '电话': '+86 123 456 7890',
    '社交媒体': '[Twitter](https://twitter.com/example), [ResearchGate](https://www.researchgate.net/)'
}

for key, value in contact_info.items():
    st.write(f"**{key}**: {value}")

# 新闻与更新
st.header('新闻与更新')
updates = [
    '2024年1月：实验室获得国家自然科学基金支持。',
    '2024年2月：实验室成员参加国际海洋会议。'
]
for update in updates:
    st.write(f"- {update}")

# 页脚
st.markdown('<div class="footer">© 2024 陈浩实验室. 保留所有权利.</div>', unsafe_allow_html=True)
