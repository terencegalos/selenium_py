import requests
import pandas as pd

# Replace with your actual JSON link
url = 'https://ragonhouse.com/content/inventorydata/ciacinventory.json'

# Send HTTP request to the provided URL and save the response from server in a response object called r
r = requests.get(url)

# Load JSON data from the response
data = r.json()

# Convert JSON data into DataFrame
df = pd.DataFrame(data)

# Write DataFrame to CSV
df.to_csv('helper/csv/outfile/Ragon.csv', index=False)
