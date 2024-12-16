import matplotlib.pyplot as plt
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
conn.close()

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
plt.show()
