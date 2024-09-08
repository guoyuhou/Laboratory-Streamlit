import streamlit as st
import oss2

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

def upload_file():
    """处理文件上传"""
    st.subheader('上传文件')
    uploaded_file = st.file_uploader("选择要上传的文件")
    if uploaded_file:
        bucket.put_object(uploaded_file.name, uploaded_file)
        st.success(f'文件 {uploaded_file.name} 上传成功')

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
    upload_file()
    download_file()
