import streamlit as st

def display_papers():
    st.title('顶级自然科学期刊')

    with st.expander("查看顶级自然科学期刊", expanded=True):
        st.write('以下是一些顶级自然科学期刊的官网链接，点击即可访问：')

        # 使用 Markdown 和图标美化
        st.markdown(
            """
            <style>
            .title {
                font-size: 20px;
                font-weight: bold;
                margin-top: 10px;
            }
            .link {
                font-size: 16px;
                color: #1f77b4;
                text-decoration: none;
            }
            .link:hover {
                text-decoration: underline;
            }
            </style>
            <div class="title">Nature</div>
            <a class="link" href="https://www.nature.com" target="_blank">Nature 官网</a>
            
            <div class="title">Cell</div>
            <a class="link" href="https://www.cell.com" target="_blank">Cell 官网</a>
            
            <div class="title">Science</div>
            <a class="link" href="https://www.sciencemag.org" target="_blank">Science 官网</a>
            
            <div class="title">Advanced Materials</div>
            <a class="link" href="https://onlinelibrary.wiley.com/journal/15214095" target="_blank">Advanced Materials 官网</a>
            
            <div class="title">Advanced Functional Materials</div>
            <a class="link" href="https://onlinelibrary.wiley.com/journal/16163028" target="_blank">Advanced Functional Materials 官网</a>
            """,
            unsafe_allow_html=True
        )

# 调用函数显示内容
if __name__ == "__main__":
    display_papers()
