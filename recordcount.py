import csv
def recordcount(file):
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        row_count = sum(1 for row in reader) - 1

    return row_count