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
#get data for artist charting songs/dates
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
    for date in song_dates:
            
        if date[0] not in artist_dict[artist[0]]:
            artist_dict[artist[0]][date[0]] = 1
        else:
            artist_dict[artist[0]][date[0]] += 1

#get data for artist news
i = 0

news_dict = {}
for artist in top_5_artists:
    cur.execute('''SELECT date FROM News
                WHERE id BETWEEN ? AND ?''',
                (i, (i + 25)))
    i += 25
    news_dates = cur.fetchall()
    news_dict[artist[0]] = {}
    for news_date in news_dates:
        for date in news_date:
            date = str(date)
            if date not in news_dict[artist[0]]:
                news_dict[artist[0]][date] = 1
            else:
                news_dict[artist[0]][date] += 1

plt.figure(figsize=(15, 10))

#create plot

for artist in artist_dict:
    dates = artist_dict[artist].keys()
    values = artist_dict[artist].values()
    plt.scatter(dates, values)

plt.figure(figsize=(15, 10))

for artist in news_dict:
    dates = sorted(news_dict[artist].keys())
    values = news_dict[artist].values()
    plt.plot(dates, values)
plt.show()
conn.close()

pass