#!/usr/bin/env python

import os, sys
import datetime
from People import *
from Useful import *
from Calculation import *
import matplotlib.pyplot as plt
from matplotlib import gridspec


print 'Add projections for the end of the year'
print 'i.e. if you keep that amount you\'ll geg ? at the end of the year'

    #Information about people
Make_plot = True
Edo_cuenta= True
nmonth    = 'Febrero'
month     = ['Feb']
directory = '/Users/josevazquezgonzalez/Desktop/TODOs/Investing/Ahorro'


    #Up to which date
today = datetime.date.today()
hoy   = 29 #int(today.strftime('%d'))



    #Select a particular person
if len(sys.argv) > 1 :
    Person = eval(sys.argv[1])()
else:
    sys.exit("** Error: Write person's name")



    #Read its deposit file
dir  = 'Investors/' + Person.name
file = '/' + dir + '/' + Person.name + '_Res_depos.txt'
dates, depos = read_file(directory + file)


    #Perform the calculation of total interest
Info = Calculation(Person, month, dates, depos)
Info.interest(hoy)
Info.total()


    #Create folder to put files
commd = """ mkdir %s/%s
"""%(dir, Info.months[-1])
os.system(commd)

print Info.months
    #Now we produce some plots
if  Make_plot:
    fig = plt.figure(figsize = (12, 7))
    gs  = gridspec.GridSpec(1, 2, width_ratios= [3, 2.5])

    make_plot(plt.subplot(gs[0]), Info.dates, Info.depos,
          title = 'Depositos realizados',
          legend= 'Depositado = $%5.2f'%(Info.sum_tot_depos[-1]),
          ylabel= 'Depositos (MXN)')

    make_plot(plt.subplot(gs[1]), Info.months, Info.final, color='Magenta',
          title = 'Total acumulado',
          legend= 'Total = $%5.2f'%(Info.final[-1]),
          ylabel= 'Total (MXN)',
          extra_yinfo= Info.sum_tot_depos, extra_color='DodgerBlue')

    plt.subplots_adjust(wspace=0.4)
    pylab.savefig(dir + '/' + Info.months[-1]+'/'+'Plots_' + Person.name + '_' + Info.months[-1] + ".pdf")
    plt.show()


    #Lates is next
if Edo_cuenta:
    make_latex(Person, Info, dir, hoy, nmonth)


    #Run everything
if Edo_cuenta:
    command = """
    cd %s/%s
    pdflatex Edo_%s_%s.tex
    open -a Preview Edo_%s_%s.pdf
    rm *aux *log *out
    """%(dir, Info.months[-1], Person.name, Info.month[0], Person.name, Info.month[0])
    os.system(command)

