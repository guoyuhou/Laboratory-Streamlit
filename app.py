import streamlit as st  
import os  
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

def pages():  
    pages = {  
        '主页': 'main_page.py',  
        '网页设计': 'Web_Design.md',  
        'Fig_preservation': { 
            '项目信息': os.path.join('Fig_preservation', 'information.md'),  
            '实验设计': os.path.join('Fig_preservation', 'experi_design.md'),
            '实验日志': os.path.join('Fig_preservation', 'experi_log.md'),
            '更新日志': os.path.join('Fig_preservation', 'update_log.md'),
        }  
    }  
  
    page_name = st.sidebar.radio('导航', list(pages.keys()))  
    page_file = None  
  
    if page_name == '主页':  
        page_file = pages[page_name]  
        # 如果主页是 Python 脚本，你可能需要特别处理它  
        if page_file.endswith('.py'):  
            with open(page_file, encoding='utf-8') as file:  
                exec(file.read())  
    elif page_name == '网页设计' or page_name.startswith('Fig_preservation'):  
        page_file = pages[page_name] if not isinstance(pages[page_name], dict) else pages[page_name][st.sidebar.radio('分类', list(pages[page_name].keys()))]  
        if page_file.endswith('.md'):  
            with open(page_file, encoding='utf-8') as file:  
                md_content = file.read()  
                st.markdown(md_content)  
  
    if not page_file or (not page_file.endswith('.py') and not page_file.endswith('.md')):  
        st.write('所选页面不正确或文件类型不支持')  
  
pages()

# Authenticator block

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)