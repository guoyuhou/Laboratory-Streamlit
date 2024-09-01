import streamlit as st
import os

st.title('陈浩实验室')

st.write('__欢迎访问，这里是山东大学威海校区海洋学院陈浩老师实验室。__')



def load_markdown_file(file_name):  
    with open(file_name, 'r', encoding='utf-8') as file:  
        return file.read()  
  
# 将 MD 文件内容显示在 Streamlit 网页上  
md_content = load_markdown_file("Web_Design.md")  
st.markdown(md_content)  
