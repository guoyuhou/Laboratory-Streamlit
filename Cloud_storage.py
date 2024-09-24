import streamlit as st
import oss2
import zipfile
import io
from pdf2image import convert_from_path
import logging
import random
from datetime import datetime, timedelta

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
            st.write(f'找到 {len(files)} 个文件:')
            for file in files:
                st.write(f'- {file}')  # 列举找到的文件
        else:
            st.write('没有找到匹配的文件')
    else:
        st.write('请在上方输入关键词进行搜索')

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

def generate_simulated_data():
    """生成模拟的每日流量、文件总数和占用率数据"""
    daily_data = {
        '日期': [],
        '流量': [],
        '文件总数': [],
        '占用率': []
    }
    
    start_date = datetime.now() - timedelta(days=30)  # 过去30天
    for i in range(30):
        date = start_date + timedelta(days=i)
        daily_data['日期'].append(date.strftime('%Y-%m-%d'))
        daily_data['流量'].append(random.randint(50, 300))  # 模拟流量（50MB到300MB）
        daily_data['文件总数'].append(random.randint(20, 100))  # 模拟文件总数
        daily_data['占用率'].append(random.uniform(0, 100))  # 模拟占用率（0%到100%）

    return daily_data

# 在 display_statistics 中调用生成的数据
def display_statistics():
    """展示云服务使用频率和占用率"""
    st.subheader('云服务统计信息')

    daily_data = generate_simulated_data()
    
    # 转换为 DataFrame 以便绘图
    import pandas as pd
    df = pd.DataFrame(daily_data)

    # 使用折线图显示数据
    st.line_chart(df.set_index('日期'))

    # 显示操作日志
    st.write('操作日志:')
    for log in operation_log:
        st.write(f"{log['time']} - {log['action']}")
def cloud_storage_page(username=None):
    """显示云存储页面"""
    st.title("云存储")
    
    # 自定义CSS样式
    st.markdown("""
    <style>
        body {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            background-color: #f0f2f5;
            color: #333;
        }
        .main {
            padding: 2rem;
        }
        .stButton > button {
            background-color: #4285f4;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #3367d6;
        }
        .sidebar .sidebar-content {
            background-color: #ffffff;
            box-shadow: 2px 0 5px rgba(0,0,0,0.1);
        }
        .css-1d391kg {
            padding-top: 3rem;
        }
        h1, h2, h3 {
            color: #333;
        }
    </style>
    """, unsafe_allow_html=True)

    # 页面标题和欢迎信息
    st.title("实验室云存储服务")
    if username:
        st.write(f"欢迎回来，{username}！")
    
    # 添加使用说明
    with st.expander("关于实验室云服务", expanded=False):
        st.write("""
        欢迎使用实验室云服务平台！我们提供安全、高效的文件管理解决方案，支持多种文件格式。
        
        主要功能：
        - 文件上传：支持ZIP、PDF、图片等多种格式
        - 文件下载：快速获取您需要的文件
        - 文件更新：方便地更新已存在的文件
        - 文件删除：单个或批量删除不再需要的文件
        - 文件预览：直接在平台上预览文件内容
        - 文件搜索：快速定位您需要的文件
        
        请使用左侧导航栏选择所需的操作。如有任何问题，请联系实验室管理员。
        """)

    # 显示统计信息
    col1, col2 = st.columns([2, 1])
    with col1:
        display_statistics()
    with col2:
        st.subheader("快速操作")
        if st.button("上传新文件"):
            upload_files_with_progress()
        if st.button("查看所有文件"):
            download_file()

    # 侧边栏导航
    st.sidebar.title("功能导航")
    options = st.sidebar.radio("选择操作", 
        ("文件上传", "文件下载", "文件更新", "文件删除", "文件预览", "文件搜索", "批量删除"))
    
    operations = {
        "文件上传": upload_files_with_progress,
        "文件下载": download_file,
        "文件更新": update_file,
        "文件删除": delete_file,
        "文件预览": preview_file,
        "文件搜索": search_files,
        "批量删除": batch_delete_files
    }
    
    operation_function = operations.get(options)
    if operation_function:
        st.subheader(options)
        operation_function()

    # 页脚
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #888;'>© 2024 实验室云存储服务 | 技术支持：实验室IT团队</p>", 
        unsafe_allow_html=True
    )



# Run the cloud storage page
if __name__ == "__main__":
    cloud_storage_page()
