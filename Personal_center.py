import streamlit as st
from app import get_db_connection, hash_password

def display_personal_center(username):
    st.title("个人中心")
    
    conn = get_db_connection()
    
    # 查询用户信息
    user = conn.execute('SELECT username, role, email, phone FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    
    if user:
        st.write(f"用户名: {user['username']}")
        st.write(f"角色: {user['role']}")
        st.write(f"邮箱: {user['email']}")
        st.write(f"电话: {user['phone']}")
        
        st.subheader("更新个人信息")
        new_email = st.text_input("新邮箱", value=user['email'])
        new_phone = st.text_input("新电话", value=user['phone'])
        
        if st.button("更新信息"):
            if new_email and new_phone:
                conn = get_db_connection()
                conn.execute('UPDATE users SET email = ?, phone = ? WHERE username = ?',
                             (new_email, new_phone, username))
                conn.commit()
                conn.close()
                st.success("个人信息更新成功")
            else:
                st.error("邮箱和电话不能为空")
        
        st.subheader("更改密码")
        new_password = st.text_input("新密码", type="password")
        confirm_password = st.text_input("确认新密码", type="password")
        
        if st.button("更新密码"):
            if new_password and new_password == confirm_password:
                hashed_password = hash_password(new_password)
                conn = get_db_connection()
                conn.execute('UPDATE users SET password = ? WHERE username = ?',
                             (hashed_password, username))
                conn.commit()
                conn.close()
                st.success("密码更新成功")
            elif new_password != confirm_password:
                st.error("两次输入的密码不一致")
            else:
                st.error("请输入新密码")
        
        st.subheader("账户注销")
        if st.button("注销账户"):
            conn = get_db_connection()
            conn.execute('DELETE FROM users WHERE username = ?', (username,))
            conn.commit()
            conn.close()
            st.success("账户注销成功")
            st.session_state['username'] = None
            st.session_state['role'] = None
            st.write("正在重定向到登录页面...")
            st.experimental_rerun()
        
        # 用户日志（可选）
        st.subheader("活动日志")
        # 这里假设有一个用户日志表，你可以自定义日志内容
        # logs = conn.execute('SELECT * FROM user_logs WHERE username = ?', (username,)).fetchall()
        # for log in logs:
        #     st.write(f"{log['timestamp']}: {log['activity']}")
    else:
        st.error("用户信息未找到")

if 'username' in st.session_state and st.session_state['username']:
    display_personal_center(st.session_state['username'])
else:
    st.error("用户未登录")
