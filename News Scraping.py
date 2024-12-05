import requests
import json
import sqlite3
import http.client, urllib.parse

ACCESS_KEY = 'e833f1cc919ad792e91a2c2a803c3b3c'

def create_news_database():
    conn = http.client.HTTPConnection('api.mediastack.com')
    params = urllib.parse.urlencode({
        'access_key': ACCESS_KEY,
        'categories': 'general',
        'countries': 'us',
        'keywords': 'japan,-tourism,-travel',
        'limit': 100
        })

    conn.request('GET', '/v1/news?{}'.format(params))

    res = conn.getresponse()
    data = res.read()

    print(data.decode('utf-8'))

    pass

def main():
    create_news_database()

main()
