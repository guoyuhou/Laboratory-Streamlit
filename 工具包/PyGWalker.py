import streamlit as st
import pandas as pd
from pygwalker.api.streamlit import StreamlitRenderer
import os

st.title('PyGWalker')
st.write('__PyGWalker is a powerful data processing and drawing tool__')
st.video(os.path.join('videos', 'pygwalker.mp4'))

# 创建一个文件上传器，允许用户上传CSV文件   
uploaded_file = st.file_uploader("选择你的CSV文件", type=["csv"])  

if uploaded_file is not None:  
    try:
        # 使用Pandas读取上传的CSV文件  
        data = pd.read_csv(uploaded_file)  

        # 显示数据帧的前几行  
        st.write(data.head())  

        # 定义一个函数来获取渲染器，确保在文件上传后才调用  
        @st.cache_resource
        def get_pyg_renderer(df):  
            # 这里可以指定spec参数，如果你有配置文件的话
            return StreamlitRenderer(df)  

        renderer = get_pyg_renderer(data)  

        # 显示PyGWalker的探索器
        renderer.explorer()
        
    except Exception as e:
        st.error(f"处理文件时发生错误: {e}")
