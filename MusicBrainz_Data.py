import json
import sqlite3
import os
import requests


def db_setup(db_name):
	#Set up connection to the database and the cursor
	path = os.path.dirname(os.path.abspath(__file__))
	conn = sqlite3.connect(path + "/" + db_name)
	cur = conn.cursor()
	return conn, cur


def fetch_artist_info(cur, conn):
	artist_list = ['P!nk', 'BTS', 'Tyla', 'Tame Impala', 'Normani']

	ARTIST = 'P!nk'

    #use SQL to retrieve the artists from tracks, take the code from homework 7 that made the types table
	#create a new table that inputs the unique artists and assigns them integer keys
	#

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
	return ''


def create_artist_country_table(cur, conn):
	# Create table if it doesn't exist
	cur.execute("""
    	CREATE TABLE IF NOT EXISTS songs (
        	id INTEGER PRIMARY KEY AUTOINCREMENT,
        	artist TEXT NOT NULL,
        	song TEXT NOT NULL,
        	date TEXT NOT NULL,
        	UNIQUE(artist, song, date)
    	)
	""")
	conn.commit()


def create_countries_table(cur, conn):
	
	#use this function to split the artist info table into countries and artists

	return ''


def main():
    #artist_info = fetch_artist_info()
    curr, con = db_setup('main.db')
    #create_news_database(news_dict, curr, con)

main()
