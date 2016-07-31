

from People import *
import numpy as np
import pandas as pd
from datetime import date

class Calculation:
    def __init__(self, Person, months, df_deposits):
        self.Person       = Person
        self.months       = months
        self.df_deposits  = df_deposits
        self.total_months = self.Person.init_month + self.months


    def calcu_interest(self, today_date):
        """Consider the # of days for each deposit and attach the corresponding percentage """
        self.today_date   = today_date
        self.len_months  = len(self.total_months)
        self.len_dates   = len(self.df_deposits)

        self.df_deposits['Date_py']       = pd.to_datetime(self.df_deposits['Dates'], format='%d/%b/%Y')
        self.df_deposits['total_days']    = (today_date - self.df_deposits['Date_py']).astype('timedelta64[D]')
        self.df_deposits['frac_interest'] = self.df_deposits['total_days']*self.Person.perct
        self.df_deposits['tot_interest']  = self.df_deposits['Deposits'] *self.df_deposits['frac_interest']
        self.df_deposits['cum_depos']     = self.df_deposits['Deposits'].cumsum()
        self.df_deposits['cum_interest']  = self.df_deposits['tot_interest'].cumsum()


        #print  self.df_deposits



