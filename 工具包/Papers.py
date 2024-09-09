import streamlit as st
import os

def display_papers():
    st.title('论文展示')

    # 顶刊官网地址
    st.subheader('顶级自然科学期刊官网')

    st.write('1. [Nature](https://www.nature.com)')
    st.write('2. [Cell](https://www.cell.com)')
    st.write('3. [Science](https://www.sciencemag.org)')

# 调用函数显示内容
if __name__ == "__main__":
    display_papers()
