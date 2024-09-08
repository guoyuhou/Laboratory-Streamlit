import streamlit as st
import oss2
import zipfile
import io
import os

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

def upload_zip_file():
    """处理ZIP文件上传"""
    st.subheader('上传文件夹（压缩为ZIP）')
    uploaded_file = st.file_uploader("选择要上传的ZIP文件", type='zip')
    if uploaded_file:
        # 解压ZIP文件并上传到OSS
        with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                file_data = zip_ref.read(file_info.filename)
                bucket.put_object(file_info.filename, file_data)
        st.success('ZIP文件上传成功，并已解压到OSS')

def download_file():
    """处理文件下载"""
    st.subheader('下载文件')
    files = list_files()
    file_name = st.selectbox('选择要下载的文件', files)
    if file_name and st.button('下载'):
        obj = bucket.get_object(file_name)
        st.download_button(
            label='下载文件',
            data=obj.read(),
            file_name=file_name,
            mime='application/octet-stream'
        )

def cloud_storage_page():
    """显示云存储页面"""
    st.title("云存储")
    upload_zip_file()
    download_file()
