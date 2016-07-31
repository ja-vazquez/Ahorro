
import csv
import os, sys
import pylab
import numpy as np
import pandas as pd
from People import *
import matplotlib.pyplot as plt
pd.set_option('display.mpl_style', 'default')

params1 = {'backend': 'pdf',
               'axes.labelsize': 12,
               'text.fontsize': 16,
               'xtick.labelsize': 18,
               'ytick.labelsize': 18,
               'legend.fontsize': 16,	
               'lines.markersize': 16,
               'font.size': 16,}
pylab.rcParams.update(params1)


def call_error():
    print ''
    sys.exit(" ------------------"
             " Error: Write person's name "
             "-------------------")


def traslation(mon):
    month_spa = {'Jan':'Enero', 'Feb':'Febrero',
                 'Mar':'Marzo', 'Apr':'Abril', 'May':'Mayo',
                 'Jun':'Junio', 'Jul':'Julio', 'Aug':'Agosto',
                 'Sep':'Septiembre', 'Oct':'Octubre', 'Nov':'Noviembre',
                 'Dec':'Diciembre'}
    return month_spa[mon]



def read_file(name):
    """Read depos file"""
    return pd.read_csv(name, sep='\s', skiprows=[0], names=['Dates', 'Deposits'])



def make_plot(ax, xinfo, yinfo, color='lime', legend="legend",
              ylabel='ylabel', xlabel='Fecha', title="title",
              extra_yinfo=None, extra_color='red'):

    opacity, bar_width = 1.0, 0.5
    spc = bar_width/2.0
    lxinfo = len(xinfo)

    for l in range(lxinfo):
        plt.bar(spc + bar_width, yinfo[l], bar_width, color=color, alpha=opacity)
        if extra_yinfo is not None:
            plt.bar(spc + bar_width, extra_yinfo[l], bar_width, color=extra_color, alpha= opacity)
        spc += 2.*bar_width
    pylab.xticks([bar_width*2. + n for n in range(lxinfo)], ([xinfo[n] for n in range(lxinfo)]))

    ax.legend(([legend]), frameon=False, fontsize='x-large')
    ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=45)
    ax.set_ylabel(ylabel, size=20)
    ax.set_xlabel(xlabel, size=18)
    ax.set_title(title)
    ax.grid()
    pylab.ylim([0, np.array(yinfo).max()*1.2])
    



def make_latex(Person, Info, dir, today, month_name):
    with open('%s/%s/Edo_%s_%s.tex'%(dir, Info.all_months[-1], Person.name, Info.all_months[-1]), 'w') as f:

        input_1 = """
\documentclass[11pt,secnumarabic,nofootinbib,preprintnumbers,amsmath,amssymb,aps]{revtex4}
\usepackage[usenames]{color}
\usepackage{graphicx}
\usepackage{ulem}
\usepackage{hyperref}

\\frenchspacing
\def\\red{\\textcolor{red}}
\def\\blue{\\textcolor{blue}}
\\begin{document}
        """
        f.write(input_1 + '\n')

        f.write('\\title{ESTADO DE CUENTA: %s.2016}\n'%(Info.all_months[-1]))
        f.write('\\author{%s}\n'%(Person.full_name))
        f.write('\\email[Contacto:~]{%s}\n'%(Person.email))


        input_2 = """
\date{\\today}\n
\maketitle\n

Estado de cuenta correspondiente hasta  el %s-%s del 2016, considerando una
tasa de inter\\'es del %.1f\%% anual.\n
        """%(today, month_name, Person.perct*100*12)
        f.write(input_2 + '\n\n')


        input_3 = """
\\begin{table}[h!]
\\begin {center}
\\begin{tabular}{rccl}
\hline
\hline
\\vspace{0.1cm}
Fecha de transacci\\'on  \qquad \qquad & Monto \qquad \qquad&  \qquad \qquad Inter\\'es acumulado & \qquad  \qquad Total  \\\\
\hline
\\vspace{0.1cm}
        """
        f.write(input_3 + '\n\n')


        if len(Info.all_months) > 1:
            input_4 = """
$\leftarrow$ %s/16'  \qquad \qquad & \$%.2f MXN     & \qquad \qquad  \$%.2f MXN & \qquad \qquad   \$%.2f MXN   \\\\
            """%(Info.all_months[-1], Info.final[-2], Info.cumul_inter[-1], Info.final[-2] + Info.cumul_inter[-1])
            f.write(input_4 + '\n\n')

            Info.kk = Info.kk + 1           #need to check the reason of this

        for n in range(Info.kk, 0, -1):
            input_5 = """
%s/16'  \qquad  \qquad  & \$%.2f MXN   & \qquad \qquad  \$%.2f MXN & \qquad \qquad   \$%.2f MXN      \\\\
            """%(Info.dates[-n], Info.depos[-n], Info.interes[-n], Info.depos[-n] + Info.interes[-n])
            f.write(input_5 + '\n\n')


        input_6 = """
\hline
-                       \qquad  \qquad  &- & \qquad \qquad - & \qquad \qquad    \color{blue}{= \$ \\bf %.2f MXN}     \\\\
        """%(Info.final[-1])
        f.write(input_6 + '\n\n')


        input_7 = """
\hline
\hline
\end{tabular}
\label{tab:omega}
\end{center}
\end{table}

\\begin{figure}[h!]
\\begin{center}
\\includegraphics[trim = 1mm -2mm 1mm 10mm, clip, width=14cm, height=8cm]{Plots_%s_%s.pdf}

\caption{Izquierda: dep\\'ositos realizados hasta %s-2016.
Derecha: monto total acumulado en la cuenta hasta  el %s-%s-2016.}
\label{fig:alpha}
\end{center}
\end{figure}

        """%(Person.name, Info.all_months[-1], month_name, today, month_name)
        f.write(input_7+'\n')

        f.write("\centering {Anual   \qquad \qquad Deposito \qquad \qquad Inter\\'es acumulado \qquad  \qquad Total \qquad \qquad \hspace{2cm}}\\\\  \n")

        f.write("\centering {2016: \qquad  \\fbox{\qquad   \$ %5.2f \qquad  ,\qquad   \$ %5.2f \qquad ,\qquad    \$ %5.2f \qquad}}\\\\ \n"%(
            Info.sum_tot_depos[-1], Info.final[-1] - Info.sum_tot_depos[-1], Info.final[-1]))


        if Person.depos_2015 != 0:
            f.write("\centering {2015: \qquad  \\fbox{\qquad   \$ %5.2f \qquad  ,\qquad   \$ %5.2f \qquad ,\qquad    \$ %5.2f \qquad}}\\\\ \n \n"%(
                Person.depos_2015, Person.final_2015 - Person.depos_2015, Person.final_2015))


        f.write('\end{document}')










