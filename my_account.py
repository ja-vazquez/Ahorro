
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


if True:
 fig = plt.figure(figsize = (10, 6))
 gs  = gridspec.GridSpec(1, 2, width_ratios= [3, 2.5])

 ax1= plt.subplot(gs[0])
 result[['cum_depos', 'cum_total']].plot(kind = 'bar', ax=ax1)
 plt.title('Investors: %.1f,  Avail: %.1f'%(result[['cum_total']].sum(), avail))
 #print (result)

 ax2= plt.subplot(gs[1])
 ser['investors']= ser['bursa']-ser['cum_total']
 ser['interests']= result.ix['Yo']['cum_interest']
 ser[['investors', 'interests']].plot(kind = 'bar', ax=ax2, label = 'Bursa: %.1f \n Yo:            %.1f :  %.2f %% \n Investors: %.1f :   %.2f %%'
                            %(ser['bursa'], result.ix['Yo']['cum_interest'], result.ix['Yo']['cum_interest']/result.ix['Yo']['cum_depos']*100,
		              ser['bursa']- ser['cum_total'], (ser['bursa'] - ser['cum_total'])/result[['cum_depos']].sum()*100)) 
 plt.legend(loc='best')
 plt.title('Total = %.1f'%(ser['bursa']- ser['cum_total'] + result.ix['Yo']['cum_interest']))
 plt.savefig('Investors/Yo/'+month+'/Final_Yo_' + month + '_' + today_day + '.pdf')
 #plt.show()
 
 commd = 'Investors/Yo/'+month+'/Final_Yo_' + month + '_' + today_day + '.pdf'
 os.system("open -a Preview %s"%(commd))
