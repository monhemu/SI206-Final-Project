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

def create_countries_table(cur, conn):
    """
    Creates a table of artists and their associated countries by querying the MusicBrainz API.

    Args:
        cur (cursor): The database cursor object.
        conn (connection): The database connection object.
    """
    
    #Create table named countries
    cur.execute('CREATE TABLE IF NOT EXISTS countries (id INTEGER PRIMARY KEY, name TEXT)')
    conn.commit()

    #Create an intermediate table named country_to_artist
    cur.execute('''CREATE TABLE IF NOT EXISTS country_to_artist (
                artist_id INTEGER PRIMARY KEY, 
                artist TEXT, 
                country TEXT)''')

    # Fetch a list of artist names from the artists table
    cur.execute('SELECT name FROM artists')
    artist_list = [row[0] for row in cur.fetchall()]  # Convert list of tuples to a list of strings
    count = 0

    
    for artist in artist_list:
        if count >= 25:  # Stop after processing 25 artists
            print('Retrieved a set of 25 rows.')
            break
        

        # Make the API request to MusicBrainz
        url = f'https://musicbrainz.org/ws/2/artist/?query={artist}&fmt=json'
        r = requests.get(url)
        
        if r.status_code == 200:
            info = json.loads(r.content)

            # Attempt to retrieve the country information
            if 'artists' in info and len(info['artists']) > 0:
                country = info['artists'][0].get('country', 'Unknown')  # Default to 'Unknown' if country not found
                
                cur.execute('INSERT INTO country_to_artist (artist, country) VALUES (?,?)', (artist, country))
                conn.commit()

                # Check if the country already exists in the countries table
                cur.execute('SELECT * FROM countries WHERE name = ?', (country,))
                if cur.fetchone():  # Skip if the country already exists
                    print(f"Found in database: {country}")
                    continue

                cur.execute('INSERT INTO countries (name) VALUES (?)', (country,))
                conn.commit()
                
                print(f"Added: {country})")
                count += 1
            else:
                print(f"No country information found for artist: {artist}")
        else:
            print(f"Failed to retrieve data for {artist}. Status code: {r.status_code}")

        # Sleep to respect the rate limit of MusicBrainz API
        time.sleep(1.1)



def assign_country_ids(cur, conn):
    cur.execute('''ALTER TABLE artists ADD COLUMN country_id INTEGER''')
    conn.commit()
    cur.execute('''UPDATE artists
                SET country_id = (
                SELECT countries.id
                FROM countries
                JOIN country_to_artist ON countries.name = country_to_artist.country
                WHERE country_to_artist.artist_id = artists.id)''')
    conn.commit()



def main():
    # Set up the database connection
    conn, cur = db_setup('main.db')

    # Create the Artists table and populate it with data
    create_countries_table(cur, conn)

    #Assign country ids to each artist in the artists table
    assign_country_ids(cur, conn)

    conn.close()

if __name__ == "__main__":
    main()
