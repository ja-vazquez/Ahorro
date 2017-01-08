
import os
import datetime 
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from Calculation import Calculation 
from matplotlib.dates import DateFormatter, WeekdayLocator, \
     MONDAY, MonthLocator

class Invest(Calculation):
    def __init__(self, person, today_date, invest):
        Calculation.__init__(self, person, today_date, invest)
    
        
    def investing(self):
        file_bursa = self.Setts.bursa_dir + self.Setts.bursa_info
        df_invest  = self.Rfiles.read_bursa(file_bursa)

        df_invest['gains']     = df_invest.total - df_invest.money_in
        df_invest['perc']      = ((df_invest.total / df_invest.money_in) - 1.0) * 100.
        df_invest['day_depos'] = [df_invest.money_in.values[i] - df_invest.money_in.values[i-1 if i!=0 else 0]
                                  for i,_ in enumerate(df_invest.index)]
        df_invest['day_gain']  = [(df_invest.total.values[i] - df_invest.total.values[i-1 if i!=0 else 0]) 
                                  for i,_ in enumerate(df_invest.index)] - df_invest.day_depos
        df_invest['day_perc']  = df_invest.day_gain / df_invest.money_in * 100.
    
        df_monthly   = df_invest.groupby([df_invest.index.month]).sum()
        total_months = [datetime.date(self.Setts.today_year, i % 12 + 1, 01) for i,_ in enumerate(df_monthly.index)] 
        df_monthly   = df_monthly.set_index([total_months])
            
        last_total = df_invest.total.values[-1]
        last_depos = df_invest.money_in.values[-1]
        last_perc  = df_invest['perc'].values[-1]    


        fig = plt.figure(figsize=(17, 10))
        
        ax1 = plt.subplot(2, 2, 1)       
        ax1.bar(df_invest.index, df_invest.gains, width=1.3, color='b', alpha=0.7,
                label='Earning_total: {0:,g} '.format(last_total - last_depos))
        plt.legend(loc='upper left')
        ax11 = ax1.twinx()
        ax11.plot(df_invest.index, df_invest.gains, color='b')
        self.anotatep(ax11, "Invertido: {0:,g}".format(last_depos), (0.9, 0.31))
        self.anotatep(ax11, "Total: {0:,g}".format(last_total), (0.9, 0.2))
        ax1.set_title('Total Earnings')
        plt.axhline(y=0, linewidth=2)
        self.plot_feat(ax1)
        
        ax2 = plt.subplot(2, 2, 2)
        df_invest.perc.plot(ax= ax2)
        plt.axhline(y=0, linewidth=2)
        ax2.set_title('Percentage')
        self.plot_feat(ax2)
        
        ax3 = plt.subplot(2, 2, 3)
        gain_tmp = df_invest.day_gain 
        ax3.bar(df_invest[gain_tmp < 0].index, df_invest[gain_tmp < 0].day_gain, width=2, color='r')
        ax3.bar(df_invest[gain_tmp > 0].index, df_invest[gain_tmp > 0].day_gain, width=2, color='g')
        ax3.bar(df_monthly.index, df_monthly.day_gain, width=30, color='y', alpha=0.2, 
                label='Earning_year: {0:,g} '.format(gain_tmp.sum()))
        ax3.bar(df_monthly.index, df_invest.groupby([df_invest.index.month]).tail(1).money_in*self.person_perct*365/12., 
                width=30, color='cyan', alpha=0.2)
        ax3.set_title('Daily Earnings')
        plt.axhline(y=0, linewidth=2)
        plt.legend(loc='upper left')
        fig.autofmt_xdate()
        self.plot_feat(ax3)
        fig.tight_layout()

        ax4 = plt.subplot(2, 2, 4)
        ax4.bar(df_invest[gain_tmp > 0].index, df_invest[df_invest.day_perc > 0].day_perc, width=2, 
                color='g', label='Total: %2.1f %% ' % (last_perc))
        ax4.bar(df_invest[gain_tmp < 0].index, df_invest[df_invest.day_perc < 0].day_perc, width=2, 
                color='r', label='Monthly: %2.1f %% ' % (last_perc / len(df_monthly)))
        ax4.bar(df_monthly.index, df_monthly.day_perc, width=30, color='y', alpha=0.2)
        ax4.bar(df_monthly.index, [self.person_perct*365*100/12. for _ in df_monthly.index], 
                width=30, color='cyan', alpha=0.2)
        ax4.set_title('Daily Percentage')
        plt.axhline(y=0, linewidth=2)
        plt.legend(loc='upper left')
        fig.autofmt_xdate()
        self.plot_feat(ax4)
        fig.tight_layout()
        
        plt.savefig(self.Setts.file_invest)
        os.system("open -a Preview {}".format(self.Setts.file_invest))  
        #plt.show(block=True)
        
        
        
        
    def extra_month(self):
        extra_month = self.Setts.today_imon  + 1
        extra_year  = self.Setts.today_year
        extra_day   = 28
         
        if self.Setts.today_imon == 12:
            extra_month = 01
            extra_year  = self.Setts.today_year + 1    
        return datetime.date(extra_year, extra_month, extra_day)
         
    
        
    def anotatep(self, ax, text, xy, color='gold'):
        ax.annotate(text, xy=xy, xycoords='axes fraction', fontsize=18, 
                    horizontalalignment='right', bbox={'alpha': 0.4, 'pad': 10, 
                    'facecolor': color}, verticalalignment='bottom')

        
    def plot_feat(self, ax):
        mondays        = WeekdayLocator(MONDAY)
        #alldays       = DayLocator()
        #weekFormatter = DateFormatter('%b %d')
        #dayFormatter  = DateFormatter('%d')
        months         = MonthLocator(range(1, 13), bymonthday=1, interval=1)
        monthsFmt      = DateFormatter("%d '%b")

        ax.xaxis.set_major_locator(mondays)
        #ax.xaxis.set_minor_locator(alldays)
        #ax.xaxis.set_major_formatter(weekFormatter)
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(monthsFmt)
        ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
        ax.yaxis.grid(True, 'major', color='g', linestyle='-', alpha=0.8)
        ax.xaxis.grid(True, 'major', color='g', linestyle='-', alpha=0.8)
        ax.xaxis.grid(True, 'minor')
        ax.yaxis.grid(True, 'minor')
        ax.grid(True)
        plt.xlim(datetime.date(self.Setts.today_year, 01, 01), self.extra_month())
        plt.xlabel('Time [Month/day]')
        
        
        
