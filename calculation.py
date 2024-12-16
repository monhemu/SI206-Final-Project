import sqlite3
conn = sqlite3.connect("main.db")
cur = conn.cursor()

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
        
conn.close()
