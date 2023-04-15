import csv
import requests

CSV_FILE = "calls.csv"  # name of the CSV file to read from
WEBHOOK_URL = "https://webhook.site/7d1bf192-e010-4a09-ba05-c7818885e550"  # URL of the webhook to send data to

# read the CSV file and encode it using UTF-8
with open(CSV_FILE, "r", encoding="utf-8") as f:
    csv_data = f.read().encode("utf-8")

# send the CSV data to the webhook
response = requests.post(WEBHOOK_URL, data=csv_data)

# check the response status code and content
if response.status_code == 200:
    print("CSV data sent successfully!")
    print(response.content)
else:
    print("Error sending CSV data!")
    print(response.status_code)
    print(response.content)
