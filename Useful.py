
import sys
import pylab
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.mpl_style', 'default')

params1 = {'backend': 'pdf',
               'axes.labelsize': 15,
               'text.fontsize': 18,
               'xtick.labelsize': 18,
               'ytick.labelsize': 18,
               'legend.fontsize': 18,
               'lines.markersize': 16,
               'font.size': 16,}
pylab.rcParams.update(params1)


def call_error():
    print ('')
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
    file= pd.read_csv(name, sep='\s', skiprows=[0], names=['Dates', 'Deposits'])
    return file



def make_plot(ax, Info_df, ylim, color='LimeGreen', label=None,
              ylabel='ylabel', xlabel='Fecha', title="title"):

    df = Info_df
    df.plot.bar(color=color, label=label,
                stacked=True, alpha=0.8, ax=ax)

    plt.legend(loc='best', frameon=True)
    plt.ylim(ymax=  ylim)
    ax.set_title(title)
    ax.set_ylabel(ylabel, size=20)
    ax.set_xlabel(xlabel, size=18)




def make_latex(Person, Info, dir_month, today_day, today_month_name):
    #Latex has some problems with .format style
    fname_month = Person.name + '_' + Info.total_months[-1]
    with open('{0}/Edo_{1}.tex'.format(dir_month, fname_month), 'w') as f:

        Latex_text_1 = r"""
\documentclass[11pt,secnumarabic,nofootinbib,preprintnumbers,amsmath,amssymb,aps]{revtex4}
\usepackage[usenames]{color}
\usepackage{graphicx}
\usepackage{ulem}
\usepackage{hyperref}

\frenchspacing
\def\\red{\\textcolor{red}}
\def\\blue{\\textcolor{blue}}
\begin{document}
	"""
        f.write(Latex_text_1  + '\n')

        f.write('\\title{ESTADO DE CUENTA: %s.2016}\n'%(traslation(Info.total_months[-1])))
        f.write('\\author{%s}\n'%(Person.full_name))
        f.write('\\email[Contacto:~]{%s}\n'%(Person.email))



        Latex_text_2 = """
%%\date{\\today}\n
\maketitle\n

Estado de cuenta correspondiente hasta  el %s-%s del 2016, considerando una
tasa de inter\\'es del %.1f\%% anual.\n
        """%(today_day, today_month_name, Person.perct*100*365)
        f.write(Latex_text_2 + '\n\n')



        Latex_text_3 = """
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
        f.write(Latex_text_3 + '\n\n')



        if len(Info.total_months) > 1:
            Latex_text_4 = """
$\leftarrow$ %s/16'  \qquad \qquad & \$%.2f MXN     & \qquad \qquad  \$%.2f MXN & \qquad \qquad   \$%.2f MXN   \\\\
            """%(Info.total_months[-1], Info.group_monthly['cum_depos'][-2],
                 Info.group_monthly['cum_interest'][-2], Info.group_monthly['cum_total'][-2],)
            f.write(Latex_text_4 + '\n\n')



        # for the last month
        num_depos = Info.group_monthly['num_deposits'][-1]
        for n in range(num_depos, 0, -1):
            date_of_deposit = Info.df_deposits.iloc[-n]['Dates']
            deposits = Info.df_deposits.iloc[-n]['Deposits']
            interest = Info.df_deposits.iloc[-n]['tot_interest']
            total    = Info.df_deposits.iloc[-n]['total']
            Latex_text_5 = """
%s/16'  \qquad  \qquad  & \$%.2f MXN   & \qquad \qquad  \$%.2f MXN & \qquad \qquad   \$%.2f MXN      \\\\
            """%(date_of_deposit, deposits, interest, total)
            f.write(Latex_text_5 + '\n\n')




        Latex_text_6 = """
\hline
-                       \qquad  \qquad  &- & \qquad \qquad - & \qquad \qquad    \color{blue}{= \$ \\bf %.2f MXN}     \\\\
        """%(Info.group_monthly['cum_total'][-1])
        f.write(Latex_text_6 + '\n\n')




        Latex_text_7 = """
\hline
\hline
\end{tabular}
\label{tab:omega}
\end{center}
\end{table}

\\begin{figure}[h!]
\\begin{center}
\\includegraphics[trim = 1mm -2mm 1mm 1mm, clip, width=14cm, height=9cm]{Plots_%s.pdf}

\caption{Izquierda: dep\\'ositos realizados hasta %s-2016.
Derecha: monto total acumulado en la cuenta hasta  el %s-%s-2016.}
\label{fig:alpha}
\end{center}
\end{figure}

        """%(fname_month, today_month_name, today_day, today_month_name)
        f.write(Latex_text_7 +'\n')

        f.write("\centering {Anual   \qquad \qquad Deposito \qquad \qquad Inter\\'es acumulado \qquad  \qquad Total \qquad \qquad \hspace{2cm}}\\\\  \n")

        f.write("\centering {2016: \qquad  \\fbox{\qquad   \$ %5.2f \qquad  ,\qquad   \$ %5.2f \qquad ,\qquad    \$ %5.2f \qquad}}\\\\ "%(
            Info.group_monthly['cum_depos'][-1], Info.group_monthly['cum_interest'][-1], Info.group_monthly['cum_total'][-1]))


        if Person.depos_2015 != 0:
            f.write("\centering {2015: \qquad  \\fbox{\qquad   \$ %5.2f \qquad  ,\qquad   \$ %5.2f \qquad ,\qquad    \$ %5.2f \qquad}}\\\\ \n \n"%(
                Person.depos_2015, Person.final_2015 - Person.depos_2015, Person.final_2015))


        f.write('\end{document}')





