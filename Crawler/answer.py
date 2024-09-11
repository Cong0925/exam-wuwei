'''
Use any preferred framework to scrap any topic on the internet. 
Construct all data scraped in a dataset, ideally containing 100 lines of data, 
save it to a CSV file. Make sure to include the timestamp the website is modified.
'''

'''
解释：
Fetching webpage content：获取网页内容。requests.get(url)
Parsing HTML：解析 HTML。BeautifulSoup(response.content, 'html.parser')
抓取文章：该脚本使用标签查找文章，提取每篇文章的标题、链接和片段。article
处理 “Last-Modified” 标头：它尝试从响应中检索 “Last-Modified” 标头，该标头指示网站或页面的上次修改时间。
存储数据：数据存储在词典列表中，每个词典代表一篇文章。
保存为 CSV：最后，数据被转换为 DataFrame 并保存为 CSV 文件 （） 。pandasscraped_articles.csv
结果：
此脚本最多可抓取 100 篇与 “人工智能” 相关的文章，并将它们连同标题、URL、片段和最后修改的时间戳一起保存到 CSV 文件中。

安装库 pip install requests beautifulsoup4 pandas

通过调整函数中的选择器，可以很容易地针对不同的网站或主题修改此脚本。scrape_articles
'''


# 示例
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
获取单个网页并解析其内容的函数
def scrape_articles(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    # 获取网页内容
    response = requests.get(url, headers=headers)
    
    # 检查上次修改的标题
    last_modified = response.headers.get('Last-Modified')
    if last_modified:
        last_modified = datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z')
    else:
        last_modified = 'N/A'
    
    # 用BeautifulSoup解析内容
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 摘录文章（这将取决于网站的结构）
    articles = soup.find_all('article')  #根据实际结构调整选择器
    data = []
    
    for article in articles:
        title = article.find('h2').text.strip() if article.find('h2') else 'No Title'
        link = article.find('a')['href'] if article.find('a') else 'No Link'
        snippet = article.find('p').text.strip() if article.find('p') else 'No Snippet'
        
        data.append({
            'Title': title,
            'Link': link,
            'Snippet': snippet,
            'Last-Modified': last_modified
        })
    
    return data

# 抓取多个页面或主题的功能
def scrape_multiple_pages(base_url, num_pages):
    all_data = []
    
    for i in range(1, num_pages + 1):
        url = f"{base_url}?page={i}"
        page_data = scrape_articles(url)
        all_data.extend(page_data)
        
        # 如果我们有足够的数据，就停下来
        if len(all_data) >= 100:
            break
    
    return all_data[:100]  # 仅返回前100行

# 主要执行
if __name__ == '__main__':
    # 设置您的目标URL（将其调整到您要定位的网站）
    base_url = 'https://www.example.com/search?q=Artificial+Intelligence'  # 示例搜索URL
    
    # 从网站上删除数据
    scraped_data = scrape_multiple_pages(base_url, num_pages=10)
    
    # 将数据转换为DataFrame
    df = pd.DataFrame(scraped_data)
    
    # 保存到CSV
    df.to_csv('scraped_articles.csv', index=False)

    print(f"Scraped {len(df)} articles and saved to 'scraped_articles.csv'.")


