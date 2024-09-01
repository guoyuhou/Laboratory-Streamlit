import streamlit as st
import os


def pages():
    pages = {
        '主页': 'main_page.py',
        '网页设计': 'Web_Design.md',
        'Fig_preservation': {
            '项目信息': 'information.md',
            '实验设计': 'experi_design.md'
        }
    }

    page_name = st.sidebar.radio('导航', list(pages.keys()))
    page_file = None

    if page_name == '主页':
        page_file = pages[page_name]
    elif page_name == '网页设计':
        page_file = pages[page_name]
    elif page_name == 'Fig_preservation':
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