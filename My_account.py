

import pandas as pd
import matplotlib.pylab as plt
from matplotlib import gridspec

month = 'Jul'
inv_names = [] 
dt =[]

bursa = 79206.4

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

if True:
 fig = plt.figure(figsize = (10, 6))
 gs  = gridspec.GridSpec(1, 2, width_ratios= [3, 2.5])

 ax1= plt.subplot(gs[0])
 result[['cum_depos', 'cum_total']].plot(kind = 'bar', ax=ax1)

 ax2= plt.subplot(gs[1])
 ser.plot(kind = 'bar', ax=ax2, label = '%.2f'%(ser['bursa']-ser['cum_total']))
 plt.legend(loc='best')
 plt.savefig('Investors/Yo/' + 'Edo_Yo_' + month + '.pdf')
 plt.show()

