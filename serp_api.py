import requests
import json
import sqlite3
from serpapi import GoogleSearch
import re

ACCESS_KEY = 'bf6ba9f4c17c5ff1f55aa4da2b3c356fd32e2c332d04a155ead918c1a819321c'

def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn

def find_searches():
    params = {
    "engine": "google_trends",
    "q": "coffee,milk,bread,pasta,steak",
    "data_type": "TIMESERIES",
    "api_key": "bf6ba9f4c17c5ff1f55aa4da2b3c356fd32e2c332d04a155ead918c1a819321c"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    interest_over_time = results["interest_over_time"]

    pass