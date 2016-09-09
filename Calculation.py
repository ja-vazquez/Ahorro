


import pandas as pd
import numpy as np

class Calculation:
    def __init__(self, Person, months, df_deposits):
        self.Person       = Person
        self.months       = months
        self.df_deposits  = df_deposits
        self.total_months = self.Person.init_month + self.months

        self.len_months  = len(self.total_months)
        self.len_dates   = len(self.df_deposits)


    def calcu_interest(self, today_date):
        """Consider the # of days for each deposit and attach the corresponding percentage """
        self.today_date  = today_date


        self.df_deposits['Date_py']         = pd.to_datetime(self.df_deposits['Dates'], format='%d/%b/%Y')
        self.df_deposits['total_days']      = (today_date - self.df_deposits['Date_py']).astype('timedelta64[D]')
        self.df_deposits['frac_interest']   = self.df_deposits['total_days']*self.Person.perct
        self.df_deposits['tot_interest']    = self.df_deposits['Deposits']  *self.df_deposits['frac_interest']

            #for claims
        #self.df_deposits['tot_interest'][self.df_deposits['Deposits'] < 0] = 0
        #self.df_retiros = self.df_deposits[self.df_deposits['Deposits'] < 0].copy()

        self.df_deposits['total']           = self.df_deposits['Deposits'] + self.df_deposits['tot_interest']
        self.df_deposits['Dates']           = self.df_deposits['Dates'].map(lambda x: x.rstrip('/2016'))


        #group by month
        group_monthly   = self.df_deposits.groupby([self.df_deposits['Date_py'].dt.month]).sum()
        num_depos_month = self.df_deposits.groupby([self.df_deposits['Date_py'].dt.month]).size()

        group_monthly['num_deposits']      = num_depos_month.to_frame(name='num_months')

        self.group_monthly                 = group_monthly.set_index([self.total_months])
        self.group_monthly['cum_depos']    = self.group_monthly['Deposits'].cumsum()
        self.group_monthly['cum_interest'] = self.group_monthly['tot_interest'].cumsum()
        self.group_monthly['cum_total']    = self.group_monthly['total'].cumsum()

        tmonths = len(self.group_monthly)
        self.group_monthly['plot_interest']= [i+1 for i in np.arange(tmonths)[::-1]]
        self.group_monthly['plot_interest']= self.group_monthly['cum_interest']/self.group_monthly['plot_interest']

        self.group_monthly.index.name      = 'Months'


        print (self.group_monthly) #.loc['Jan']['Deposits'])
        #print self.df_deposits
