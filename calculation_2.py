import sqlite3
conn = sqlite3.connect("main.db")
cur = conn.cursor()

#Calculation 1
cur.execute("""
    SELECT countries.name AS country_name, AVG(songs.weeks_on_list) AS avg_weeks
    FROM songs
    JOIN artists ON songs.artist_id = artists.id
    JOIN countries ON artists.country_id = countries.id
    GROUP BY countries.id ORDER BY avg_weeks DESC
""")
rows = cur.fetchall()

with open('average_weeks_by_nationality.txt', 'w', encoding='utf-8') as f:
    f.write("Average Weeks on Chart by Nationality:\n")
    for row in rows:
        country_name, avg_weeks = row
        f.write(f"{country_name}: {avg_weeks:.2f} weeks\n")

#Calculation 2
cur.execute('''
            SELECT name, id FROM countries
            ''')

countries_list = cur.fetchall()

lines = []

for i in range(len(countries_list)):
    num = 1
    cur.execute('''SELECT artists.name, COUNT(songs.id) as song_count
                    FROM artists
                    JOIN songs ON artists.id = songs.artist_id
                    WHERE country_id = ?
                    GROUP BY artists.name
                    ORDER BY song_count DESC
                    LIMIT 10''',
                    (countries_list[i][1],))
    top_10_artists = cur.fetchall()
    lines.append(f"\n")
    lines.append(f"Top Artists from {countries_list[i][0]}\n")
    for artist in top_10_artists:
        lines.append(f"{num}: {artist[0]}, number of songs on charts: {artist[1]}\n")
        num += 1
    if num == 10:
         num = 1

with open('top_artists_by_country.txt', 'w', encoding='utf-8') as f:
        f.write(f"Top Artists by Country\n")
        for line in lines:
             f.write(line)

conn.close()
