import csv

def parse(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        retlist = list(map(tuple, [map(int, line) for line in reader]))
    return retlist
