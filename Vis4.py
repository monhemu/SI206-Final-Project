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
print(results)

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
sizes = []

for num in counts:
    sizes.append(num/(total))

ax.pie(sizes, labels=country)
ax.set_title('Country Representation by Artist (No US, Unknown)')
plt.show()
