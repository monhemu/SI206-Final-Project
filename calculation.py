import sqlite3
import re
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

#Calculation 3
cur.execute('''SELECT artists.name, songs.artist_id, COUNT(songs.id) as song_count
                    FROM artists
                    JOIN songs ON artists.id = songs.artist_id
                    WHERE country_id = ?
                    GROUP BY artists.name
                    ORDER BY song_count DESC
                    LIMIT 10''',
                    (1,))

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
sep_count = 0
oct_count = 0
nov_count = 0
dec_count = 0

lines = []

for artist_news in news_dict:
    for article in news_dict[artist_news]:
        if re.search(r'2024(09)\d{2}', str(article)):
            sep_count += 1
        elif re.search(r'2024(10)\d{2}', str(article)):
            oct_count += 1
        elif re.search(r'2024(11)\d{2}', str(article)):
            nov_count += 1
        elif re.search(r'2024(12)\d{2}', str(article)):
            dec_count += 1
    lines.append(f'''\nArtist: {artist_news}\n
                 Average # of Articles Published in September: {sep_count/4}
                 Average # of Articles Published in October: {oct_count/4}
                 Average # of Articles Published in November: {nov_count/4}
                 Average # of Articles Published in December: {dec_count/4}\n''')
    
    with open('Average # of Articles Published per Month for Top 10 US Artists.txt', 'w', encoding='utf-8') as f:
        f.write("Average # of Articles Published per Month for Top 10 US Artists\n")
        for line in lines:
             f.write(line)
conn.close()
