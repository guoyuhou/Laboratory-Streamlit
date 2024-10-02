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

# 自定义CSS样式和JavaScript动画
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

body {
    font-family: 'Roboto', sans-serif;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    color: #333;
}

.main {
    padding: 2rem;
    animation: fadeIn 0.5s ease-in-out;
}

.user-info {
    background-color: rgba(255, 255, 255, 0.9);
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.user-info:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
}

.section-title {
    color: #2c3e50;
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    border-bottom: 2px solid #3498db;
    padding-bottom: 0.5rem;
}

.info-item {
    margin-bottom: 1rem;
    font-size: 1.1rem;
}

.stExpander {
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.stExpander:hover {
    background-color: rgba(255, 255, 255, 1);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.stButton > button {
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 0.5rem 1rem;
    font-weight: 500;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background-color: #2980b9;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.activity-log {
    max-height: 200px;
    overflow-y: auto;
    padding-right: 10px;
}

.activity-item {
    padding: 0.5rem;
    border-left: 3px solid #3498db;
    margin-bottom: 0.5rem;
    background-color: rgba(255, 255, 255, 0.6);
    transition: all 0.2s ease;
}

.activity-item:hover {
    background-color: rgba(255, 255, 255, 0.9);
    transform: translateX(5px);
}

.project-progress {
    height: 10px;
    background-color: #ecf0f1;
    border-radius: 5px;
    overflow: hidden;
    margin-top: 0.5rem;
}

.progress-bar {
    height: 100%;
    background-color: #2ecc71;
    border-radius: 5px;
    transition: width 0.5s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

</style>

<script>
document.addEventListener('DOMContentLoaded', (event) => {
    // 添加淡入效果
    document.body.style.opacity = 0;
    let opacity = 0;
    let fadeIn = setInterval(() => {
        if (opacity >= 1) {
            clearInterval(fadeIn);
        }
        document.body.style.opacity = opacity;
        opacity += 0.1;
    }, 50);

    // 为用户信息卡片添加悬停效果
    const userInfo = document.querySelector('.user-info');
    userInfo.addEventListener('mouseover', () => {
        userInfo.style.transform = 'translateY(-5px)';
        userInfo.style.boxShadow = '0 15px 30px rgba(0, 0, 0, 0.2)';
    });
    userInfo.addEventListener('mouseout', () => {
        userInfo.style.transform = 'translateY(0)';
        userInfo.style.boxShadow = '0 10px 20px rgba(0, 0, 0, 0.1)';
    });

    // 为活动日志项添加动画效果
    const activityItems = document.querySelectorAll('.activity-item');
    activityItems.forEach(item => {
        item.addEventListener('mouseover', () => {
            item.style.transform = 'translateX(5px)';
            item.style.backgroundColor = 'rgba(255, 255, 255, 0.9)';
        });
        item.addEventListener('mouseout', () => {
            item.style.transform = 'translateX(0)';
            item.style.backgroundColor = 'rgba(255, 255, 255, 0.6)';
        });
    });

    // 为项目进度条添加动画效果
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
        }, 300);
    });
});
</script>
""", unsafe_allow_html=True)

# 显示个人中心页面
def display_personal_center(username, users):
    st.title("个人中心")

    user = users.get(username)
    if user:
        # 显示用户信息
        st.markdown('<div class="user-info">', unsafe_allow_html=True)
        st.markdown(f"<h2 class='section-title'>个人信息</h2>", unsafe_allow_html=True)
        st.markdown(f"<p class='info-item'><strong>用户名:</strong> {username}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='info-item'><strong>角色:</strong> {user['role']}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

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
            st.markdown('<div class="activity-log">', unsafe_allow_html=True)
            for activity in activities:
                st.markdown(f'<div class="activity-item">{activity}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # 项目进展
        with st.expander("项目进展", expanded=False):
            st.markdown('<h3 class="section-title">当前项目</h3>', unsafe_allow_html=True)
            projects = [
                {"name": "海洋生态系统研究", "progress": 75},
                {"name": "气候变化影响分析", "progress": 40}
            ]
            for project in projects:
                st.markdown(f"<h4>{project['name']}</h4>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class="project-progress">
                    <div class="progress-bar" style="width: {project['progress']}%;"></div>
                </div>
                <p>{project['progress']}% 完成</p>
                """, unsafe_allow_html=True)

    else:
        st.error("用户信息未找到")

# 确保用户已登录才能访问个人中心
if 'username' in st.session_state and st.session_state['username']:
    users = load_users()
    display_personal_center(st.session_state['username'], users)
else:
    st.error("用户未登录")
