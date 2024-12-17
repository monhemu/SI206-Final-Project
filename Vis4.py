import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import sqlite3

conn = sqlite3.connect('main.db')
cur = conn.cursor()

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

conn.close()

#Create figure and ax objects
fig, ax = plt.subplots()

#With US, Unknown data
country, counts = zip(*results)
country = list(country)
counts = list(counts)

country.remove('US')
country.remove('Unknown')
counts = counts[2:]

total = sum(counts)
labels, sizes = [], []

for num in counts:
    percent = num*100/(total)
    sizes.append(percent)

for size in sizes:
    label = f"{size:.1f}%"
    labels.append(label)

ax.pie(sizes, labels=labels)
ax.set_title('Country Representation by Artist (No US, Unknown)')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', labels=country)
plt.show()


