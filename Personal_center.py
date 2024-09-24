import streamlit as st
import json
import os
from PIL import Image
import base64

# 加载用户配置文件
def load_users(file_path='users.json'):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"配置文件 {file_path} 不存在")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 自定义CSS样式


# 显示个人中心页面
def display_personal_center(username, users):
    st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
    }
    .user-info {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .section-title {
        color: #1f77b4;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .info-item {
        margin-bottom: 0.5rem;
    }
    .stExpander {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("个人中心")

    user = users.get(username)
    if user:
        # 显示用户信息
        st.markdown("## 个人信息")
        st.write(f"**用户名:** {username}")
        st.write(f"**角色:** {user['role']}")

        # 更新密码部分
        with st.expander("更改密码", expanded=False):
            new_password = st.text_input("新密码", type="password")
            confirm_password = st.text_input("确认新密码", type="password")
            if st.button("更新密码"):
                if new_password and new_password == confirm_password:
                    user['password'] = new_password  # 注意：实际应用中应使用加密存储
                    with open('users.json', 'w', encoding='utf-8') as f:
                        json.dump(users, f, ensure_ascii=False, indent=4)
                    st.success("密码更新成功")
                elif new_password != confirm_password:
                    st.error("两次输入的密码不一致")
                else:
                    st.error("请输入新密码")

        # 用户活动日志
        with st.expander("活动日志", expanded=False):
            st.markdown('<h3 class="section-title">最近活动</h3>', unsafe_allow_html=True)
            activities = [
                "2024-03-15: 登录系统",
                "2024-03-14: 更新个人信息",
                "2024-03-13: 上传新文件"
            ]
            for activity in activities:
                st.markdown(f"- {activity}")

        # 项目进展
        with st.expander("项目进展", expanded=False):
            st.markdown('<h3 class="section-title">当前项目</h3>', unsafe_allow_html=True)
            projects = [
                {"name": "海洋生态系统研究", "progress": 75},
                {"name": "气候变化影响分析", "progress": 40}
            ]
            for project in projects:
                st.markdown(f"**{project['name']}**")
                st.progress(project['progress'])

    else:
        st.error("用户信息未找到")

# 确保用户已登录才能访问个人中心
if 'username' in st.session_state and st.session_state['username']:
    users = load_users()
    display_personal_center(st.session_state['username'], users)
else:
    st.error("用户未登录")
