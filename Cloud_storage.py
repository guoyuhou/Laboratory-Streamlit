import streamlit as st
import oss2
import zipfile
import io
from pdf2image import convert_from_path
import logging
import random
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
        operation_log.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "action": f"{operation}文件 {file.name}"})
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
        operation_log.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "action": f"上传ZIP文件 {uploaded_file.name}"})
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
                operation_log.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "action": f"下载文件 {file_name}"})
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
            operation_log.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "action": f"删除文件 {file_name}"})
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
            operation_log.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "action": f"预览文件 {file_name}"})
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
            operation_log.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "action": f"批量删除 {len(selected_files)} 个文件"})
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

def display_statistics():
    """展示云服务使用频率和占用率"""
    st.subheader('云服务统计信息')

    daily_data = generate_simulated_data()
    df = pd.DataFrame(daily_data)

    # 使用Plotly创建交互式图表
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['日期'], y=df['流量'], mode='lines+markers', name='流量 (MB)'))
    fig.add_trace(go.Scatter(x=df['日期'], y=df['文件总数'], mode='lines+markers', name='文件总数'))
    fig.add_trace(go.Scatter(x=df['日期'], y=df['占用率'], mode='lines+markers', name='占用率 (%)'))

    fig.update_layout(
        title='云服务使用统计',
        xaxis_title='日期',
        yaxis_title='数值',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True)

    # 显示操作日志
    st.subheader('最近操作日志')
    log_df = pd.DataFrame(operation_log[-10:])  # 只显示最近10条日志
    st.table(log_df)

def cloud_storage_page(username=None):
    """显示云存储页面"""
    st.title("智能云存储管理系统")
    
    # 自定义CSS样式
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
        
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f0f2f5;
            color: #333;
        }
        .main {
            padding: 2rem;
            animation: fadeIn 0.5s ease-in-out;
        }
        .stButton > button {
            background-color: #4285f4;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .stButton > button:hover {
            background-color: #3367d6;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .sidebar .sidebar-content {
            background-color: #ffffff;
            box-shadow: 2px 0 5px rgba(0,0,0,0.1);
        }
        .css-1d391kg {
            padding-top: 3rem;
        }
        h1, h2, h3 {
            color: #1a73e8;
            font-weight: 700;
        }
        .stSelectbox, .stTextInput {
            background-color: #ffffff;
            border-radius: 4px;
            border: 1px solid #e0e0e0;
            padding: 0.5rem;
            transition: all 0.3s ease;
        }
        .stSelectbox:focus, .stTextInput:focus {
            border-color: #4285f4;
            box-shadow: 0 0 0 2px rgba(66, 133, 244, 0.2);
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .file-card {
            background-color: #ffffff;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .file-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
    </style>
    """, unsafe_allow_html=True)

    # 页面标题和欢迎信息
    st.title("智能云存储管理系统")
    if username:
        st.write(f"欢迎回来，{username}！")
    
    # 添加使用说明
    with st.expander("关于智能云存储管理系统", expanded=False):
        st.write("""
        欢迎使用智能云存储管理系统！我们提供安全、高效的文件管理解决方案，支持多种文件格式。
        
        主要功能：
        - 智能文件上传：支持ZIP、PDF、图片等多种格式，自动分类
        - 快速文件下载：便捷获取您需要的文件
        - 实时文件更新：轻松更新已存在的文件
        - 批量文件管理：单个或批量删除不再需要的文件
        - 智能文件预览：直接在平台上预览文件内容
        - 高级文件搜索：快速定位您需要的文件
        - 数据可视化：直观展示云存储使用情况
        
        使用左侧导航栏选择所需的操作。如有任何问题，请联系系统管理员。
        """)

    # 显示统计信息
    col1, col2 = st.columns([2, 1])
    with col1:
        display_statistics()
    with col2:
        st.subheader("快速操作")
        if st.button("上传新文件", key="upload_button"):
            st.session_state.current_operation = "文件上传"
        if st.button("查看所有文件", key="view_files_button"):
            st.session_state.current_operation = "文件下载"

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
    
    if 'current_operation' not in st.session_state:
        st.session_state.current_operation = options

    operation_function = operations.get(st.session_state.current_operation)
    if operation_function:
        st.subheader(st.session_state.current_operation)
        operation_function()

    # 添加文件分类展示
    st.subheader("文件分类")
    file_types = {
        "文档": ["pdf", "doc", "docx", "txt"],
        "图片": ["jpg", "jpeg", "png", "gif"],
        "压缩文件": ["zip", "rar"],
        "其他": []
    }
    
    all_files = list_files()
    categorized_files = {category: [] for category in file_types}
    
    for file in all_files:
        file_ext = file.split('.')[-1].lower()
        categorized = False
        for category, extensions in file_types.items():
            if file_ext in extensions:
                categorized_files[category].append(file)
                categorized = True
                break
        if not categorized:
            categorized_files["其他"].append(file)
    
    for category, files in categorized_files.items():
        with st.expander(f"{category} ({len(files)})"):
            for file in files:
                st.markdown(f"""
                <div class="file-card">
                    <h4>{file}</h4>
                    <p>大小: {bucket.get_object_meta(file).content_length / 1024:.2f} KB</p>
                    <p>上传时间: {bucket.get_object_meta(file).last_modified}</p>
                </div>
                """, unsafe_allow_html=True)

    # 页脚
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #888;'>© 2024 智能云存储管理系统 | 技术支持：AI实验室</p>", 
        unsafe_allow_html=True
    )

# 添加JavaScript动画效果
st.markdown("""
<script>
document.addEventListener('DOMContentLoaded', (event) => {
    // 添加淡入效果
    document.body.style.opacity = 0;
    let opacity = 0;
    let fadeIn = setInterval(() => {
        if (opacity >= 1) {
            clearInterval(fadeIn);
        }
        document.body.style.opacity = opacity;
        opacity += 0.1;
    }, 50);

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

    // 为文件卡片添加悬停效果
    const fileCards = document.querySelectorAll('.file-card');
    fileCards.forEach(card => {
        card.addEventListener('mouseover', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 5px 15px rgba(0,0,0,0.2)';
        });
        card.addEventListener('mouseout', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 5px rgba(0,0,0,0.1)';
        });
    });
});
</script>
""", unsafe_allow_html=True)

# Run the cloud storage page
if __name__ == "__main__":
    cloud_storage_page()
