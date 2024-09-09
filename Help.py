import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 实验室主页
st.title('陈浩实验室')
st.write('__欢迎访问，这里是山东大学威海校区海洋学院陈浩老师实验室。__')

# 开发声明
st.subheader('开发声明')

st.markdown("""
欢迎使用本应用程序！

本应用程序旨在为实验室的生态建设提供支持，创建一个高效的导师-研究生-本科生综合平台。目标是集成科研过程中所需的各种工具和实验室信息，以减少科研过程中的繁琐步骤，从而使科研人员能够将更多精力集中在核心研究任务上。

**本应用提供以下功能：**
- **工具集成**：集合科研所需的多种数据分析、绘图和项目管理工具。
- **信息管理**：集中展示实验室的基本信息、研究方向和团队成员等，便于信息共享和协作。
- **即时互动**：支持实时沟通、任务跟踪和项目管理，以促进团队内部的高效协作。

我们相信，通过这个平台的建设和使用，实验室的工作效率将得到显著提升。我们的愿景是通过这份热情和努力，帮助实验室成员更好地进行科研，同时增强团队的凝聚力和合作精神。我们希望每一位使用者都能在科研道路上取得更大的进步。

感谢您的使用与支持。我们期待通过这个平台，助力每位科研人员的成长与成功。

—— 刘曜畅
""")

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

# 用户反馈模块
st.subheader('用户反馈')

# 创建反馈表单
with st.form(key='feedback_form'):
    st.write('请填写以下表单以提交您的反馈：')
    
    name = st.text_input('姓名（可选）：')
    email = st.text_input('电子邮件（可选）：')
    feedback_type = st.selectbox('反馈类型：', ['功能建议', '问题报告', '其他'])
    feedback_content = st.text_area('反馈内容：', height=150)
    
    # 提交按钮
    submit_button = st.form_submit_button(label='提交反馈')

    if submit_button:
        if feedback_content.strip() == '':
            st.warning('请填写反馈内容。')
        else:
            # 配置邮箱信息
            sender_email = '17806067729@163.com'  # 您的网易邮箱
            receiver_email = '13562157226@163.com'  # 收件人邮箱
            password = '9426983..chang'  # 您的网易邮箱密码或应用专用密码
            smtp_server = 'smtp.163.com'
            smtp_port = 465  # 使用SSL端口

            # 创建邮件内容
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = '用户反馈'

            body = f'''
            姓名: {name}
            电子邮件: {email}
            反馈类型: {feedback_type}
            反馈内容:
            {feedback_content}
            '''
            msg.attach(MIMEText(body, 'plain'))

            # 发送邮件
            try:
                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, msg.as_string())
                    st.success('感谢您的反馈！我们会认真考虑您的建议。')
            except smtplib.SMTPAuthenticationError:
                st.error('认证失败：请检查您的邮箱地址和密码。')
            except Exception as e:
                st.error(f'发送邮件时发生错误: {e}')
