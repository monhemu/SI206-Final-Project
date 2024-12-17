import requests
import json
import sqlite3
import http.client, urllib.parse
import re
import os

ACCESS_KEY = '70673ffb38f29475d1325145b9aa2cf1'


def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn

def create_news_dict(artist_name):
    conn = http.client.HTTPConnection('api.mediastack.com')
    params = urllib.parse.urlencode({
        'access_key': ACCESS_KEY,
        'categories': 'general, entertainment, -sports',
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

def create_news_database(dict, curr, conn):
    data = dict['data']
    i = 0
    for article in data:
        if i>= 25:
             break
        publish_date = article['published_at']
        publish_date = (re.findall(r'\d{4}\-\d{2}\-\d{2}', publish_date))[0]
        publish_date = publish_date.replace('-','')
        article['published_at'] = int(publish_date)
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
    curr, conn = set_up_database('main.db')

    #curr.execute('''DROP TABLE News''')

    curr.execute('''SELECT artists.name, COUNT(songs.id) as song_count
                    FROM artists
                    JOIN songs ON artists.id = songs.artist_id
                    WHERE country_id = ?
                    GROUP BY artists.name
                    ORDER BY song_count DESC
                    LIMIT 5''',
                    (1,))
    
    artist_list = curr.fetchall()

    curr.execute('''CREATE TABLE IF NOT EXISTS News
                ( id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                date INTEGER )''')
    
    conn.commit()

    curr.execute('''SELECT COUNT(*) FROM News''')
    news_list = curr.fetchall()

    if news_list[0][0] == 0:
        artist = artist_list[0]
        artist_name = artist[0].replace('-', ' ')
        artist_dict = create_news_dict(artist_name)
        create_news_database(artist_dict, curr, conn)
    elif news_list[0][0]  <= 25:
        artist = artist_list[1]
        artist_name = artist[0].replace('-', ' ')
        artist_dict = create_news_dict(artist_name)
        create_news_database(artist_dict, curr, conn)
    elif news_list[0][0]  <= 50:
        artist = artist_list[2]
        artist_name = artist[0].replace('-', ' ')
        artist_dict = create_news_dict(artist_name)
        create_news_database(artist_dict, curr, conn)
    elif news_list[0][0]  <= 75:
        artist = artist_list[3]
        artist_name = artist[0].replace('-', ' ')
        artist_dict = create_news_dict(artist_name)
        create_news_database(artist_dict, curr, conn)
    elif news_list[0][0]  <= 100:
        artist = artist_list[4]
        artist_name = artist[0].replace('-', ' ')
        artist_dict = create_news_dict(artist_name)
        create_news_database(artist_dict, curr, conn)  
    
main()
