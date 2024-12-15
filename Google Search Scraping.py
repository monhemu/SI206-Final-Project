import requests
from bs4 import BeautifulSoup
import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')
dates = [20241025, 20241101, 20241108, 20241115, 20241122, 20241129, 20241206, 20241213]
conn = sqlite3.connect('main.db')
cursor = conn.cursor()

#cursor.execute("DROP TABLE songs")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        artist TEXT NOT NULL,
        song TEXT NOT NULL,
        date TEXT NOT NULL,
        UNIQUE(song)
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
        rows = soup.find_all('tr')[1:51]
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

            cursor.execute("""
                SELECT COUNT(*) FROM songs WHERE song = ? AND artist = ?
            """, (song, artist))
            result = cursor.fetchone()

            if result[0] == 0:
                songs_to_insert.append((artist, song, str(date)))
                i += 1
                #print(i, artist, song)
            #else:
                #print(f" alr in db {artist} & {song}")

        cursor.executemany("""
            INSERT OR IGNORE INTO songs (artist, song, date)
            VALUES (?, ?, ?)
        """, songs_to_insert)
        conn.commit()
conn.close()
