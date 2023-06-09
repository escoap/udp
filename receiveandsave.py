import csv
import json
import socket
import base64
import uuid
import requests
import re # Used for parsing parts of CallerID.com records
import sys # Used to terminate program

UDP_IP = "0.0.0.0"  # listen on all available network interfaces
UDP_PORT = 3520  # choose a port number that matches the device's configuration
CSV_FILE = "calls.csv"  # name of the CSV file to save the data to
LISTEN_ON_UDP_PORT = 3520
NON_DETAILED_PATTERN = ".*(\d\d) ([IO]) ([ESB]) (\d{4}) ([GB]) (.)(\d) (\d\d/\d\d \d\d:\d\d [AP]M) (.{14})(.{15})"
DETAILED_PATTERN = ".*(\d\d) ([NFR]) {13}(\d\d/\d\d \d\d:\d\d:\d\d)"
WEBHOOK_URL = "https://webhook.site/7d1bf192-e010-4a09-ba05-c7818885e550"  # URL of the webhook to send data to

def sendtohook(file, url):

# send the CSV data to the webhook
    response = requests.post(url, data=file)

# check the response status code and content
    if response.status_code == 200:
        print("CSV data sent successfully!")
        print(response.content)
    else:
        print("Error sending CSV data!")
        print(response.status_code)
        print(response.content)



def csvencode64(file):
    with open(file, 'rb') as csv_file:
        csv_bytes = csv_file.read()
        csv_base64 = base64.b64encode(csv_bytes).decode('utf-8')
    return csv_base64


def startdate(file):
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        first_row = next(reader) # Get the first row
        second_column = first_row[1] # Get the second column of the first row
        return second_column

def enddate(file):
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        last_row = None
        for row in reader:
            last_row = row
    second_column = last_row[1] # Get the second column of the last row
    return second_column

def toJson(record_start, record_end, record_count, records):

    UUID = str(uuid.uuid4())
    data = {
        "record_start": record_start,
        "record_end": record_end,
        "record_format": "csv",
        "record_count": record_count,
        "records": records,
        "id": UUID,
        "id_client": "168E62D0-4E61-4144-8069-0D7784C59776"
    }

    json_data = json.dumps(data, indent=4)
    return json_data

def recordcount(file):
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        row_count = sum(1 for row in reader) - 1

    return row_count


# TAKE INPUT DATA AND PARSE PARTS
def parse_packet(packet):

    # Decode packet from bytes to readable text
    packet = packet.decode("utf-8")

    non_detailed_match = re.search(NON_DETAILED_PATTERN, packet)
    detailed_match = re.search(DETAILED_PATTERN, packet)

    # Call type
    detailed_call = False

    # Parsed non_detailed variables for use in program
    pLineNumber = ""
    pInboundOrOutbound = ""
    pStartOrEnd = ""
    pDuration = ""
    pCheckSum = ""
    pRingType = ""
    pRings = ""
    pDateTime = ""
    pNumber = ""
    pName = ""

    # Parsed detailed variables for use in program
    pDetailedStatus = ""
    pDetailedDate = ""

    # If call is a non-deatiled packet
    if non_detailed_match:

        # Set call type
        detailed_call = False

        # Parse variables
        pLineNumber = non_detailed_match.group(1)
        pInboundOrOutbound = non_detailed_match.group(2)
        pStartOrEnd = non_detailed_match.group(3)
        pDuration = non_detailed_match.group(4)
        pCheckSum = non_detailed_match.group(5)
        pRingType = non_detailed_match.group(6)
        pRings = non_detailed_match.group(7)
        pDateTime = non_detailed_match.group(8)
        pNumber = non_detailed_match.group(9)
        pName = non_detailed_match.group(10)

        # For testing purposes - check variables
        print("Call Record ----------\n")
        print("Line: " + pLineNumber + "\n")
        print("IO: " + pInboundOrOutbound + "\n")
        print("SE: " + pStartOrEnd + "\n")
        print("DUR: " + pDuration + "\n")
        print("CHKS: " + pCheckSum + "\n")
        print("Ring: " + pRingType + pRings + "\n")
        print("DateTime: " + pDateTime + "\n")
        print("Number: " + pNumber + "\n")
        print("Name: " + pName + "\n")
        print("----------------------\n")

        call_data = {
        "timestamp": pDateTime,
        "number": pNumber,
        "name": pName
    }

    # write the Csv object to the file
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([call_data['number'], call_data['timestamp'],call_data['name']])



sendtohook(toJson(startdate(CSV_FILE),enddate(CSV_FILE),recordcount(CSV_FILE), csvencode64(CSV_FILE)), WEBHOOK_URL)
# create a UDP socket and bind it to the specified IP address and port number
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind((UDP_IP, UDP_PORT))

# print("Listening for UDP packets on port {}...".format(UDP_PORT))

# # create a CSV file and write a header row
# with open(CSV_FILE, "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerow(["number", "timestamp", "name", "call_type", "call_duration"])

# # continuously receive UDP packets and write their contents to the CSV file
# while True:
#     data, addr = sock.recvfrom(1024)  # receive up to 1024 bytes of data
#     parse_packet(data)
#     print(data)