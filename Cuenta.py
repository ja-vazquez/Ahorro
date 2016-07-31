#!/usr/bin/env python

import os, sys
import datetime
from People import *
from Useful import *
import datetime as dt
import pandas as pd
from send_info import *
from Calculation import *
import matplotlib.pyplot as plt
from matplotlib import gridspec


print 'Add projections for the end of the year'
print 'i.e. if you keep that amount you\'ll geg ? at the end of the year'

    #Information about people
Make_plot  = False
Edo_cuenta = False
Send_mail  = False
months     = ['Feb','Mar', 'Apr', 'May','Jun','Jul']



    #Up to which date
today_date  = datetime.date.today()

#today_day   = int(today_date.strftime('%d'))
today_month = today_date.strftime("%b")
today_month_name  = traslation(today_month)


    #Select a particular person
try:
    if len(sys.argv) > 1 :
        Person = eval(sys.argv[1])()
    else:
        call_error()
except:
    call_error()


    #Read its deposit file
dir        = 'Investors/' + Person.name
file_name  = '/' + dir + '/' + Person.name + '_Res_depos.txt'
directory  = os.path.dirname(os.path.realpath(__file__))

file_deposits  = read_file(directory + file_name)

    #Perform the calculation of total interest
Info = Calculation(Person, months, file_deposits)
Info.calcu_interest(today_date)

#Info = Calculation(Person, months, dates, depos)
#Info.interest(today)
#Info.total()


    #Create folder to put files
commd = """ mkdir %s/%s
"""%(dir, Info.all_months[-1])
os.system(commd)


    #Now we produce some plots
if  Make_plot:
    fig = plt.figure(figsize = (14, 12))
    gs  = gridspec.GridSpec(1, 2, width_ratios= [3, 2.5])

    make_plot(plt.subplot(gs[0]), Info.dates, Info.depos,
          title  = 'Depositos realizados',
          legend = 'Depositado = $%5.2f'%(Info.sum_tot_depos[-1]),
          ylabel = 'Depositos (MXN)')

    make_plot(plt.subplot(gs[1]), Info.all_months, Info.final, color='Magenta',
          title  = 'Total acumulado',
          legend = 'Total = $%5.2f'%(Info.final[-1]),
          ylabel = 'Total (MXN)',
          extra_yinfo= Info.sum_tot_depos, extra_color='DodgerBlue')

    plt.subplots_adjust(wspace=0.4)
    pylab.savefig(dir + '/' + Info.all_months[-1] + '/' + 'Plots_' + Person.name + '_' + Info.all_months[-1] + ".pdf")
    plt.show()


    #Lates is next
if Edo_cuenta:
    make_latex(Person, Info, dir, today, this_month)


    #Run everything
if Edo_cuenta:
    command = """
    cd %s/%s
    pdflatex Edo_%s_%s.tex
    open -a Preview Edo_%s_%s.pdf
    rm *aux *log *out
    """%(dir, Info.all_months[-1], Person.name, Info.all_months[-1], Person.name, Info.all_months[-1])
    os.system(command)


    #Send mails from google account
if Send_mail:
    to = Person.email
    pdf_file = "%s/%s/Edo_%s_%s.pdf"%(dir, Info.all_months[-1], Person.name, Info.all_months[-1])
    mail(to, 'Edo de cuenta', msge(), pdf_file, 'pswd')

