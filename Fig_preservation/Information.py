import streamlit as st
import os

def load_markdown_file(file_name):  
    with open(file_name, 'r', encoding='utf-8') as file:  
        return file.read()  
  
# 将 MD 文件内容显示在 Streamlit 网页上  
md_content = load_markdown_file("information.md")  
st.markdown(md_content)