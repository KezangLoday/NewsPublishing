from flask import Flask, render_template
from newsapi import NewsApiClient
import datetime as the_date
from datetime import date

app = Flask(__name__)

today = date.today()
@app.route('/')
def index():
    newsapi = NewsApiClient(api_key="b0f75ce660c0466a9a98c2478f8abb62")
    my_data = newsapi.get_everything(sources="bbc-news", to=today, sort_by="popularity")
    articles = my_data['articles']

    desc = []
    news = []
    img = []
    author = []
    time = []
    url=[]

    for i in range(len(articles)):
        myarticles = articles[i]

        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
        author.append(myarticles['author'])
        url.append(myarticles['url'])
        pub_date = the_date.datetime.strptime(myarticles['publishedAt'], "%Y-%m-%dT%H:%M:%SZ").date()

        time.append(pub_date.strftime("%B %d, %Y"))

    mylist = zip(news, desc, img, author, time, url)

    return render_template('index.html', context=mylist)


@app.route('/cnn')
def cnn():
    newsapi = NewsApiClient(api_key="f8f06d634b0e48f6a9e41363832a25c5")
    topheadlines = newsapi.get_top_headlines(sources="al-jazeera-english")

    articles = topheadlines['articles']

    desc = []
    news = []
    img = []

    for i in range(len(articles)):
        myarticles = articles[i]

        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])

    mylist = zip(news, desc, img)

    return render_template('cnn.html', context=mylist)


if __name__ == "__main__":
    app.run(debug=True)
