import requests
import requests
import matplotlib.pyplot as plt


params = {
    'engine': 'google_trends',
    'q': 'COVID,COVID-19,coronavirus',
    'geo': 'US',
    'date': 'today 5-y',  
    'data_type': 'TIMESERIES',
    'csv' : 'true',  # This parameter is valid for CSV response
    'api_key': '79230c7427c06094bdbc3699e9ed066db3984d6de715971803155af1557bc684'
}

# URL for the Google Trends API on SerpAPI
url = 'https://serpapi.com/search.json'

# Make the GET request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Save the CSV if csv=true
    if params.get('csv') == 'true':
        with open('covid_trends.csv', 'w') as f:
            f.write(response.text)
    else:
        # Printing the interest_over_time dictionary
        print(data.get('interest_over_time', {}))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

