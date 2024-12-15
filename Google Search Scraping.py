import requests
from bs4 import BeautifulSoup
import sqlite3

# URL of the page to scrape
dates = [20241206, 20241129, 20241122, 20241115, 20241108, 20241101, 20241025]

# Connect to the SQLite database (main.db)
conn = sqlite3.connect('main.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        artist TEXT NOT NULL,
        song TEXT NOT NULL,
        date TEXT NOT NULL,
        UNIQUE(artist, song, date)
    )
""")
conn.commit()  # Commit the changes to the database

# Loop through the dates and scrape data
for date in dates:
    # Construct the URL for the given date
    url = f"https://kworb.net/ww/archive/{date}.html"

    # Send GET request to fetch the content of the page
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find all rows in the table (the top 25 songs are in <tr> tags)
        rows = soup.find_all('tr')[1:26]  # Get the top 25 songs (skip header row)
        
        # List to hold the data to be inserted
        songs_to_insert = []
        
        # Extract song titles and artist names
        for row in rows:
            # Find the column that contains the song title and artist
            artist_and_title_column = row.find_all('td')[2]  # The artist and title are in the third column
            
            # Extract the song title and artist name
            artist_and_title = artist_and_title_column.find('div').text.strip()
            
            # Split the string into artist and song title
            if " - " in artist_and_title:
                artist, song = artist_and_title.split(" - ", 1)  # Only split once at the first occurrence of " - "
            else:
                artist, song = artist_and_title, ""  # If there's no hyphen, treat the whole string as the artist name
            
            # Add the song data and date to the list
            songs_to_insert.append((artist, song, str(date)))
        
        # Insert the data into the database (only 25 rows at a time)
        cursor.executemany("""
            INSERT OR IGNORE INTO songs (artist, song, date)
            VALUES (?, ?, ?)
        """, songs_to_insert)
        
        conn.commit()  # Commit the changes to the database
        
        print(f"Successfully inserted 25 songs for date {date}")
    else:
        print(f"Failed to retrieve the webpage for {date}. Status code: {response.status_code}")

# Close the connection to the database
conn.close()
