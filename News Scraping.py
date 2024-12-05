import requests
import json
import sqlite3

ACCESS_KEY = 'e833f1cc919ad792e91a2c2a803c3b3c'

def create_news_database():

    params = {
        'access_key': 'ACCESS_KEY',
        'categories': 'general,health',
        'countries': 'us',
        'keywords': 'virus,corona',
        'date': '2021-01-24,2022-12-31'
        }

    url = f'''https://api.mediastack.com/v1/news?
        access_key=e833f1cc919ad792e91a2c2a803c3b3c&categories=general,health&countries=us&keywords=virus,covid
        &date=2020-12-24,2020-12-31'''
    
    response = requests.get(url)
    news_dict = json.loads(response.content)

    print(news_dict)

    pass

def main():
    create_news_database()

main()
