
import os, sys
import datetime
import pandas as pd
import matplotlib.pylab as plt
from matplotlib import gridspec

month = 'Sep'
dt =[]
df = pd.read_csv('inv_names.csv',names=['names'])
inv_names = df['names'].tolist()

today_date  = datetime.date.today()
today_day   = str(today_date.strftime('%d'))

#bursa = 93522.7
bursa =float( input("Bursanet total: "))


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
avail = ser['bursa'] - result[['cum_total']].iloc[0:-1].sum()

commd = """ mkdir Investors/Yo/%s"""%(month)
os.system(commd)

ser.to_csv('Investors/Yo/'+month+'/Final_Yo_'+ month+'.csv')


if True:
 fig = plt.figure(figsize = (10, 6))
 gs  = gridspec.GridSpec(1, 2, width_ratios= [3, 2.5])

 ax1= plt.subplot(gs[0])
 result[['cum_depos', 'cum_total']].plot(kind = 'bar', ax=ax1)
 plt.title('Available: %.2f'%(avail))
 #print (result)

 ax2= plt.subplot(gs[1])
 ser.plot(kind = 'bar', ax=ax2, label = 'Bursa: %.2f \n Total: %.2f'%(ser['bursa'], ser['cum_total']))
 plt.legend(loc='lower center')
 plt.title('Total = %.2f'%(ser['bursa'] - ser['cum_total']))
 plt.savefig('Investors/Yo/'+month+'/Final_Yo_' + month + '_' + today_day + '.pdf')
 #plt.show()
 
 commd = 'Investors/Yo/'+month+'/Final_Yo_' + month + '_' + today_day + '.pdf'
 os.system("open -a Preview %s"%(commd))
