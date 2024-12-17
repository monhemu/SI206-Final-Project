import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect("main.db")
cur = conn.cursor()

cur.execute("""
    SELECT countries.name AS country_name, AVG(songs.weeks_on_list) AS avg_weeks
    FROM songs
    JOIN artists ON songs.artist_id = artists.id
    JOIN countries ON artists.country_id = countries.id
    GROUP BY countries.id
    ORDER BY avg_weeks DESC
""")
rows = cur.fetchall()

countries = []
avg_weeks = []

for row in rows:
    country_name, avg_weeks_value = row
    if country_name != "Unknown":
        countries.append(country_name)
        avg_weeks.append(avg_weeks_value)

plt.figure(figsize=(12, 8))
plt.bar(countries, avg_weeks, color='Goldenrod')

plt.xlabel('Country', fontsize=12)
plt.ylabel('Average Weeks on Chart', fontsize=12)
plt.title('Average Weeks on Chart by Nationality', fontsize=14)
plt.xticks(rotation=90)

plt.tight_layout()
plt.show()