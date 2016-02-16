#!/usr/bin/env python

import sys
import datetime
from People import *
from Read_file import *
from Calculation import *

month     = ['Feb']
investors = ['Alan', 'Sandra']
directory = '/Users/josevazquezgonzalez/Desktop/TODOs/Investing/New_test'

today = datetime.date.today()
hoy   = int(today.strftime('%d'))


    #Select a particular person
if len(sys.argv) > 1 :
    if sys.argv[1] in investors:
        Person = eval(sys.argv[1])()
    else:
        sys.exit("** Error: Person not found in the list")
else:
    sys.exit("** Error: Write person's name")


    #Read its deposit file
file = '/' + Person.name + '/' + Person.name + '_Res_depos.txt'
dates, depos = read_file(directory + file)


    #Perform the calculation of total interest
A = Calculation(Person, month, dates, depos)
A.interest(hoy)
print A.total()

#print month
#print len(x[0])