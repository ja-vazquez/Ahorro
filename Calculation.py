import os
import pylab
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import gridspec
from collections import OrderedDict

class Settings:
    def __init__(self, _person, _today_date):
        self.person      = _person
        self.today_date  = _today_date
        self.today_day   = int(self.today_date.strftime('%d'))
        self.today_imon  = int(self.today_date.strftime('%m'))
        self.today_year  = int(self.today_date.strftime('%Y'))
        self.today_month = self.today_date.strftime("%b")
        self.month_name  = self.traslation(self.today_month)

	self.retiro	 = 0.0025        
        self.directory   = 'Ahorro/Investors/'
        self.bursa_dir   = 'Investing/Bursanet/'
        self.bursa_info  = 'Investing.txt'
        self.bursa_2015  = 'Investing/2015/Investing_2015.txt'
	self.bursa_2016  = 'Investing/2016/Investing_2016.txt'
	self.invest_info = 'Investors_info.txt'
        self.finances    = 'Ahorro/Finances.csv'
        self.depos_file  = self.person + '/' + self.person + '_Res_depos.txt'
        self.dir_month   = self.directory + self.person + '/' + self.today_month + '/'
        self.file_month  = self.person + '_' + self.today_month 
        if not os.path.isdir(self.dir_month): os.system('mkdir {}'.format(self.dir_month))
       
        self.invest_name = 'Investing.pdf'
        self.plot_name   = 'Plots_{}.pdf'.format(self.file_month)
        self.edo_name    = 'Edo_{}.csv'.format(self.file_month)
        self.file_finan  = 'Finances_{}.pdf'.format(self.file_month)
             
            
        
    def traslation(self, month):
        mspanish = {'Jan':'Enero', 'Feb':'Febrero',
                 'Mar':'Marzo', 'Apr':'Abril', 'May':'Mayo',
                 'Jun':'Junio', 'Jul':'Julio', 'Aug':'Agosto',
                 'Sep':'Septiembre', 'Oct':'Octubre', 'Nov':'Noviembre',
                 'Dec':'Diciembre'}
        return mspanish[month]
        
        

        
class Read_files:
    def __init__(self, Setts):
        self.Setts = Setts
        
        
    def all_persons(self):
        df = pd.read_csv(self.Setts.directory + self.Setts.invest_info, sep='&', 
                    names =['names','full_name','email','member_since',
                            'perct','depos_2016','final_2016'],
                    comment='#', index_col='names')
        return df
        
        
    def person_info(self):
        return self.all_persons().loc['{}'.format(self.Setts.person)]
        
                      
    def person_depos(self):
        depositos = pd.read_csv(self.Setts.directory + self.Setts.depos_file, sep='\s+') 
        depositos['Date_py'] = pd.to_datetime(depositos.Date, format='%d/%b/%Y')
	depositos['Dates']   = depositos.Date.map(lambda x: x[:-5]) #x.rstrip('/2017') 
	depositos['Months']  = depositos.Dates.map(lambda x: x[3:])
	return depositos
        
         
    def read_bursa(self, files):
        pd_bursa = pd.read_csv(files, 
                               names = ['dates', 'fees', 'money_in', 'total'],
                               skiprows = 4, sep='\s+', index_col = 'dates', parse_dates=True)
        return pd_bursa

        
        
class Calculation:
    def __init__(self, person, today_date):
        self._person      = person
        self._today_date  = today_date
        
        self.Setts        = Settings(self._person, self._today_date)
        self.Rfiles       = Read_files(self.Setts)
        
        self.df_deposits  = self.Rfiles.person_depos()
        self.Person_info  = self.Rfiles.person_info()
        
        self.person_perct = eval(self.Person_info.perct)
        self.person_d2016 = self.Person_info.depos_2016
        self.person_f2016 = self.Person_info.final_2016

	self.total_months = list(OrderedDict.fromkeys(self.df_deposits.Months.tolist()))
        #self.total_months= self.Person_info.init_month.split(',')
        #self.total_months.append(self.Setts.today_month)
        
        self.len_months   = len(self.total_months)
        self.len_dates    = len(self.df_deposits)
        

        
    def interests(self):
        """Consider the # of days for each deposit and attach the corresponding percentage """

        Dates     = self.df_deposits['Date']
        Depositos = self.df_deposits['Deposito']
        Date_py   = self.df_deposits['Date_py']
        
	self.df_deposits['total_days']      = (self._today_date - Date_py).astype('timedelta64[D]')
        self.df_deposits['frac_interest']   = self.df_deposits.total_days *self.person_perct
        self.df_deposits['tot_interest']    = (Depositos *self.df_deposits.frac_interest +  
							self.df_deposits['Inter_past'])
       
        self.df_deposits['total']           = Depositos + self.df_deposits.tot_interest

        #group by month
        group_monthly   = self.df_deposits.groupby([Date_py.dt.month]).sum()
        num_depos_month = self.df_deposits.groupby([Date_py.dt.month]).size()
        group_monthly['num_deposits']      = num_depos_month.to_frame(name='num_months')

        self.group_monthly                 = group_monthly.set_index([self.total_months])
        self.group_monthly['cum_depos']    = self.group_monthly.Deposito.cumsum()
        self.group_monthly['cum_interest'] = self.group_monthly.tot_interest.cumsum()
        self.group_monthly['cum_total']    = self.group_monthly.total.cumsum()


        
        self.group_monthly['plot_interest']= [i+1 for i in range(self.len_months)[::-1]]
        self.group_monthly['plot_interest']= self.group_monthly.cum_interest/self.group_monthly.plot_interest

        self.group_monthly.index.name      = 'Months'
        self.df_deposits                   = self.df_deposits.set_index('Dates', drop=False)

        self.group_monthly.to_csv(self.Setts.dir_month + self.Setts.edo_name)
       
        #print self.group_monthly
        #print self.group_monthly.head() #.loc['Jan']['Deposits'])
        #print self.df_deposits.head()


        
        
