
import os, sys
import datetime
import pandas as pd
import matplotlib.pylab as plt
from matplotlib import gridspec

month = 'Oct'
dt =[]
df = pd.read_csv('inv_names.csv',names=['names'])
inv_names = df['names'].tolist()

today_date  = datetime.date.today()
today_day   = str(today_date.strftime('%d'))

dir = '/Users/josevazquezgonzalez/Desktop/TODOs/Finances/Investing/Bursanet/'
pd_bursa = pd.read_csv(dir + 'Investing.txt', skiprows=4, sep='\s+',
                       names=['dates', 'fees', 'money_in', 'total'])

bursa = pd_bursa['total'].iloc[-1]

for inv in inv_names:
    direc = 'Investors/{}/{}/'.format(inv, month)
    fname = 'Edo_{}_{}.csv'.format(inv, month)
    df = pd.read_csv(direc + fname)
    dt.append(df.iloc[-1:])

result = pd.concat(dt)
result['names'] = inv_names
result.index =  result['names']


ser = result[['cum_total']].sum()
ser.set_value('bursa', bursa)
print(ser)
avail = ser['bursa'] - result[['cum_total']].iloc[0:-1].sum()

commd = """ mkdir Investors/Yo/%s"""%(month)
os.system(commd)

ser.to_csv('Investors/Yo/'+month+'/Final_Yo_'+ month+'.csv')

result['tot_perc'] =  result[['cum_total']]/result[['cum_total']].sum()*100

if True:
 fig = plt.figure(figsize = (15, 6))
 gs  = gridspec.GridSpec(1, 3, width_ratios= [2, 2, 3])

 ax1= plt.subplot(gs[0])
 result['cum_total'].plot(kind = 'bar', ax=ax1, color='orange')
 plt.title('Investors: %.1f,  Avail: %.1f'%(result[['cum_total']].sum(), avail))


 ax3= plt.subplot(gs[1])
 result['cum_interest'].plot(kind = 'bar', ax=ax3, color='g')
 plt.title('Interests')

 ax2= plt.subplot(gs[2])
 ser['investors'] = ser['bursa']-ser['cum_total']
 ser['interests'] = result.ix['Yo']['cum_interest']
 ser[['investors', 'interests']].plot(kind = 'barh', ax=ax2, label = 'Yo:            %.1f :  %.2f %% \n Investors: %.1f :   %.2f %%'
                            %(result.ix['Yo']['cum_interest'], result.ix['Yo']['cum_interest']/result.ix['Yo']['cum_depos']*100,
                              ser['bursa']- ser['cum_total'], (ser['bursa'] - ser['cum_total'])/result[['cum_depos']].sum()*100))
 plt.legend(loc='upper right')
 ax2.axvline(0, color='b', linestyle='-')
 plt.legend(frameon=False)
 plt.title('Bursa:  %.1f, Total = %.1f'%(ser['bursa'], ser['bursa']- ser['cum_total'] + result.ix['Yo']['cum_interest']))
 plt.savefig('Investors/Yo/'+month+'/Final_Yo_' + month + '_' + today_day + '.pdf')
 #plt.show()
 
 commd = 'Investors/Yo/'+month+'/Final_Yo_' + month + '_' + today_day + '.pdf'
 os.system("open -a Preview %s"%(commd))
