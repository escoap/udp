import base64

with open('calls.csv', 'rb') as csv_file:
    csv_bytes = csv_file.read()
    csv_base64 = base64.b64encode(csv_bytes).decode('utf-8')

print(csv_base64)