import streamlit as st
from page_manager import PageManager
from auth_manager import AuthManager, load_users

def main():
    # 加载用户和权限管理
    users = load_users()
    auth_manager = AuthManager(users)

    # 用户登录（示例）
    st.sidebar.title("用户登录")
    username = st.sidebar.text_input("用户名")
    password = st.sidebar.text_input("密码", type='password')

    if st.sidebar.button("登录"):
        if auth_manager.authenticate(username, password):
            st.session_state['username'] = username
            role = users[username]['role']
            page_manager = PageManager(role, users, auth_manager)
            page_manager.display_pages()
        else:
            st.error("登录失败，请检查用户名和密码。")
    else:
        st.info("请登录以继续。")

if __name__ == "__main__":
    main()
