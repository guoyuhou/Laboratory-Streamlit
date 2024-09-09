import streamlit as st
from app import get_db_connection, hash_password  # 从 app.py 导入所需函数

def display_personal_center(username):
    st.title("个人中心")
    
    conn = get_db_connection()
    user = conn.execute('SELECT username, role FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    
    if user:
        st.write(f"用户名: {user['username']}")
        st.write(f"角色: {user['role']}")
        
        st.subheader("更改信息")
        new_password = st.text_input("新密码", type="password")
        if st.button("更新密码"):
            if new_password:
                hashed_password = hash_password(new_password)
                conn = get_db_connection()
                conn.execute('UPDATE users SET password = ? WHERE username = ?',
                             (hashed_password, username))
                conn.commit()
                conn.close()
                st.success("密码更新成功")
            else:
                st.error("请输入新密码")
    else:
        st.error("用户信息未找到")

if 'username' in st.session_state and st.session_state['username']:
    display_personal_center(st.session_state['username'])
else:
    st.error("用户未登录")