class Performance(Calculation):
    def __init__(self, person, today_date, invest):
        Calculation.__init__(self, person, today_date, invest)
        self._invest = invest

        
    def perform(self):
        file_bursa = self.Setts.bursa_dir + self.Setts.bursa_info
        df_2017    = self.Rfiles.read_bursa(file_bursa)

        if self._invest == 'bursa':
            file_2015  = self.Setts.bursa_2015
            file_2016  = self.Setts.bursa_2016
            df_2015    = self.Rfiles.read_bursa(file_2015)
            df_2016    = self.Rfiles.read_bursa(file_2016)
        
            end_year_2015  = df_2015.total[-1] - df_2015.money_in[-1]
            end_year_2016  = df_2016.total[-1] - df_2016.money_in[-1]

            df_2016['money_in'] = df_2016.money_in - end_year_2015
            df_2017['money_in'] = df_2017.money_in - end_year_2016 - end_year_2015

            result = pd.concat([df_2015, df_2016, df_2017])
        else:
            result = df_2017

            
        result['earn'] = result.total - result.money_in
        result['perc'] = result.earn/result.money_in*100
        rolmean  = pd.rolling_mean(result.earn, window=25)
        avg_rate = (self.earn_rate(rolmean, -1) + self.earn_rate(rolmean, -2))/2.


        fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, figsize=(14, 10))
        
        result['earn'].plot(ax= ax1, color= 'c', label= 'Earn')
        rolmean.plot(ax= ax1, color= 'y', label= 'Avg')
        ax1.set_title('Deposits: %s,  total: %s, earn: %s, Percentage: %.1f %%, rate: %.1f p/month'%(
                    result.money_in[-1], result.total[-1],  result.earn[-1], result.perc[-1], avg_rate))
        ax1.set_ylim(ymin= 0)
        ax1.axhline(end_year_2015, color= 'gray', linestyle= '--')
        ax1.axhline(end_year_2015 + end_year_2016, color= 'gray', linestyle= '--')

        
        result['perc'].plot(ax= ax2, ylim= (0, 40), label='Percentage')
        ax2.axhline(15, color= 'gray', linestyle= '--')
        
        
        result['total'].plot(ax=ax3, color='g', label='Total')
        result['money_in'].plot(ax=ax3, color='orange', label='Money in')
        
        fig.subplots_adjust(hspace=0)
        for i, l in zip((ax1,ax2,ax3),('earn', 'perc', 'total')):  self.bplot(i, l, result)
        
        plt.savefig(self.Setts.file_perform)
        os.system("open -a Preview {}".format(self.Setts.file_perform))
        #plt.show(block=True)
        

        
    def bplot(self, ax, label, result):
        ax.grid(True)
        ax.legend(loc ='lower right')
        ax.axvline(pd.to_datetime('2016-01-01'), color='gray', linestyle='--')
        ax.axvline(pd.to_datetime('2017-01-01'), color='gray', linestyle='--')
        ax.axhline(result[label][-1], color='r', linestyle='--')
        
        
        
    def earn_rate(self, rolmean, idx):
        return (rolmean.groupby([rolmean.index.month]).tail(1).values[idx] -
                rolmean.groupby([rolmean.index.month]).tail(1).values[idx-2])/2.
                          
                          
                          
                          
                          
        
