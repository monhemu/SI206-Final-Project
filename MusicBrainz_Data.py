import json
import sqlite3
import os
import requests
import time

#will need to input artist ID into the news table

def db_setup(db_name):
	#Set up connection to the database and the cursor
	path = os.path.dirname(os.path.abspath(__file__))
	conn = sqlite3.connect(path + "/" + db_name)
	cur = conn.cursor()
	return conn, cur




def create_artists_table(cur, conn):
	"""
    Creates a table of countries.
    
    Args:
        cur (cursor): The database cursor object
        conn (connection): The database connection 

	Returns:
		data (dictionary): Artist names as keys and their countries as the values
    """

	#Create the artist table with their associated countries
	cur.execute('''
			 CREATE TABLE IF NOT EXISTS Artists (
			 id INTEGER PRIMARY KEY AUTOINCREMENT,
			 name TEXT,
			 country TEXT)''')
	
	#Grab the list of all artists from the songs table
	cur.execute('SELECT artist FROM songs')
	artist_list = cur.fetchall()
	count = 0
	
	#Loop through the list of artists to make requests one at a time
	for artist in artist_list:

		#Check that 25 rows have been added
		if count > 25:
			print('Retrieved a set of 25 rows')
			break

		#Checks to see if the current artist has already been added to the table
		cur.execute('SELECT * FROM Artists WHERE name = ?', (artist,))
		try:
			check_artist = cur.fetchone()[1]
			print("Found in database ", artist)
			continue
		except:
			pass

		url = f'https://musicbrainz.org/ws/2/artist/?query={artist}&fmt=json'
		r = requests.get(url)

		if r.status_code == 200:
			count += 1
			info = json.loads(r.content)
			print(info)
		else:
			print('Failed to retrieve data')

		#Grab the country information and insert it into the table with artist name
		country = info['country']
		cur.execute('INSERT INTO Artists (name, country) VALUES (?,?)', (artist, country))
		conn.commit()

		#Sleep for 3 seconds after every request (1 request/sec limit...)
		time.sleep(3) 



def create_countries_table(cur, conn):
	cur.execute('''CREATE TABLE IF NOT EXISTS countries (
			 id PRIMARY INTEGER KEY AUTOINCREMENT,
			 name TEXT)''')
	
	cur.execute('''SELECT country FROM Artists''')
	country_list = cur.fetchall()

	for country in country_list:
		cur.execute('SELECT * FROM countries WHERE name = ?', (country,))
		check_country = cur.fetchone()[2]

		#If there already exists a row for that country, skip & go to the next
		if check_country != None:
			continue

		cur.execute('INSERT INTO countries (name) VALUES ?', (country,))





def main():
    cur, conn = db_setup('main.db')
    create_artists_table(cur, conn)
    create_countries_table(cur, conn)
    #create_news_database(news_dict, curr, con)

main()




'''
Everytime you run the code, the count will reset so that you only retrieve 25 items at a time
Inside the for loop, have a mechanism where you check if the artist you're trying to input already
exists in the table. If it does, skip the entire rest of the loop and move to the next artist. The next 
artist will also go through the same round of checks, and after all the artists that already exist are 
skipped, it should be able to pass the checks and start making requests for artists that don't exist.
'''

'''
	#Create a list of unique countries based off the artist dictionary
	country_list = []
	for country in data.values():
		if country not in country_list:
			country_list.append(country)
	
	#Create a countries table and input the countries from the list
	cur.execute('CREATE TABLE IF NOT EXISTS countries (id INTEGER PRIMARY KEY, name TEXT UNIQUE)')

	for i in range(len(country_list)):
		cur.execute("INSERT OR IGNORE INTO Countries (id,name) VALUES (?,?)", 
			 		 (i, country_list[i]))
	'''