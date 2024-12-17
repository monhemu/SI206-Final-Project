import sqlite3
import matplotlib.pyplot as plt
import re

conn = sqlite3.connect("main.db")
cur = conn.cursor()

cur.execute('''SELECT artists.name, songs.artist_id, COUNT(songs.id) as song_count
                    FROM artists
                    JOIN songs ON artists.id = songs.artist_id
                    WHERE country_id = ?
                    GROUP BY artists.name
                    ORDER BY song_count DESC
                    LIMIT 5''',
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
    
    with open('Average # of Articles Published per Month for Top 5 US Artists.txt', 'w', encoding='utf-8') as f:
        f.write("Average # of Articles Published per Month for Top 5 US Artists\n")
        for line in lines:
             f.write(line)

conn.close()