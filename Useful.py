
import csv
from People import *
import pylab
import numpy as np
import matplotlib.pyplot as plt

def read_file(name):
    with open(name, 'rb') as f:
        reader = csv.DictReader(f , delimiter='\t')
        dates, depos = [], []
        for row in reader:
            dates.append(row['Date'])
            depos.append(float(row['Deposito']))

        return dates, depos



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
    ax.set_ylabel(ylabel, size=20)
    ax.set_xlabel(xlabel, size=18)
    ax.set_title(title)

    pylab.ylim([0, np.array(yinfo).max()*1.2])
    ax.grid()



def make_latex(Person, Info, dir, hoy, nmonth):
    with open('%s/%s/Edo_%s_%s.tex'%(dir, Info.month[0], Person.name, Info.month[0]), 'w') as f:

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

        f.write('\\title{ESTADO DE CUENTA: %s.2016}\n'%(Info.month[0]))
        f.write('\\author{%s}\n'%(Person.full_name))
        f.write('\\email[Contacto:~]{%s}\n'%(Person.email))


        input_2 = """
\date{\\today}\n
\maketitle\n

Estado de cuenta correspondiente hasta  el %s-%s del 2016, considerando una
tasa de inter\\'es del %.1f\%% anual.\n
        """%(hoy, nmonth, Person.perct*100*12)
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


        if len(Info.months) > 1:
            input_4 = """
$\leftarrow$ %s/16'  \qquad \qquad & \$%.2f MXN     & \qquad \qquad  \$%.2f MXN & \qquad \qquad   \$%.2f MXN   \\\\
            """%(Info.month[0], Info.final[-2], Info.sum_tot_inter[-2], Info.final[-2] + Info.sum_tot_inter[-2])
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
\\includegraphics[trim = 1mm 1mm 1mm 1mm, clip, width=13cm, height=8cm]{Plots_%s_%s.pdf}

\caption{Izquierda: dep\\'ositos realizados hasta %s-2016.
Derecha: monto total acumulado en la cuenta hasta  el %s-%s-2016.}
\label{fig:alpha}
\end{center}
\end{figure}

        """%(Person.name, Info.months[-1], nmonth, hoy, nmonth)
        f.write(input_7+'\n')

        f.write("\centering {Anual   \qquad \qquad Deposito \qquad \qquad Inter\\'es acumulado \qquad  \qquad Total \qquad \qquad \hspace{2cm}}\\\\  \n")

        f.write("\centering {2016: \qquad  \\fbox{\qquad   \$ %5.2f \qquad  ,\qquad   \$ %5.2f \qquad ,\qquad    \$ %5.2f \qquad}}\\\\ \n"%(
            Info.sum_tot_depos[-1], Info.final[-1] - Info.sum_tot_depos[-1], Info.final[-1]))


        if Person.depos_2015 != 0:
            f.write("\centering {2015: \qquad  \\fbox{\qquad   \$ %5.2f \qquad  ,\qquad   \$ %5.2f \qquad ,\qquad    \$ %5.2f \qquad}}\\\\ \n \n"%(
                Person.depos_2015, Person.final_2015 - Person.depos_2015, Person.final_2015))


        f.write('\end{document}')










