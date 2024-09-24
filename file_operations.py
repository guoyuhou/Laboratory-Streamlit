import requests
import base64
import json
import logging
import streamlit as st

# GitHub API 设置
GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = st.secrets["oss"]["GITHUB_TOKEN"]
GITHUB_REPO = st.secrets["oss"]["GITHUB_REPO"]

logging.basicConfig(level=logging.INFO)

def get_github_file(repo, path):
    url = f"{GITHUB_API_URL}/repos/{repo}/contents/{path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"无法获取文件: {response.json().get('message')}")
        return None

def update_github_file(repo, path, content, message):
    url = f"{GITHUB_API_URL}/repos/{repo}/contents/{path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    file_data = get_github_file(repo, path)
    if not file_data:
        st.error("无法获取文件信息，更新操作无法继续。")
        return False

    sha = file_data['sha']
    data = {
        "message": message,
        "content": base64.b64encode(content.encode()).decode(),
        "sha": sha
    }

    try:
        with st.spinner("正在更新文件..."):
            response = requests.put(url, headers=headers, json=data)
            response.raise_for_status()
            st.success("文件更新成功")
            logging.info("文件更新成功")
            return True
    except requests.exceptions.HTTPError as e:
        st.error(f"更新失败: {e.response.status_code} - {e.response.json().get('message', '未知错误')}")
        logging.error(f"更新错误: {e}")
        return False

def edit_markdown(repo, file_path):
    file_data = get_github_file(repo, file_path)
    if file_data:
        content = base64.b64decode(file_data['content']).decode("utf-8")
        return content
    return None

# 美化Streamlit页面
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background-color: #4a90e2;
        color: white;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #357ae8;
    }
    .stTextInput>div>div>input {
        border-radius: 4px;
        border: 1px solid #e0e0e0;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .stSelectbox {
        border-radius: 4px;
        border: 1px solid #e0e0e0;
    }
    .stMarkdown a {
        color: #4a90e2;
        text-decoration: none;
    }
    .stMarkdown a:hover {
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)
