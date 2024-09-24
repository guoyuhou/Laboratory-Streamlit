import streamlit as st
import json
import os
from PIL import Image
import base64

# 自定义CSS样式
def load_css():
    st.markdown("""
    <style>
    .personal-center {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .user-info {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }
    .section-title {
        color: #1f77b4;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    .info-item {
        margin-bottom: 0.5rem;
    }
    .stExpander {
        background-color: white;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 加载用户数据
def load_users(file_path='users.json'):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"配置文件 {file_path} 不存在")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 显示个人中心
def display_personal_center(username, users):
    load_css()
    st.title("个人中心")

    user = users.get(username)
    if user:
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # 显示用户头像
            image = Image.open("path_to_default_avatar.png")  # 替换为实际的默认头像路径
            st.image(image, width=150)
        
        with col2:
            st.markdown('<div class="personal-center">', unsafe_allow_html=True)
            
            # 用户信息部分
            st.markdown('<div class="user-info">', unsafe_allow_html=True)
            st.markdown('<h2 class="section-title">个人信息</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="info-item"><strong>用户名:</strong> {username}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="info-item"><strong>角色:</strong> {user["role"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="info-item"><strong>邮箱:</strong> {user.get("email", "未设置")}</p>', unsafe_allow_html=True)
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
            
            # 用户统计信息
            with st.expander("统计信息", expanded=False):
                st.markdown('<h3 class="section-title">活跃度</h3>', unsafe_allow_html=True)
                st.progress(0.8)  # 示例进度条
                st.markdown('<h3 class="section-title">贡献度</h3>', unsafe_allow_html=True)
                st.progress(0.6)  # 示例进度条
            
            # 活动日志
            with st.expander("活动日志", expanded=False):
                st.markdown('<h3 class="section-title">最近活动</h3>', unsafe_allow_html=True)
                st.write("2024-03-15: 登录系统")
                st.write("2024-03-14: 更新个人信息")
                st.write("2024-03-13: 上传新文件")
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("用户信息未找到")

# 确保用户已登录才能访问个人中心
if 'username' in st.session_state and st.session_state['username']:
    users = load_users()
    display_personal_center(st.session_state['username'], users)
else:
    st.error("用户未登录")
