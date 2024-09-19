import streamlit as st
import json
import os

# Load users from configuration file
def load_users(file_path='users.json'):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"配置文件 {file_path} 不存在")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def display_personal_center(username, users):
    st.title("个人中心")

    user = users.get(username)
    if user:
        # 显示用户信息
        st.markdown("## 个人信息")
        st.write(f"**用户名:** {username}")
        st.write(f"**角色:** {user['role']}")

        # 更新密码部分
        with st.expander("更改密码", expanded=True):
            new_password = st.text_input("新密码", type="password")
            confirm_password = st.text_input("确认新密码", type="password")
            if st.button("更新密码"):
                if new_password and new_password == confirm_password:
                    user['password'] = new_password  # 明文存储不安全
                    with open('users.json', 'w', encoding='utf-8') as f:
                        json.dump(users, f, ensure_ascii=False, indent=4)
                    st.success("密码更新成功")
                elif new_password != confirm_password:
                    st.error("两次输入的密码不一致")
                else:
                    st.error("请输入新密码")

        # 用户日志（可选）
        with st.expander("活动日志", expanded=True):
            st.write("活动日志功能待实现")
    else:
        st.error("用户信息未找到")

# 确保用户已登录才能访问个人中心
if 'username' in st.session_state and st.session_state['username']:
    users = load_users()
    display_personal_center(st.session_state['username'], users)
else:
    st.error("用户未登录")
