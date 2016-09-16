#!/usr/bin/env python

import os, sys
import datetime
from People import *
from Useful import *
from send_info import *
from Calculation import *
import matplotlib.pyplot as plt
from matplotlib import gridspec


print ('Add projections for the end of the year')
print ('i.e. if you keep that amount you\'ll geg ? at the end of the year')

    #Information about people
Make_plot  = True
Run_latex  = True
Edo_cuenta = True
months     = ['Jul', 'Aug', 'Sep']



    #Up to which date
today_date  = datetime.date.today()
#today_date  = datetime.date(2016,07,31)

today_day   = int(today_date.strftime('%d'))
today_month = today_date.strftime("%b")
today_month_name  = traslation(today_month)




    #Select a particular person
try:
    if len(sys.argv) > 1 : Person = eval(sys.argv[1])()
    else:                  call_error()
except:
    call_error()



    #Read its deposit file
directory  = 'Investors/' + Person.name
file_name  = '/' + directory + '/' + Person.name + '_Res_depos.txt'
global_dir = os.path.dirname(os.path.realpath(__file__))
file_deposits  = read_file(global_dir + file_name)



    #Perform the calculation of total interest
Calc = Calculation(Person, months, file_deposits)
Calc.calcu_interest(today_date)
df = Calc.df_deposits.set_index('Dates')
dm = Calc.group_monthly

dir_month   = directory + '/' + Calc.total_months[-1]
fname_month = Person.name + '_' + Calc.total_months[-1]

    #Create folder to put files
commd = """ mkdir %s"""%(dir_month)
os.system(commd)



    #Now we produce some plots
if Make_plot:
    fig = plt.figure(figsize = (12, 10))
    gs  = gridspec.GridSpec(1, 2, width_ratios= [3, 2.5])

    ax1= plt.subplot(gs[0])
    make_plot(ax1, df['Deposits'], ylim=df['Deposits'].max()*1.2,
          title  = 'Depositos realizados',
          label  = 'Depositado = $%5.2f'%(df['Deposits'].sum()),
          ylabel = 'Depositos (MXN)')
    plt.axhline(y=0, color='k')

    ax2= plt.subplot(gs[1])
    make_plot(ax2, dm[['cum_depos','plot_interest']],
          ylim   = dm['cum_depos'].max()*1.3, color=['blue','Magenta'],
          title  = 'Total acumulado',
          ylabel = 'Total (MXN)')

    L= plt.legend()
    L.get_texts()[0].set_text('Depositos')
    L.get_texts()[1].set_text('Total =  $%5.2f'%(dm['cum_total'][-1]))

    plt.subplots_adjust(wspace=0.4)
    pylab.savefig(dir_month + '/' + 'Plots_' + Person.name + '_'
                            + Calc.total_months[-1] + ".pdf")
    #plt.show(block=True)



    #Latex is next
if Run_latex:
    make_latex(Person, Calc, dir_month, today_day, today_month_name)
    Calc.group_monthly.to_csv('{0}/Edo_{1}.csv'.format(dir_month, fname_month))

    #Run everything
if Edo_cuenta:
    command = """
    cd {0}
    pdflatex Edo_{1}.tex
    open -a Preview Edo_{1}.pdf
    rm *aux *log *out
    """.format(dir_month, fname_month)
    os.system(command)



#Send mails from google account
enviar_mail = raw_input("Enviar mail? (yes/no) ")

if enviar_mail == 'yes':
    passw = raw_input("Enter password :")
    to = Person.email
    pdf_file = "{0}/Edo_{1}.pdf".format(dir_month, fname_month)
    mail(to, 'Edo de cuenta %s'%(Calc.total_months[-1]), msge(Calc.total_months[-1]), pdf_file, passw)
    print ('Mail enviado a', Person.email)
