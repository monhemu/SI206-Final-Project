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
plt.bar(artist_names, song_counts, color='skyblue', width=0.6)
plt.xlabel("Number of Songs")
plt.ylabel("Artists")
plt.title("Number of Songs per Artist")
plt.xticks(rotation=90)
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
        int_date = int(date[0])
        if int_date not in artist_dict[artist[0]]:
            artist_dict[artist[0]][int_date] = 1
        else:
            artist_dict[artist[0]][int_date] += 1

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
            if date not in news_dict[artist[0]]:
                news_dict[artist[0]][date] = 1
            else:
                news_dict[artist[0]][date] += 1

plt.figure(figsize=(15, 10))
plt.xlabel('Dates')
plt.ylabel('Number of appearances')
plt.title('Number of Articles Written About Artist vs. Charted Songs')
#create plot

for artist in news_dict:
    dates = sorted(news_dict[artist].keys())
    print(dates)
    values = news_dict[artist].values()
    plt.plot(dates, values)

for artist in artist_dict:
    dates = sorted(artist_dict[artist].keys())
    values = artist_dict[artist].values()
    plt.scatter(dates, values)

legend = []
for artist in top_5_artists:
    legend.append(f'Articles About {artist[0]}')
for artist in top_5_artists:
    legend.append(f'Charting Songs For {artist[0]}')
plt.legend(legend)


plt.show()




cur.execute("""
    SELECT countries.name, COUNT(songs.id) as song_count
    FROM countries
    JOIN Artists ON countries.id = Artists.country_id
    JOIN songs ON Artists.id = songs.artist_id
    GROUP BY countries.name
    ORDER BY song_count DESC
""")

# Fetch results
results = cur.fetchall()
print(results)
song_total = 0

for tup in results:
    if tup[0] == 'Unknown' or tup[0] == 'US':
        results.remove(tup)

#song_total += tup[1]

country, size = zip(*results)
country = list(country)
size = list(size)

print(country)
print(size)

print(song_total)


conn.close()

pass

