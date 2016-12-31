import os

class Latex:
    def __init__(self, Calcul):
        self.Calcul = Calcul
        self.Setts  = self.Calcul.Setts
        
    def make_latex(self):
	this_year = self.Setts.today_year
        #Latex has some problems with .format style
        with open('{0}Edo_{1}.tex'.format(self.Calcul.Setts.dir_month,
                                           self.Calcul.Setts.file_month), 'w') as f:
            Latex_text_1 = r"""
\documentclass[10pt,secnumarabic,nofootinbib,preprintnumbers,amsmath,amssymb,aps]{revtex4}
\usepackage[usenames]{color}
\usepackage{footnote}
\usepackage{graphicx}
\usepackage{ulem}
\usepackage{hyperref}

\frenchspacing
\def\\red{\\textcolor{red}}
\def\\blue{\\textcolor{blue}}
\begin{document}
            """
            f.write(Latex_text_1 + '\n')
            f.write('\\title{ESTADO DE CUENTA: %s.%s}\n'%(
                    self.Setts.month_name, this_year))
            f.write('\\author{%s}\n'%(self.Calcul.Person_info.full_name))
            f.write('\\email[\hfill]{%s}\n'%(self.Calcul.Person_info.email))
    
            
            print self.Setts.today_day, self.Setts.month_name, self.Setts.today_year
            Latex_text_2 = """
%%\date{\\today}\n
\maketitle\n
Estado de cuenta correspondiente hasta  el %s-%s del %s, considerando una
tasa de inter\\'es del %.1f\%% anual y un cargo del %.2f\%% del monto total a retirar. 
\\footnote{Esto es, por cada \$1000.0 MXN a retirar se har\\'a un cargo de \$%.1f MXN.}\n
        """%(self.Setts.today_day, self.Setts.month_name, this_year,
             self.Calcul.person_perct*100*365, self.Calcul.Setts.retiro*100,
	     self.Calcul.Setts.retiro*1000)
            f.write(Latex_text_2 + '\n\n')
         
            

            Latex_text_3 = """
\\begin{savenotes}
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


            #past deposits <-
            if self.Calcul.len_months > 1:
                Latex_text_4 = """
$\leftarrow$ %s/%s  \qquad \qquad & \$%.2f MXN     & \qquad \qquad  \$%.2f MXN & \qquad \qquad   \$%.2f MXN   \\\\
                """%(this_year,
		     self.Setts.today_month, 
                     self.Calcul.group_monthly.cum_depos[-2],
                     self.Calcul.group_monthly.cum_interest[-2], 
                     self.Calcul.group_monthly.cum_total[-2]) 
                f.write(Latex_text_4 + '\n\n')



            #current deposits
            num_depos = self.Calcul.group_monthly.num_deposits[-1]  
            for n in range(num_depos, 0, -1):
                date_deposits = self.Calcul.df_deposits.iloc[-n].Dates       
                deposits      = self.Calcul.df_deposits.iloc[-n].Deposito     
                interest      = self.Calcul.df_deposits.iloc[-n].tot_interest 
                total         = self.Calcul.df_deposits.iloc[-n].total        
                
                Latex_text_5 = """
%s/%s'  \qquad  \qquad  & \$%.2f MXN   & \qquad \qquad  \$%.2f MXN & \qquad \qquad   \$%.2f MXN      \\\\
                """%(date_deposits, this_year, deposits, interest, total)
                f.write(Latex_text_5 + '\n\n')



            Latex_text_6 = """
\hline
-                       \qquad  \qquad  &- & \qquad \qquad - & \qquad \qquad    \color{blue}{= \$ \\bf %.2f MXN}
			\\footnote{Monto disponible para retirar: \$ %.2f MXN} \\\\
        """%(self.Calcul.group_monthly.cum_total[-1], self.Calcul.group_monthly.cum_total[-1]*(1- self.Calcul.Setts.retiro))
            f.write(Latex_text_6 + '\n\n')


            Latex_text_7 = """
\hline
\hline
\end{tabular}
\label{tab:omega}
\end{center}
\end{table}
\end{savenotes}


\\begin{figure}[h!]
\\begin{center}
\\includegraphics[trim = 1mm -2mm 1mm 1mm, clip, width=18cm, height=9cm]{Plots_%s.pdf}

\caption{Izquierda: dep\\'ositos realizados hasta %s-%s.
Derecha: monto total acumulado en la cuenta hasta  el %s-%s-%s.}
\label{fig:alpha}
\end{center}
\end{figure}

            """%(self.Setts.file_month, 
		self.Setts.month_name, this_year, 
		self.Setts.today_day, self.Setts.month_name, this_year)
            f.write(Latex_text_7 +'\n')
            
            

            f.write("\centering {Anual   \qquad \qquad Deposito \qquad \qquad Inter\\'es acumulado \qquad  \qquad Total \qquad \qquad \hspace{2cm}}\\\\  \n")
            f.write("\centering {%s: \qquad  \\fbox{\qquad   \$ %5.2f \qquad  ,\qquad   \$ %5.2f \qquad ,\qquad    \$ %5.2f \qquad}}\\\\ "%(
		    this_year,
                    self.Calcul.group_monthly.cum_depos[-1], 
                    self.Calcul.group_monthly.cum_interest[-1],
                    self.Calcul.group_monthly.cum_total[-1]))  
                    


            if self.Calcul.Person_info.depos_2016 != 0:
                f.write("\centering {2016: \qquad  \\fbox{\qquad   \$ %5.2f \qquad  ,\qquad   \$ %5.2f \qquad ,\qquad    \$ %5.2f \qquad}}\\\\ \n \n"%(
                        self.Calcul.person_d2016, 
                        self.Calcul.person_f2016 - self.Calcul.person_d2016,
                        self.Calcul.person_f2016))

	    f.write(". \\newline . \hfill JA V\\'azquez")
            f.write('\end{document}')

  
            
    def show_pdf(self):
        command = """
        cd {0}
        pdflatex Edo_{1}.tex
        open -a Preview Edo_{1}.pdf
        rm *aux *log *out
        """.format(self.Calcul.Setts.dir_month, self.Calcul.Setts.file_month)
        os.system(command)