class Plotting():
    def __init__(self, Calcul):
        self.Calcul = Calcul
        
        params1 = {'backend': 'pdf',
               'axes.labelsize': 15, 'text.fontsize': 18,
               'xtick.labelsize': 18, 'ytick.labelsize': 18,
               'legend.fontsize': 18, 'lines.markersize': 16,
               'font.size': 16,}
        pylab.rcParams.update(params1)
        pd.set_option('display.mpl_style', 'default')
        
        
        
    def _make_plot(self, ax, df, ylims, color='LimeGreen', label=None,
              ylabel=None, xlabel='Fecha', title="title"):

        df.plot.bar(color=color, label=label,
                stacked=True, alpha=0.8, ax=ax)

	if label: plt.legend(loc='best', frameon=True)
	if ylabel: ax.set_ylabel(ylabel, size=20)
	plt.ylim(ymax=  ylims)
	ax.set_title(title)
        ax.set_xlabel(xlabel, size=18)

        
        
    def deposits_plot(self):
        Deposits= self.Calcul.df_deposits.Deposito

        plt.figure(figsize = (18, 10))
	if self.Calcul.df_deposits.index.tolist()[0] == '01/Jan':	
	    gs  = gridspec.GridSpec(1, 3, width_ratios= [0.8, 3, 2.5])
	   
            ax1= plt.subplot(gs[0])
	    self._make_plot(ax1, Deposits[:1], 
		ylims  = self.Calcul.group_monthly.cum_depos.max()*1.3,
                title  = '%i'%(int(self.Calcul.Setts.today_year) - 1),
		color  = 'gold',
                ylabel = 'Depositos (MXN)')
            plt.axhline(y=0, color='k')

            ax2= plt.subplot(gs[1])
	    self._make_plot(ax2, Deposits[1:], ylims=Deposits[1:].max()*1.2,
          	title  = '%i'%int(self.Calcul.Setts.today_year),
          	label  = 'Depositado = $%5.2f'%(Deposits.sum()))
            plt.axhline(y=0, color='k')
                
            ax3= plt.subplot(gs[2])
            self._make_plot(ax3, self.Calcul.group_monthly[['cum_depos','cum_interest']],
          	ylims   = self.Calcul.group_monthly.cum_depos.max()*1.3, 
          	color=['blue','Magenta'],
          	title  = 'Total acumulado',
          	ylabel = 'Total (MXN)', xlabel = 'Meses')
        
        L= plt.legend()
        L.get_texts()[0].set_text('Depositos')
        L.get_texts()[1].set_text('Total =  $%5.2f'%(self.Calcul.group_monthly.cum_total[-1]))

        plt.subplots_adjust(wspace=0.4)
        pylab.savefig(self.Calcul.Setts.dir_month + self.Calcul.Setts.plot_name)
   
        #plt.show(block=True)
        

   
