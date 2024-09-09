import streamlit as st
import requests
import feedparser

def search_papers(query):
    response = requests.get(f'https://api.crossref.org/works?query={query}')
    data = response.json()
    results = data['message']['items']
    return results

def recommended_papers():
    st.header("推荐阅读的论文")
    papers = [
        {"title": "论文标题1", "url": "https://example.com/paper1"},
        {"title": "论文标题2", "url": "https://example.com/paper2"},
    ]
    
    for paper in papers:
        st.markdown(f"- [{paper['title']}]({paper['url']})")

def latest_papers():
    st.header("最新发表的论文")
    
    feeds = {
        "Nature": "https://www.nature.com/nature/rss",
        "Cell": "https://www.cell.com/rss",
        "Science": "https://www.sciencemag.org/rss/current.xml",
    }
    
    for journal, feed_url in feeds.items():
        st.subheader(f"{journal} 最新论文")
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:5]:
            st.markdown(f"- [{entry.title}]({entry.link})")

def paper_search():
    st.header("论文搜索")
    query = st.text_input("输入论文关键词:")
    
    if st.button("搜索"):
        if query:
            results = search_papers(query)
            if results:
                for result in results[:5]:
                    st.markdown(f"- [{result['title'][0]}]({result['URL']})")
            else:
                st.write("未找到相关论文。")
        else:
            st.write("请输入搜索关键词。")

def paper_comments():
    st.header("论文讨论区")
    comment = st.text_area("在这里留言:")
    
    if st.button("提交评论"):
        if comment:
            st.write("评论已提交，谢谢您的参与！")
        else:
            st.write("评论内容不能为空。")

def main():
    st.title('科研论文资源')
    
    st.write('以下是三大顶级自然科学期刊的官网链接，点击即可访问：')
    st.markdown(
        """
        <style>
        .title {
            font-size: 24px;
            font-weight: bold;
        }
        .link {
            font-size: 18px;
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
        """,
        unsafe_allow_html=True
    )
    
    paper_search()
    recommended_papers()
    latest_papers()
    paper_comments()

if __name__ == "__main__":
    main()
