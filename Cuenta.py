#!/usr/bin/env python

import sys
import datetime
from People import *
from Useful import *
from Calculation import *
import matplotlib.pyplot as plt
from matplotlib import gridspec

    #Information about people
Make_plot = False
Edo_cuenta= True
month     = ['Feb']
investors = ['Alan', 'Sandra']
directory = '/Users/josevazquezgonzalez/Desktop/TODOs/Investing/Ahorro'

today = datetime.date.today()
hoy   = int(today.strftime('%d'))


    #Select a particular person
if len(sys.argv) > 1 :
    Person = eval(sys.argv[1])()
else:
    sys.exit("** Error: Write person's name")


    #Read its deposit file
file = '/' + Person.name + '/' + Person.name + '_Res_depos.txt'
dates, depos = read_file(directory + file)


    #Perform the calculation of total interest
A = Calculation(Person, month, dates, depos)
A.interest(hoy)
sum_tot_depos, final = A.total()


    #Now we produce some plots

if  Make_plot:
    fig = plt.figure(figsize = (12, 7))
    gs  = gridspec.GridSpec(1, 2, width_ratios= [3, 2.5])

    make_plot(plt.subplot(gs[0]), dates, depos,
          title='Depositos realizados',
          legend='Depositado = $%5.2f'%(sum_tot_depos[-1]),
          ylabel='Depositos (MXN)')

    make_plot(plt.subplot(gs[1]), A.months, final, color='Magenta',
          title='Total acumulado',
          legend='Total = $%5.2f'%(final[-1]),
          ylabel='Total (MXN)',
          extra_yinfo= sum_tot_depos, extra_color='DodgerBlue')

    plt.subplots_adjust(wspace=0.4)
    plt.show()

if Edo_cuenta:
    make_latex(Person, month)


#Lates is next