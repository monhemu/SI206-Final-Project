import requests
import json
import sqlite3
import http.client, urllib.parse
import re

ACCESS_KEY = 'bf6ba9f4c17c5ff1f55aa4da2b3c356fd32e2c332d04a155ead918c1a819321c'

def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn

def find_top_artists():
    '''SELECT		TOP 1 songs
        FROM		Students
        GROUP BY	artist
        ORDER BY	artist DESC'''
    pass