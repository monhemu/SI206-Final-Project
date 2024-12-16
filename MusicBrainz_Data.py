import json
import sqlite3
import os
import requests
import time

def db_setup(db_name):
    """
    Set up connection to the database and return connection and cursor.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return conn, cur

def create_artists_table(cur, conn):
    """
    Creates a table of artists and their associated countries by querying the MusicBrainz API.

    Args:
        cur (cursor): The database cursor object.
        conn (connection): The database connection object.
    """
    # Create the Artists table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Artists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            country TEXT
        )
    ''')
    conn.commit()

    # Fetch a list of unique artists from the songs table
    cur.execute('SELECT DISTINCT artist FROM songs')
    artist_list = [row[0] for row in cur.fetchall()]  # Convert list of tuples to a list of strings

    count = 0

    for artist in artist_list:
        if count >= 25:  # Stop after processing 25 artists
            print('Retrieved a set of 25 rows.')
            break

        # Check if the artist already exists in the Artists table
        cur.execute('SELECT * FROM Artists WHERE name = ?', (artist,))
        if cur.fetchone():  # Skip if the artist already exists
            print(f"Found in database: {artist}")
            continue

        # Make the API request to MusicBrainz
        url = f'https://musicbrainz.org/ws/2/artist/?query={artist}&fmt=json'
        r = requests.get(url)
        
        if r.status_code == 200:
            info = json.loads(r.content)

            # Attempt to retrieve the country information
            if 'artists' in info and len(info['artists']) > 0:
                country = info['artists'][0].get('country', 'Unknown')  # Default to 'Unknown' if country not found
                cur.execute('INSERT INTO Artists (name, country) VALUES (?, ?)', (artist, country))
                conn.commit()
                print(f"Added: {artist} (Country: {country})")
                count += 1
            else:
                print(f"No country information found for artist: {artist}")
        else:
            print(f"Failed to retrieve data for {artist}. Status code: {r.status_code}")

        # Sleep to respect the rate limit of MusicBrainz API
        time.sleep(2)



def create_countries_table(cur, conn):
    #Create table named countries
    cur.execute('CREATE TABLE IF NOT EXISTS countries (id INTEGER PRIMARY KEY, name TEXT)')
    conn.commit()

    cur.execute('SELECT DISTINCT country FROM Artists')
    country_list = [row[0] for row in cur.fetchall()]  # Convert list of tuples to a list of strings

    for country in country_list:
        cur.execute('''INSERT INTO countries (name) VALUES (?)''', (country,))

    conn.commit()


def correct_artist_ids(cur, conn):
    cur.execute('''ALTER TABLE songs ADD COLUMN artist_id INT''')
    cur.execute('''UPDATE songs 
                SET artist_id = Artists.id
                FROM Artists
                WHERE songs.artist = Artists.name''')
    
    cur.execute('''ALTER TABLE songs DROP COLUMN artist''')
    conn.commit()


def correct_country_ids(cur, conn):
    cur.execute('''ALTER TABLE Artists ADD COLUMN country_id INT''')
    cur.execute('''UPDATE Artists 
                SET country_id = countries.id
                FROM countries
                WHERE Artists.country = countries.name''')
    
    cur.execute('''ALTER TABLE Artists DROP COLUMN country''')
    conn.commit()



def main():
    # Set up the database connection
    conn, cur = db_setup('main.db')

    # Create the Artists table and populate it with data
    #create_artists_table(cur, conn)

    #correct_artist_ids(cur, conn)

    #create_countries_table(cur, conn)

    #correct_country_ids(cur, conn)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()
