import requests
import csv
from bs4 import BeautifulSoup as bs

# emulating of browser work
headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
# web-page for parsing
baseUrl = 'https://www.reuters.com/news/archive/worldNews?view=page&page=1&pageSize=10'


def parse(baseUrl, headers):
    articleList = []
    urls = []
    urls.append(baseUrl)

    session = requests.Session()
    response = session.get(baseUrl, headers=headers)

    if response.status_code == 200:
        try:
            for i in range(10):
                url = f'https://www.reuters.com/news/archive/worldNews?view=page&page={i}&pageSize=10'
                if url not in urls:
                    urls.append(url)
        except:
            pass

        for url in urls:
            response = session.get(url, headers=headers)
            soup = bs(response.content, 'html.parser')  # response from reuters.com

            divArticles = soup.find('div', attrs={'class': 'column1 col col-10'})  # div with articles
            articles = divArticles.find_all('article', attrs={'class': 'story'})  # all articles
            try:
                for article in articles:
                    articleTitle = article.find('h3', attrs={'class': 'story-title'}).text
                    articleTitle = articleTitle.replace("\n", "")
                    articleHref = 'https://www.reuters.com/' + article.find('a')['href']
                    articleTime = article.find('span', attrs={'class': 'timestamp'}).text
                    articleDescription = article.find('p').text

                    articleList.append({
                        'title': articleTitle,
                        'description': articleDescription,
                        'href': articleHref,
                        'time': articleTime
                    })
            except:
                pass
        print(response.status_code)
    else:
        print(response.status_code)

    return articleList


def articlesToCSV(articleList):
    with open('parsed_articles.csv', 'w', encoding='utf-8') as file:
        writerOfArticles = csv.writer(file, delimiter=';')
        writerOfArticles.writerow(('Title', 'Description', 'URL', 'Date'))
        for article in articleList:
            writerOfArticles.writerow((article['title'], article['description'], article['href'], article['time']))


articleList = parse(baseUrl, headers)
articlesToCSV(articleList)

