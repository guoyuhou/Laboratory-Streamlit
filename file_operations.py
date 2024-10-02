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
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    body {
        font-family: 'Roboto', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #333;
    }
    
    .stApp {
        background-color: transparent;
    }
    
    .main .block-container {
        padding: 2rem;
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .main .block-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
    }
    
    .stButton>button {
        background-color: #4a90e2;
        color: white;
        border-radius: 25px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(74, 144, 226, 0.2);
    }
    
    .stButton>button:hover {
        background-color: #357ae8;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(74, 144, 226, 0.3);
    }
    
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #4a90e2;
        box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
    }
    
    .sidebar .sidebar-content {
        background-color: rgba(248, 249, 250, 0.9);
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stSelectbox {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
    }
    
    .stMarkdown a {
        color: #4a90e2;
        text-decoration: none;
        transition: all 0.2s ease;
    }
    
    .stMarkdown a:hover {
        color: #357ae8;
        text-decoration: underline;
    }
    
    /* 添加动画效果 */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .main {
        animation: fadeIn 0.5s ease-in-out;
    }
    
    </style>
    
    <script>
    document.addEventListener('DOMContentLoaded', (event) => {
        // 为按钮添加点击动画
        const buttons = document.querySelectorAll('button');
        buttons.forEach(button => {
            button.addEventListener('click', function() {
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                }, 200);
            });
        });
    
        // 为输入框添加焦点动画
        const inputs = document.querySelectorAll('input[type="text"]');
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.style.transform = 'translateY(-2px)';
                this.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
            });
            input.addEventListener('blur', function() {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = 'none';
            });
        });
    
        // 为页面元素添加滚动显示动画
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, { threshold: 0.1 });
    
        document.querySelectorAll('.main > div > div').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            observer.observe(el);
        });
    });
    </script>
""", unsafe_allow_html=True)
