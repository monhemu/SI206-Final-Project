import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect("main.db")
cur = conn.cursor()
cur.execute("SELECT song, weeks_on_list FROM songs ORDER BY weeks_on_list DESC")
data = cur.fetchall()
conn.close()

songs_worth_graphing = []
for song, weeks in data:
    if weeks >= 2:
        song_tup = (song, weeks)
        songs_worth_graphing.append(song_tup)

sorted_songs = sorted(songs_worth_graphing, key=lambda x: x[0], reverse=True)
sorted_weeks = sorted(songs_worth_graphing, key=lambda x: x[1], reverse=True)

songs = [song for song, _ in sorted_songs]
weeks = [weeks for _, weeks in sorted_weeks]

plt.figure(figsize=(10, 8))
plt.bar(songs, weeks)

plt.xlabel("Song Names", fontsize=12)
plt.ylabel("Weeks on List", fontsize=12)
plt.title("Number of Weeks Songs Stayed on the Top Songs List", fontsize=12)

plt.xticks(rotation=90, fontsize=5)

plt.savefig("song_weeks.png")
plt.show()