class Run_all(Calculation):
    def __init__(self, person, today_date):
        Calculation.__init__(self, person, today_date)
        
        
    def all_result(self):
        names = self.Rfiles.all_persons().index.values
        dt = []
        for name in names:
            Calcul = Calculation(name, self._today_date)
            Calcul.interests()
            dt.append(Calcul.group_monthly[-1:])
        
        all_invest          = pd.concat(dt)
        all_invest['names'] = names
        all_invest.index    = all_invest.names
	
        total_invest     = all_invest[['cum_total']].sum() 
	total_depos      = all_invest[['cum_depos']].sum()
	total_interests  = all_invest[['cum_interest']].sum()
	print '**', all_invest['cum_depos'].tolist()
        file_bursa                     = self.Setts.bursa_dir + self.Setts.bursa_info
        total_invest.set_value('bursa', self.Rfiles.read_bursa(file_bursa)['total'].iloc[-1])
        total_invest['gain_investors'] = total_invest.bursa -  total_invest.cum_total
        total_invest['gain_mine']      = all_invest.loc['Yo'].cum_interest

	inv_depos        = all_invest.drop('Yo')[['cum_depos']].sum()
	inv_interests    = all_invest.drop('Yo')[['cum_interest']].sum()
        inv_total	 = all_invest.drop('Yo')[['cum_total']].sum()

        my_invest        = all_invest.ix['Yo'].cum_total
        my_depos         = all_invest.ix['Yo'].cum_depos
        my_interests     = all_invest.ix['Yo'].cum_interest
 
        total_gain       = total_invest.bursa -  total_invest.cum_total + my_invest
        
        
        
        params1 = {'backend': 'pdf',
               'axes.labelsize': 15, 'text.fontsize': 16,
               'xtick.labelsize': 15, 'ytick.labelsize': 15,
               'legend.fontsize': 15, 'lines.markersize': 16,
               'font.size': 15,}
        pylab.rcParams.update(params1)
        pd.set_option('display.mpl_style', 'default')
        
        
        plt.figure(figsize = (15, 8))
        gs  = gridspec.GridSpec(1, 3, width_ratios= [3, 3, 3])
        
        ax1= plt.subplot(gs[0])
        all_invest.cum_depos.plot(kind = 'bar', ax=ax1, color='orange', 
			label='Total: %.1f \n Investors: %.1f \n Mine: %.1f'%(
				total_depos, inv_depos, my_depos))
	plt.ylim(ymax =  all_invest.cum_depos.max()*1.3)		
        plt.title('Deposits')
        plt.legend(loc='best')
        
        
        ax2= plt.subplot(gs[1])
        all_invest.cum_interest.plot(kind = 'bar', ax=ax2, color='g',
			label='Total: %.1f \n Investors: %.1f \n Mine: %.1f'%(
			    total_interests, inv_interests, my_interests))
	plt.ylim(ymax = all_invest.cum_interest.max()*1.3)
	plt.title('Interests')
        plt.legend(loc='best')
        
        
        ax3=plt.subplot(gs[2])
        pd.DataFrame(total_invest[['gain_investors','gain_mine']]).T.plot.bar(stacked=True, 
                    ax=ax3)
        plt.title('Gains')
        plt.legend(['People: %.1f, %.1f%%'%(total_invest.gain_investors, 
                             total_invest.gain_investors/my_depos*100.), 
                    'Mine: %.1f,   %.1f%%'%(total_invest.gain_mine, 
                             total_invest.gain_mine/my_depos*100.)],
                   loc='best')
	ax3.text(0.15,6000, 'Bursa: %.1f \n Investors: %.1f'%(
			total_invest.bursa , inv_total), fontsize=14)
        ax3.text(0.15,3000, 'Mine_avail: %.1f \n Mine_gain: %.1f'%(total_gain , 
                           total_invest.gain_investors+total_invest.gain_mine), fontsize=14)
       
        plt.savefig('People.pdf')
        os.system("open -a Preview People.pdf")
        #plt.show(block=True)
        

        
class Finances(Calculation):
    def __init__(self, _person, _today_date):
        Calculation.__init__(self, _person, _today_date)
        
    
    def my_finances(self):
        pd.set_option('display.mpl_style', 'default')
        finan = pd.read_csv(self.Setts.finances, sep='\s+', comment='#')
        
        finan['total'] = finan.sum(axis=1)
        finan2         = finan.set_index(['date'])

        instruments    = finan.set_index(['date']).T
        finan2['bursa_mine'] = finan2['bursanet'] + finan2['investors']
        
        fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, figsize=(10, 12))
        
        finan2[['bursa_mine', 'etoro', 'tfcu-deb', 'bnx-deb', 'chase-deb', 'bbva', 'santa-deb', 'cash']].plot(
                kind='bar', ax= ax1, stacked=True)         
        finan2[['tfcu-cred', 'bnx-cred', 'amz-cred', 'santa-cred', 'debts']].plot(
                kind='bar', ax= ax2, stacked=True)
        instruments.ix['total'].plot(kind='bar', ax= ax3)
        
        ax1.set_title('Amount I have: %s'%(instruments.ix['total'][-1]))
        fig.subplots_adjust(hspace=0.1)
        
        #my_file = self.Setts.directory + self.Setts.file_month + self.Setts.file_finan
        
        plt.savefig('Finances.pdf')
        os.system('open -a Preview Finances.pdf')
        
        #plt.show(block=True)
        
        
        
        
        
