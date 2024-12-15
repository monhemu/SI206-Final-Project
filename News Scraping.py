import requests
import json
import sqlite3
import http.client, urllib.parse
import re
import os

ACCESS_KEY = '98ccceb701f523f653f3ea662ec39fdc'

def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn

def create_news_dict(artist_name):
    conn = http.client.HTTPConnection('api.mediastack.com')
    params = urllib.parse.urlencode({
        'access_key': ACCESS_KEY,
        'categories': 'general, entertainment',
        'countries': 'us',
        'keywords': artist_name,
        'limit': 25,
        'sort': 'popularity'
        })

    conn.request('GET', '/v1/news?{}'.format(params))

    res = conn.getresponse()
    news_data = res.read()

    news_data = news_data.decode('utf-8')

    news_dict = json.loads(news_data)

    return news_dict
    pass

def create_news_database(dict_list, curr, conn):
    for dict in dict_list:
        data = dict['data']
        i = 0
        if i >= 25:
            break
        for article in data:
            if i>= 25:
                break
            publish_date = article['published_at']
            publish_date = (re.findall(r'\d{4}\-\d{2}\-\d{2}', publish_date))[0]
            article['published_at'] = publish_date

            curr.execute('''INSERT OR IGNORE INTO News
                        (name, description, date)
                        VALUES (?, ?, ?)''',
                        (article['title'],
                        article['description'],
                        article['published_at']))
            i += 0
    conn.commit()

    pass

def main():
    jin_dict = create_news_dict('BTS, Jin')
    chap_dict = create_news_dict('Chappell Roan')
    billie_dict = create_news_dict('Linkin Park')
    dict_list = [jin_dict, chap_dict, billie_dict]
    curr, conn = set_up_database('main.db')

    curr.execute("DROP TABLE News")

    curr.execute('''CREATE TABLE IF NOT EXISTS News
                ( id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                date INTEGER )''')
    conn.commit()
    create_news_database(dict_list, curr, conn)
    conn.close()
main()
