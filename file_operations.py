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

def upload_github_file(repo, path, content, message):
    url = f"{GITHUB_API_URL}/repos/{repo}/contents/{path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    data = {
        "message": message,
        "content": base64.b64encode(content.encode()).decode()
    }

    try:
        with st.spinner("正在上传文件..."):
            response = requests.put(url, headers=headers, json=data)
            response.raise_for_status()
            st.success("文件上传成功", icon="✅")
            logging.info("文件上传成功")
            return True
    except requests.exceptions.HTTPError as e:
        st.error(f"上传失败: {e.response.status_code} - {e.response.json().get('message', '未知错误')}", icon="❌")
        logging.error(f"上传错误: {e}")
        return False

# 美化界面
st.set_page_config(page_title="实验室文件管理系统", page_icon="📁", layout="wide")

st.title("实验室文件管理系统")
st.markdown("---")

# 使用标签页来组织内容
tab1, tab2, tab3 = st.tabs(["查看文件", "上传文件", "更新文件"])

with tab1:
    st.header("查看文件")
    file_path = st.text_input("输入文件路径（例如：docs/file.md）")
    if st.button("查看文件"):
        file_data = get_github_file(GITHUB_REPO, file_path)
        if file_data:
            content = base64.b64decode(file_data['content']).decode("utf-8")
            st.code(content, language="markdown")

with tab2:
    st.header("上传文件")
    uploaded_file = st.file_uploader("选择一个文件上传到GitHub", type=["md", "txt", "pdf"])
    if uploaded_file is not None:
        file_content = uploaded_file.read().decode("utf-8")
        file_path = st.text_input("输入文件路径（例如：docs/new_file.md）")
        commit_message = st.text_input("输入提交信息")
        if st.button("上传文件"):
            if upload_github_file(GITHUB_REPO, file_path, file_content, commit_message):
                st.success("文件上传成功", icon="✅")
            else:
                st.error("文件上传失败", icon="❌")

with tab3:
    st.header("更新文件")
    file_path = st.text_input("输入文件路径（例如：docs/file.md）", key="update_path")
    new_content = st.text_area("输入新的文件内容")
    commit_message = st.text_input("输入提交信息", key="update_message")
    if st.button("更新文件"):
        if update_github_file(GITHUB_REPO, file_path, new_content, commit_message):
            st.success("文件更新成功", icon="✅")
        else:
            st.error("文件更新失败", icon="❌")
