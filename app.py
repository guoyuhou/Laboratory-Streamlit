import streamlit as st
import json
import os
from Cloud_storage import cloud_storage_page
import pygwalker
import pandas as pd
from pygwalker.api.streamlit import StreamlitRenderer
import base64
import requests
import logging
from user_manager import load_users, AuthManager
from page_manager import PageManager
from st_on_hover_tabs import on_hover_tabs
from PIL import Image
import folium
from streamlit_folium import folium_static

# 设置版本信息
VERSION = "1.0.0"

def main():
    st.set_page_config(
        page_title="Frontier Lab",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # 优化自定义CSS
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #f6f9fc, #e6eef7);
            font-family: 'Helvetica Neue', Arial, sans-serif;
        }
        .stButton>button {
            background-color: #4a90e2;
            color: white;
            border-radius: 25px;
            padding: 10px 20px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            border: none;
            box-shadow: 0 4px 6px rgba(50, 50, 93, 0.11), 0 1px 3px rgba(0, 0, 0, 0.08);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #357ae8;
            transform: translateY(-2px);
            box-shadow: 0 7px 14px rgba(50, 50, 93, 0.1), 0 3px 6px rgba(0, 0, 0, 0.08);
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            padding: 10px 15px;
            transition: all 0.3s ease;
        }
        .stTextInput>div>div>input:focus {
            border-color: #4a90e2;
            box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
            outline: none;
        }
        .sidebar .sidebar-content {
            background-color: #ffffff;
            box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
        }
        .stSelectbox {
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            overflow: hidden;
        }
        .stSelectbox > div > div > div {
            background-color: white;
        }
        .stCheckbox > label {
            font-weight: 500;
            color: #333;
        }
        .stMarkdown a {
            color: #4a90e2;
            text-decoration: none;
            border-bottom: 1px solid #4a90e2;
            transition: all 0.3s ease;
        }
        .stMarkdown a:hover {
            color: #357ae8;
            border-bottom: 2px solid #357ae8;
        }
        </style>
        """, unsafe_allow_html=True)

    # 显示logo
    st.logo('Images/sdu_logo2.jpg')

    users = load_users()
    auth_manager = AuthManager(users)

    if 'username' not in st.session_state:
        st.session_state.update({'username': None, 'role': None, 'login_page': False, 'edit_content': ''})

    if st.session_state['username'] is None:
        if st.session_state['login_page']:
            handle_login(auth_manager)
        else:
            home_page()  # 显示首页
            PageManager(None, users, auth_manager).display_pages()
            if st.sidebar.button("登录以访问更多内容", key="login_button"):
                st.session_state['login_page'] = True
    else:
        st.sidebar.success(f"欢迎回来，{st.session_state['username']}！")
        page_manager = PageManager(st.session_state['role'], users, auth_manager)
        page_manager.display_pages()
        dashboard()  # 显示仪表板

    # 美化侧边栏内容
    with st.sidebar:
        st.markdown("---")
        st.markdown(
            '<h6 style="text-align: center;">由 <img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16"> 强力驱动</h6>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="display: flex; justify-content: center; margin-top: 0.75em;"><a href="https://moderny-alexander.streamlit.app/" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="支持我们" height="41" width="174"></a></div>',
            unsafe_allow_html=True,
        )
        # 添加版本信息
        st.text(f"版本: {VERSION}")

def home_page():
    st.title("欢迎来到前沿实验室")
    st.write("我们致力于推动科技创新和前沿研究")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("研究方向")
        st.write("- 人工智能")
        st.write("- 量子计算")
        st.write("- 生物技术")
    with col2:
        st.subheader("最新动态")
        st.write("- 发表重要论文")
        st.write("- 获得重大科研项目")
        st.write("- 举办学术研讨会")
    with col3:
        st.subheader("合作伙伴")
        st.write("- 顶尖高校")
        st.write("- 知名企业")
        st.write("- 研究机构")

def team_page():
    st.title("团队成员")
    
    members = [
        {"name": "张教授", "title": "实验室主任", "image": "path/to/zhang.jpg"},
        {"name": "李博士", "title": "高级研究员", "image": "path/to/li.jpg"},
        {"name": "王工程师", "title": "技术专家", "image": "path/to/wang.jpg"},
    ]
    
    for member in members:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(member["image"], width=150)
        with col2:
            st.subheader(member["name"])
            st.write(member["title"])
            st.write("简介：...")  # 添加成员简介

def projects_page():
    st.title("研究项目")
    
    projects = [
        {"name": "智能机器人", "description": "开发新一代智能机器人系统", "image": "path/to/robot.jpg"},
        {"name": "量子通信", "description": "研究量子通信技术及其应用", "image": "path/to/quantum.jpg"},
        {"name": "基因编辑", "description": "探索CRISPR基因编辑技术", "image": "path/to/gene.jpg"},
    ]
    
    for project in projects:
        with st.expander(project["name"]):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(project["image"], width=200)
            with col2:
                st.write(project["description"])
                st.write("项目进展：...")  # 添加项目进展

def publications_page():
    st.title("发表论文")
    
    publications = [
        {"title": "人工智能在医疗诊断中的应用", "authors": "张三, 李四", "journal": "Nature", "year": 2023},
        {"title": "量子计算在密码学中的突破", "authors": "王五, 赵六", "journal": "Science", "year": 2022},
        {"title": "新型基因编辑技术的伦理考量", "authors": "刘七, 陈八", "journal": "Cell", "year": 2021},
    ]
    
    for pub in publications:
        st.write(f"**{pub['title']}**")
        st.write(f"作者：{pub['authors']}")
        st.write(f"发表于：{pub['journal']}, {pub['year']}")
        st.write("---")

def dashboard():
    st.title(f"欢迎回来，{st.session_state['username']}！")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("最新通知")
        st.info("下周三将举行实验室会议")
        st.info("新的研究项目申请截止日期：2023年12月31日")
    
    with col2:
        st.subheader("个人任务")
        st.success("完成实验报告")
        st.warning("准备下周的演讲")

    st.subheader("实验室资源使用情况")
    resource_usage = {
        "计算集群": 75,
        "存储空间": 60,
        "实验设备": 40
    }
    for resource, usage in resource_usage.items():
        st.write(f"{resource}：")
        st.progress(usage)

def contact_page():
    st.title("联系我们")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("联系方式")
        st.write("地址：XX市XX区XX路XX号")
        st.write("电话：123-456-7890")
        st.write("邮箱：contact@frontierlab.com")
    
    with col2:
        st.subheader("实验室位置")
        m = folium.Map(location=[31.2304, 121.4737], zoom_start=15)
        folium.Marker([31.2304, 121.4737], popup="前沿实验室").add_to(m)
        folium_static(m)

def handle_login(auth_manager):
    st.title("欢迎登录")
    st.write("请登录以访问更多精彩内容。")
    
    username = st.text_input("用户名", placeholder="请输入用户名", key="username_input")
    password = st.text_input("密码", type="password", placeholder="请输入密码", key="password_input")
    
    remember_me = st.checkbox("记住我")
    
    if st.button("登录", key="login_submit"):
        if username and password:
            user = auth_manager.authenticate_user(username, password)
            if user:
                st.balloons()
                st.success("登录成功！正在跳转...")
                st.session_state.update({'username': username, 'role': user['role'], 'login_page': False})
            else:
                st.error("用户名或密码无效")
        else:
            st.warning("用户名和密码不能为空")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("忘记密码？"):
            st.info("请联系管理员重置密码")
    with col2:
        if st.button("没有账号？注册"):
            st.info("请联系管理员创建新账号")

def handle_logout():
    st.session_state.update({'username': None, 'role': None, 'login_page': False})
    st.success("已退出登录")

if __name__ == "__main__":
    main()