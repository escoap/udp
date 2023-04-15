import csv
import socket
import re

UDP_IP = "0.0.0.0"
UDP_PORT = 3520
CSV_FILE = "calls.csv"
NON_DETAILED_PATTERN = ".*(\d\d) ([IO]) ([ESB]) (\d{4}) ([GB]) (.)(\d) (\d\d/\d\d \d\d:\d\d [AP]M) (.{14})(.{15})"
DETAILED_PATTERN = ".*(\d\d) ([NFR]) {13}(\d\d/\d\d \d\d:\d\d:\d\d)"

def parse_packet(packet):
    packet = packet.decode("utf-8")

    non_detailed_match = re.search(NON_DETAILED_PATTERN, packet)
    detailed_match = re.search(DETAILED_PATTERN, packet)

    detailed_call = False
    call_data = {}

    if non_detailed_match:
        detailed_call = False
        pLineNumber, pInboundOrOutbound, pStartOrEnd, pDuration, pCheckSum, pRingType, pRings, pDateTime, pNumber, pName = non_detailed_match.groups()

        call_data = {
            "timestamp": pDateTime,
            "number": pNumber,
            "name": pName,
            "call_type": pInboundOrOutbound,
            "call_duration": pDuration,
        }

    if detailed_match:
        detailed_call = True
        pLineNumber, pDetailedStatus, pDetailedDate = detailed_match.groups()

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([call_data.get('number', ''), call_data.get('timestamp', ''), call_data.get('name', ''), call_data.get('call_type', ''), call_data.get('call_duration', '')])

        if detailed_call:
            print("Detailed Record ----------\n")
            print("Line: " + pLineNumber + "\n")
            print("Status: " + pDetailedStatus + "\n")
            print("DateTime: " + pDetailedDate + "\n")
            print("--------------------------\n")
        else:
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


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Listening for UDP packets on port {}...".format(UDP_PORT))

with open(CSV_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["number", "timestamp", "name", "call_type", "call_duration"])

while True:
    data, addr = sock.recvfrom(1024)
    parse_packet(data)
