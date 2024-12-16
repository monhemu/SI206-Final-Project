import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect("main.db")
cursor = conn.cursor()

cursor.execute(
    """
    SELECT songs.song, songs.weeks_on_list
    FROM songs
    JOIN artists ON songs.artist_id = artists.id
    WHERE songs.weeks_on_list > 2
    ORDER BY songs.weeks_on_list DESC
    """
)

songs = cursor.fetchall()
conn.close()

song_names = [song for song, _ in songs]
weeks_on_chart = [weeks for _, weeks in songs]

plt.figure(figsize=(10, 8))
plt.barh(song_names, weeks_on_chart)
plt.xlabel("Weeks on Chart", fontsize=12)
plt.ylabel("Songs", fontsize=12)
plt.title("Longest Charting Songs (More than 2 Weeks)", fontsize=14)
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

