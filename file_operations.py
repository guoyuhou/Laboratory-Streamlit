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
        st.error(f"无法获取文件: {response.json().get('message')}", icon="❌")
        return None

def update_github_file(repo, path, content, message):
    url = f"{GITHUB_API_URL}/repos/{repo}/contents/{path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    file_data = get_github_file(repo, path)
    if not file_data:
        st.error("无法获取文件信息，更新操作无法继续。", icon="❌")
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
            st.success("文件更新成功", icon="✅")
            logging.info("文件更新成功")
            return True
    except requests.exceptions.HTTPError as e:
        st.error(f"更新失败: {e.response.status_code} - {e.response.json().get('message', '未知错误')}", icon="❌")
        logging.error(f"更新错误: {e}")
        return False

def edit_markdown(repo, file_path):
    file_data = get_github_file(repo, file_path)
    if file_data:
        content = base64.b64decode(file_data['content']).decode("utf-8")
        return content
    return None

# 美化界面
st.set_page_config(page_title="实验室文件管理系统", page_icon="📁", layout="wide")

st.markdown("""
<style>
    .reportview-container {
        background: linear-gradient(to right, #f0f2f6, #e6e9ef);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(to bottom, #2e7bcf, #2a71b8);
        color: white;
    }
    .Widget>label {
        color: #1f4b77;
        font-weight: bold;
    }
    .stButton>button {
        color: #ffffff;
        background-color: #2e7bcf;
        border-radius: 5px;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #1f4b77;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .stAlert {
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

st.title("实验室文件管理系统")
st.markdown("---")
