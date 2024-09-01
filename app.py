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

def pages():
    pages = {
        'Fig_preservation': {
            'Fig_presrvation': 'information.py'
        }
    }

    page_name = st.sidebar.radio('导航', list(pages.keys()))
    page_file = None

    if page_name == 'Fig_preservation':
        fig_preservation = pages[page_name]
        page_title = st.sidebar.radio('分类', list(fig_preservation.keys()))
        page_file = fig_preservation[page_title]
    
    if page_file:
        try:
            with open(page_file, encoding='utf-8') as file:
                exec(file.read())
        except FileNotFoundError:
            st.write(f'文件 {page_file} 找不到')
        except Exception as e:
            st.write(f'执行文件时出错: {e}')
    else:
        st.write('所选页面不正确')


pages()