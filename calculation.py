import sqlite3
conn = sqlite3.connect("main.db")
cur = conn.cursor()
cur.execute("""
    SELECT Artists.country_id, AVG(songs.weeks_on_list) as weeks_on_list
    FROM songs
    JOIN Artists ON songs.artist_id = Artists.id
    GROUP BY Artists.country_id
    ORDER BY weeks_on_list DESC
""")


rows = cur.fetchall()

with open('average_weeks_by_nationality.txt', 'w') as f:
    f.write(f"Average Weeks on Chart by Nationality:\n")
    for row in rows:
        nationality, avg_weeks = row
        f.write(f"{nationality}: {avg_weeks:.2f} weeks\n")

print("Average weeks on chart by nationality written to 'average_weeks_by_nationality.txt'")
conn.close()
