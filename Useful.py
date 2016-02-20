
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



def make_latex(Person, month):
    with open('Edo_%s_%s.tex'%(Person.name, month[0]), 'w') as f:

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

        f.write('\\title{ESTADO DE CUENTA: %s.2016}\n'%(month[0]))
        f.write('\\author{%s}\n'%(Person.full_name))
        f.write('\\email[Contacto:~]{%s}\n'%(Person.email))


        input_2 = """
\date{\\today}\n
\maketitle\n

Estado de cuenta correspondiente al mes de %s del 2016, considerando una
tasa de inter\\'es del %.1f\%% anual~\\footnote{IVA incluido.}.\n
        """%(month[0], Person.perct*100*12)
        f.write(input_2 + '\n\n')


        input_3 = """
\\begin{table}[h!]
\\begin {center}
\\begin{tabular}{rccl}
\hline
\hline
\\vspace{0.1cm}
Fecha de transacci\\'on  \qquad \qquad & Monto \qquad \qquad&  \qquad \qquad Inter\\'es & \qquad  \qquad Total  \\\\
\hline
\\vspace{0.1cm}
        """
        f.write(input_3 + '\n\n')
















