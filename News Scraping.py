import requests
import json
import sqlite3
import http.client, urllib.parse
import re
import os

ACCESS_KEY = '8b5020c63b59809c8b3d2ee19b0fcc4f'

def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn

def create_news_dict():
    conn = http.client.HTTPConnection('api.mediastack.com')
    params = urllib.parse.urlencode({
        'access_key': ACCESS_KEY,
        'categories': 'general',
        'countries': 'us',
        'keywords': 'climate change',
        'limit': 100,
        'sort': 'popularity'
        })

    conn.request('GET', '/v1/news?{}'.format(params))

    res = conn.getresponse()
    news_data = res.read()

    news_data = news_data.decode('utf-8')

    news_dict = json.loads(news_data)

    return news_dict
    pass

def create_news_database(dict, cur, conn):
    news_data = dict['data']

    cur.execute('''CREATE TABLE IF NOT EXISTS News
                ( id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                date INTEGER )''')

    for article in news_data:
        publish_date = article['published_at']
        publish_date = (re.findall(r'\d{4}\-\d{2}\-\d{2}', publish_date))[0]
        article['published_at'] = publish_date

        cur.execute('''INSERT OR IGNORE INTO News
                    (name, description, date)
                    VALUES (?, ?, ?)''',
                    (article['title'],
                    article['description'],
                    article['published_at']))
    conn.commit()

    pass

def main():
    #news_dict = create_news_dict()
    news_dict = {
        "pagination": {
        "limit": 100,
        "offset": 0,
        "count": 100,
        "total": 1332
    },
    "data": [
        {
        "author": "Jerel Ezell",
        "title": "How Youth Climate Anxiety Became a Convenient Foil for the Right",
        "description": "Suppression of climate change discussions is likely to only elevate more fear around it, writes Jerel Ezell.",
        "url": "https://time.com/7093781/youth-climate-anxiety-weaponization-essay/",
        "source": "TIME.com",
        "image": None,
        "category": "general",
        "language": "en",
        "country": "us",
        "published_at": "2024-10-16T15:45:40+00:00"
        },
        {
      "author": "Austyn Gaffney and Somini Sengupta",
      "title": "Floods Wreak Havoc Across Four Continents",
      "description": "Flooding events around the world share a common factor of an atmosphere made warmer by climate change. What can be done to help citizens prepare?",
      "url": "https://www.nytimes.com/2024/09/18/climate/global-flooding-climate-change.html",
      "source": "The New York Times",
      "image": "https://static01.nyt.com/images/2024/09/18/multimedia/18cli-global-flooding-01-cbtp/18cli-global-flooding-01-cbtp-mediumSquareAt3X.jpg",
      "category": "general",
      "language": "en",
      "country": "us",
      "published_at": "2024-09-18T18:33:18+00:00"
    }
    ]
    }
    curr, con = set_up_database('main.db')
    create_news_database(news_dict, curr, con)

main()
