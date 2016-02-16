
import csv
from People import *

def read_file(name):
    with open(name, 'rb') as f:
        reader = csv.DictReader(f , delimiter='\t')
        dates, depos = [], []
        for row in reader:
            dates.append(row['Date'])
            depos.append(float(row['Deposito']))


        return dates, depos


