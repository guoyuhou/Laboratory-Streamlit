import streamlit as st
import os

# 实验室主页
st.title('陈浩实验室')
st.write('__欢迎访问，这里是山东大学威海校区海洋学院陈浩老师实验室。__')

# 用户反馈功能
st.subheader('用户反馈')
feedback = st.text_area('请在下方输入您的反馈或建议，我们非常欢迎您的意见！', height=150)
if st.button('提交反馈'):
    if feedback:
        st.success('感谢您的反馈！我们会认真考虑您的建议。')
        # 将反馈保存到文件或数据库 (示例代码)
        with open("feedback.txt", "a") as f:
            f.write(feedback + "\n")
    else:
        st.warning('反馈内容不能为空。')

# 帮助文档
st.subheader('帮助文档')
st.write('欢迎阅读实验室应用的使用文档和常见问题解答。')
st.write('### 使用文档')
st.write('1. **上传文件**: 点击“上传文件”选项，选择要上传的文件或ZIP包，支持多种文件格式。')
st.write('2. **下载文件**: 在“下载文件”选项中选择文件进行下载。')
st.write('3. **更新文件**: 选择要更新的文件并上传新的版本。')
st.write('4. **删除文件**: 选择要删除的文件进行删除操作。')
st.write('5. **预览文件**: 支持对图像、文本文件进行预览。')
st.write('6. **搜索文件**: 输入关键词搜索文件。')
st.write('7. **批量删除文件**: 选择多个文件进行批量删除。')

st.write('### 常见问题')
st.write('**问:** 如何上传多个文件？')
st.write('**答:** 您可以将多个文件打包成一个ZIP文件进行上传。')

st.write('**问:** 如何查看上传的文件？')
st.write('**答:** 使用“预览文件”功能，您可以查看上传的图像和文本文件。')
