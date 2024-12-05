import requests
import json
import os
import sqlite3

API_KEY = '6COMVPIdPC3rnU6qrUcbYwNbpk6A8bay'

conn = sqlite3.connect("main.db")
cur = conn.cursor()

url = f"https://api.currencybeacon.com/v1/historical/?base=USD/?date=2024-01-01/?api_key={API_KEY}"
r = requests.get(url)

if r.status_code == 200:
    d = json.loads(r.content)
    print(d)
elif r.status_code == 401:
    print("Unauthorized Missing or incorrect API token in header.")
elif r.status_code == 422:
    print("Unprocessable Entity")
elif r.status_code == 500:
    print("Internal Server Error")
else:
    print("Other error")
