import streamlit as st
import oss2
import zipfile
import io

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

def upload_files_with_progress():
    """处理文件上传，显示进度条"""
    st.subheader('上传文件')
    
    uploaded_file = st.file_uploader("选择要上传的文件（支持ZIP和其他类型）", type=['zip', 'csv', 'txt', 'pdf', 'png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        file_size = uploaded_file.size / 1024 / 1024  # 以MB为单位
        st.write(f'文件大小：{file_size:.2f} MB')
        
        progress_bar = st.progress(0)
        
        if uploaded_file.type == 'application/zip':
            # 如果上传的是ZIP文件
            with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                total_files = len(zip_ref.infolist())
                for i, file_info in enumerate(zip_ref.infolist(), start=1):
                    file_data = zip_ref.read(file_info.filename)
                    bucket.put_object(file_info.filename, file_data)
                    progress_bar.progress(i / total_files)
                    st.write(f'文件 {file_info.filename} 上传成功')
            st.success('ZIP文件中的所有文件已成功上传到 OSS')
        else:
            # 处理其他文件类型
            bucket.put_object(uploaded_file.name, uploaded_file)
            st.success(f'文件 {uploaded_file.name} 上传成功')
            progress_bar.progress(1)

def download_file():
    """处理文件下载"""
    st.subheader('下载文件')
    files = list_files()
    if files:
        file_name = st.selectbox('选择要下载的文件', files)
        if file_name and st.button('下载'):
            obj = bucket.get_object(file_name)
            st.download_button(
                label='下载文件',
                data=obj.read(),
                file_name=file_name,
                mime='application/octet-stream'
            )
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
                # 如果上传的是ZIP文件
                with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                    for file_info in zip_ref.infolist():
                        file_data = zip_ref.read(file_info.filename)
                        bucket.put_object(file_info.filename, file_data)
                        st.write(f'文件 {file_info.filename} 已被更新')
                st.success('ZIP文件中的所有文件已成功更新到 OSS')
            else:
                # 更新单个文件
                bucket.put_object(uploaded_file.name, uploaded_file)
                st.success(f'文件 {uploaded_file.name} 已被更新')

def delete_file():
    """处理文件删除"""
    st.subheader('删除文件')
    files = list_files()
    file_name = st.selectbox('选择要删除的文件', files)
    
    if file_name and st.button('删除'):
        bucket.delete_object(file_name)
        st.success(f'文件 {file_name} 已成功删除')

def preview_file():
    """处理文件预览"""
    st.subheader('预览文件')
    files = list_files()
    file_name = st.selectbox('选择要预览的文件', files)
    
    if file_name:
        obj = bucket.get_object(file_name)
        file_content = obj.read()
        if file_name.lower().endswith(('png', 'jpg', 'jpeg')):
            st.image(file_content, caption=file_name)
        elif file_name.lower().endswith('txt'):
            st.text(file_content.decode('utf-8'))
        elif file_name.lower().endswith('pdf'):
            st.write('PDF 文件无法在这里直接预览，建议下载查看。')
        else:
            st.write(f'无法预览此文件类型：{file_name}')

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
        for file_name in selected_files:
            bucket.delete_object(file_name)
        st.success(f'已成功删除 {len(selected_files)} 个文件')

def cloud_storage_page():
    """显示云存储页面"""
    st.title("云存储")
    upload_files_with_progress()
    download_file()
    update_file()
    delete_file()
    preview_file()
    search_files()
    batch_delete_files()
