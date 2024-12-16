import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import sqlite3

conn = sqlite3.connect('main.db')
cur = conn.cursor()

cur.execute("""
    SELECT artists.name, COUNT(songs.id) as song_count
    FROM artists
    JOIN songs ON artists.id = songs.artist_id
    GROUP BY artists.name
    ORDER BY song_count DESC
""")

# Fetch results
results = cur.fetchall()

# Extract data for visualization
artist_names = [row[0] for row in results]
song_counts = [row[1] for row in results]

# Create a bar chart
plt.figure(figsize=(15, 10))
plt.bar(artist_names, song_counts, color='skyblue')
plt.xlabel("Number of Songs")
plt.ylabel("Artists")
plt.title("Number of Songs per Artist")
plt.gca().invert_yaxis() 
plt.tight_layout()

#plt.savefig("songs_per_artist.png")
#plt.show()

#visualization for artist news / charted songs
cur.execute('''SELECT artists.name, artists.id, COUNT(songs.id) as song_count
                FROM artists
                JOIN songs ON artists.id = songs.artist_id
                GROUP BY artists.name
                ORDER BY song_count DESC
                LIMIT 5''')

top_5_artists = cur.fetchall()
artist_dict = {}
for artist in top_5_artists:
    artist_dict[artist[0]] = {}
    cur.execute('''SELECT date FROM songs
                    WHERE artist_id = ?''',
                    (artist[1],))
    song_dates = cur.fetchall()
    print(song_dates)
    for date in song_dates:
            
        if date[0] not in artist_dict[artist[0]]:
            artist_dict[artist[0]][date[0]] = 1
        else:
            artist_dict[artist[0]][date[0]] += 1

plt.figure(figsize=(15, 10))

for artist in artist_dict:
    dates = artist_dict[artist].keys()
    values = artist_dict[artist].values()
    plt.scatter(dates, values)
#create line plot
plt.show()
conn.close()

pass