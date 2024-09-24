import streamlit as st
import oss2
import zipfile
import io
from pdf2image import convert_from_path
import logging
import random
from datetime import datetime, timedelta
import pandas as pd

# 设置日志
logging.basicConfig(level=logging.INFO)

# 从Streamlit的Secrets中读取OSS的密钥和存储桶信息
ACCESS_KEY_ID = st.secrets["oss"]["ACCESS_KEY_ID"]
ACCESS_KEY_SECRET = st.secrets["oss"]["ACCESS_KEY_SECRET"]
ENDPOINT = st.secrets["oss"]["ENDPOINT"]
BUCKET_NAME = st.secrets["oss"]["BUCKET_NAME"]

# 创建OSS认证和存储桶对象
auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, ENDPOINT, BUCKET_NAME)

def list_files():
    """列出OSS中的所有文件"""
    return [obj.key for obj in oss2.ObjectIterator(bucket)]

# 用于记录操作日志
operation_log = []

def handle_file(file, operation):
    """处理文件上传和更新"""
    try:
        bucket.put_object(file.name, file)
        st.success(f'文件 {file.name} {operation} 成功', icon="✅")
    except Exception as e:
        logging.error(f'操作文件 {file.name} 时出错: {e}')
        st.error(f'操作文件时出错: {e}')

def upload_zip_file(uploaded_file):
    """处理ZIP文件上传"""
    try:
        with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
            total_files = len(zip_ref.infolist())
            progress_bar = st.progress(0)
            for i, file_info in enumerate(zip_ref.infolist(), start=1):
                file_data = zip_ref.read(file_info.filename)
                bucket.put_object(file_info.filename, file_data)
                progress_bar.progress(i / total_files)
                st.write(f'文件 {file_info.filename} 上传成功')
        st.success('ZIP文件中的所有文件已成功上传到 OSS', icon="✅")
    except Exception as e:
        logging.error(f'处理ZIP文件时出错: {e}')
        st.error(f'处理ZIP文件时出错: {e}')

def cloud_storage_page(username=None):
    """显示云存储页面"""
    st.set_page_config(layout="wide")
    
    # 自定义CSS样式
    st.markdown("""
    <style>
    .main {
        background-color: #f0f2f5;
        padding: 2rem;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .file-card {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
    }
    .file-icon {
        font-size: 2rem;
        margin-right: 1rem;
    }
    .file-info {
        display: flex;
        align-items: center;
    }
    .file-actions {
        display: flex;
        justify-content: flex-end;
    }
    .btn-action {
        margin-left: 0.5rem;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        border: none;
        cursor: pointer;
    }
    .btn-download {
        background-color: #4CAF50;
        color: white;
    }
    .btn-delete {
        background-color: #f44336;
        color: white;
    }
    .upload-area {
        border: 2px dashed #ddd;
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("实验室云存储")
    
    if username:
        st.write(f"欢迎回来，{username}！")
    
    # 创建两列布局
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("我的文件")
        files = list_files()
        for file in files:
            with st.container():
                st.markdown(f"""
                <div class="file-card">
                    <div class="file-info">
                        <span class="file-icon">📄</span>
                        <span>{file}</span>
                    </div>
                    <div class="file-actions">
                        <button class="btn-action btn-download">下载</button>
                        <button class="btn-action btn-delete">删除</button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("上传文件")
        st.markdown("""
        <div class="upload-area">
            <p>拖拽文件到此处或点击上传</p>
        </div>
        """, unsafe_allow_html=True)
        uploaded_file = st.file_uploader("选择文件", type=['zip', 'csv', 'txt', 'pdf', 'png', 'jpg', 'jpeg'])
        if uploaded_file:
            handle_file(uploaded_file, '上传')
        
        st.subheader("存储统计")
        # 这里可以添加存储使用情况的图表
        chart_data = pd.DataFrame(
            {"使用量": [65, 35]},
            index=["已用", "可用"]
        )
        st.bar_chart(chart_data)
    
    # 底部添加操作日志
    st.subheader("最近操作")
    for log in operation_log[-5:]:  # 只显示最近5条日志
        st.text(f"{log['time']} - {log['action']}")

# Run the cloud storage page
if __name__ == "__main__":
    cloud_storage_page()
