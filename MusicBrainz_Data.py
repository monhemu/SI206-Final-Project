import json
import sqlite3
import os
import requests

#Set up connection to the database and the cursor
path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path + "/" + 'main.db')
cur = conn.cursor()

artist_list = ['P!nk', 'BTS', 'Tyla', 'Tame Impala', 'Normani']

ARTIST = 'P!nk'
'''
for artist in artist_list:
	url = f'https://musicbrainz.org/ws/2/artist/?query={artist}&fmt=json'
	r = requests.get(url)

	if r.status_code == 200:
		info = json.loads(r.content)
		print(info)
	else:
		print('Failed to retrieve data')
'''
