import streamlit as st

# 实验室主页
st.title('陈浩实验室')
st.write('__欢迎访问，这里是山东大学威海校区海洋学院陈浩老师实验室。__')

# 实验室简介
st.header('实验室简介')
st.write('本实验室专注于海洋科学的前沿研究，致力于海洋生态、环境保护及资源管理等领域。')

# 研究团队
st.header('研究团队')
team_members = {
    '陈浩': '实验室主任，研究方向：海洋生态学',
    '李四': '博士研究生，研究方向：海洋生物多样性',
    '王五': '硕士研究生，研究方向：海洋污染治理'
}

cols = st.columns(len(team_members))
for i, (member, description) in enumerate(team_members.items()):
    with cols[i]:
        st.subheader(member)
        st.write(description)

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

project_cols = st.columns(len(projects))
for i, project in enumerate(projects):
    with project_cols[i]:
        st.markdown(f"### {project['name']}")
        st.write(project['description'])
        st.write(f"[了解更多]({project['link']})")

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

paper_cols = st.columns(len(papers))
for i, paper in enumerate(papers):
    with paper_cols[i]:
        st.markdown(f"- [{paper['title']}]({paper['link']})")

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

# 添加样式
st.markdown("""
<style>
    .stHeader {font-size: 2.5rem;}
    .stSubheader {font-size: 2rem;}
    .stMarkdown {text-align: left;}
</style>
""", unsafe_allow_html=True)
