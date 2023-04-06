import csv
import json
import socket
import re # Used for parsing parts of CallerID.com records
import sys # Used to terminate program

UDP_IP = "0.0.0.0"  # listen on all available network interfaces
UDP_PORT = 3520  # choose a port number that matches the device's configuration
CSV_FILE = "calls.csv"  # name of the CSV file to save the data to
LISTEN_ON_UDP_PORT = 3520
NON_DETAILED_PATTERN = ".*(\d\d) ([IO]) ([ESB]) (\d{4}) ([GB]) (.)(\d) (\d\d/\d\d \d\d:\d\d [AP]M) (.{14})(.{15})"
DETAILED_PATTERN = ".*(\d\d) ([NFR]) {13}(\d\d/\d\d \d\d:\d\d:\d\d)"
JSON_FILE = "calls.json"

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
        "name": pName,
        "call_type": pInboundOrOutbound,
        "call_duration": pDuration,
    }

    # write the Csv object to the file
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([call_data['number'], call_data['timestamp'],call_data['name'], call_data['call_type'], call_data['call_duration']])


    # If call is a detailed packet
    if detailed_match:

        # Set call type
        detailed_call = True

        # Parse variables
        pLineNumber = detailed_match.group(1)
        pDetailedStatus = detailed_match.group(2)
        pDetailedDate = detailed_match.group(3)

        # For testing purposes - check variables
        print("Detailed Record ----------\n")
        print("Line: " + pLineNumber + "\n")
        print("Status: " + pDetailedStatus + "\n")
        print("DateTime: " + pDetailedDate + "\n")
        print("--------------------------\n")

# create a UDP socket and bind it to the specified IP address and port number
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Listening for UDP packets on port {}...".format(UDP_PORT))

# create a CSV file and write a header row
with open(CSV_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["number", "timestamp", "name", "call_type", "call_duration"])

# continuously receive UDP packets and write their contents to the CSV file
while True:
    data, addr = sock.recvfrom(1024)  # receive up to 1024 bytes of data
    parse_packet(data)

    # parse the data from the UDP packet
    '''parts = data.decode().strip().split(",")
    print(parts)
    timestamp = parts[0]
    caller_id = parts[1]
    call_type = parts[2]
    call_duration = parts[3]

    # write the parsed data to the CSV file
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, caller_id, call_type, call_duration])

    print("Received UDP packet from {}: {}".format(addr, data))'''
