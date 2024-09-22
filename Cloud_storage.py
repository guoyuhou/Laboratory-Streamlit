import streamlit as st
import oss2
import zipfile
import io
from pdf2image import convert_from_path
import logging

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

def upload_files_with_progress():
    """处理文件上传，显示进度条"""
    st.subheader('上传文件')
    uploaded_file = st.file_uploader("选择要上传的文件（支持ZIP和其他类型）", type=['zip', 'csv', 'txt', 'pdf', 'png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        st.write(f'文件大小：{uploaded_file.size / 1024 / 1024:.2f} MB')
        if uploaded_file.type == 'application/zip':
            upload_zip_file(uploaded_file)
        else:
            handle_file(uploaded_file, '上传')

def download_file():
    """处理文件下载"""
    st.subheader('下载文件')
    files = list_files()
    if files:
        file_name = st.selectbox('选择要下载的文件', files)
        if file_name and st.button('下载'):
            try:
                obj = bucket.get_object(file_name)
                st.download_button(
                    label='下载文件',
                    data=obj.read(),
                    file_name=file_name,
                    mime='application/octet-stream'
                )
            except Exception as e:
                logging.error(f'下载文件 {file_name} 时出错: {e}')
                st.error(f'下载文件时出错: {e}')
    else:
        st.write('没有文件可供下载')

def update_file():
    """处理文件更新"""
    st.subheader('更新文件')
    files = list_files()
    file_name = st.selectbox('选择要更新的文件', files)
    
    if file_name:
        uploaded_file = st.file_uploader("选择新的文件来替换", type=['zip', 'csv', 'txt', 'pdf', 'png', 'jpg', 'jpeg'])
        if uploaded_file:
            if uploaded_file.type == 'application/zip':
                upload_zip_file(uploaded_file)
            else:
                handle_file(uploaded_file, '更新')

def delete_file():
    """处理文件删除"""
    st.subheader('删除文件')
    files = list_files()
    file_name = st.selectbox('选择要删除的文件', files)
    
    if file_name and st.button('删除'):
        try:
            bucket.delete_object(file_name)
            st.success(f'文件 {file_name} 已成功删除', icon="✅")
        except Exception as e:
            logging.error(f'删除文件 {file_name} 时出错: {e}')
            st.error(f'删除文件时出错: {e}')

def preview_file():
    """处理文件预览"""
    st.subheader('预览文件')
    files = list_files()
    file_name = st.selectbox('选择要预览的文件', files)
    
    if file_name:
        try:
            obj = bucket.get_object(file_name)
            file_content = obj.read()
            if file_name.lower().endswith(('png', 'jpg', 'jpeg')):
                st.image(file_content, caption=file_name)
            elif file_name.lower().endswith('txt'):
                st.text(file_content.decode('utf-8'))
            elif file_name.lower().endswith('pdf'):
                images = convert_from_path(io.BytesIO(file_content), first_page=5)
                for image in images:
                    st.image(image, caption=file_name)
            else:
                st.write(f'无法预览此文件类型：{file_name}')
        except Exception as e:
            logging.error(f'预览文件 {file_name} 时出错: {e}')
            st.error(f'预览文件时出错: {e}')

def search_files():
    """处理文件搜索"""
    st.subheader('搜索文件')
    query = st.text_input('输入搜索关键词')
    if query:
        files = [file for file in list_files() if query.lower() in file.lower()]
        if files:
            st.write(f'找到 {len(files)} 个文件')
            return files
        else:
            st.write('没有找到匹配的文件')
            return []
    return list_files()

def batch_delete_files():
    """处理批量文件删除"""
    st.subheader('批量删除文件')
    files = list_files()
    selected_files = st.multiselect('选择要删除的文件', files)
    
    if selected_files and st.button('删除选中的文件'):
        try:
            for file_name in selected_files:
                bucket.delete_object(file_name)
            st.success(f'已成功删除 {len(selected_files)} 个文件', icon="✅")
        except Exception as e:
            logging.error(f'批量删除文件时出错: {e}')
            st.error(f'批量删除文件时出错: {e}')

def cloud_storage_page():
    """显示云存储页面"""
    st.title("云存储")
    
    # 添加使用说明
    st.subheader("关于实验室云服务")
    st.write("""
        欢迎使用实验室云服务平台！您可以在这里上传、下载、更新、删除文件，支持多种文件格式（如ZIP、PDF、图片等）。
        请根据侧边栏的选项选择您需要的服务。
    """)

    # 添加一些样式
    st.markdown("""
    <style>
        body {
            background-color: #f4f4f4;
            color: #333;
            font-family: 'Arial', sans-serif;
        }
        .sidebar .sidebar-content {
            background-color: #001f3f;
            color: white;
        }
        .stButton button {
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 15px;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #0056b3;
        }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.title("导航")
    options = st.sidebar.radio("选择操作", ("上传文件", "下载文件", "更新文件", "删除文件", "预览文件", "搜索文件", "批量删除文件"))
    
    operations = {
        "上传文件": upload_files_with_progress,
        "下载文件": download_file,
        "更新文件": update_file,
        "删除文件": delete_file,
        "预览文件": preview_file,
        "搜索文件": search_files,
        "批量删除文件": batch_delete_files
    }
    
    operation_function = operations.get(options)
    if operation_function:
        operation_function()

    st.markdown("""<style>.css-1xarl7p { padding: 1rem; }</style>""", unsafe_allow_html=True)
