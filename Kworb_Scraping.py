import requests
from bs4 import BeautifulSoup
import sqlite3
import sys 
sys.stdout.reconfigure(encoding='utf-8')

dates = [20240906, 20240913, 20240920, 20240927, 20241004, 20241011,
         20241018, 20241025, 20241101, 20241108, 20241115, 20241122, 20241129,
         20241206, 20241213]

conn = sqlite3.connect('main.db')
cursor = conn.cursor()

#cursor.execute("DROP TABLE artists")
#cursor.execute("DROP TABLE songs")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS artists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        artist_id INTEGER NOT NULL,
        song TEXT NOT NULL UNIQUE,
        date TEXT NOT NULL,
        FOREIGN KEY (artist_id) REFERENCES artists (id)
    )
""")
conn.commit()

i = 0
for date in dates:
    if i >= 25:
        break

    url = f"https://kworb.net/ww/archive/{date}.html"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        rows = soup.find_all('tr')[1:26]
        songs_to_insert = []

        for row in rows:
            if i >= 25:
                break
            artist_and_title_column = row.find_all('td')[2]
            artist_and_title = artist_and_title_column.find('div').text.strip()
            if " - " in artist_and_title:
                artists, song = artist_and_title.split(" - ", 1)
                artist = artists.split(", ")[0]
            else:
                artist, song = artist_and_title, ""

            cursor.execute("SELECT id FROM artists WHERE name = ?", (artist,))
            artist_id = cursor.fetchone()

            if artist_id is None:
                cursor.execute("INSERT INTO artists (name) VALUES (?)", (artist,))
                conn.commit()
                artist_id = cursor.lastrowid
            else:
                artist_id = artist_id[0]

            cursor.execute("SELECT COUNT(*) FROM songs WHERE song = ?", (song,))
            song_exists = cursor.fetchone()[0]

            if song_exists == 0:
                songs_to_insert.append((artist_id, song, str(date)))
                i += 1
                print(f"{i}. Added song: {artist} - {song}")
            else:
                print(f"Skipped duplicate: {artist} - {song}")

        cursor.executemany("""
            INSERT OR IGNORE INTO songs (artist_id, song, date)
            VALUES (?, ?, ?)
        """, songs_to_insert)
        conn.commit()


conn.commit()
conn.close()
