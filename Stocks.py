#!/usr/bin/env python

# Add fit with straight line 
# Add volume of the stocks
# Write the documentation

"""
 This code has been built to analyse and plot stock data.
 It contains function to produce the best file value between
 two given dates. It also displays conficende levels.
"""

import pylab
import os, sys
import numpy as np
import matplotlib as mpl
from scipy import optimize
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
	DayLocator, MONDAY, MonthLocator
from matplotlib.finance import *
#from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc,\
#	volume_overlay2	
import datetime
import matplotlib.gridspec as gridspec

candle = False
volumen = True

        #today
today        = datetime.date.today()
hoy, mon_hoy = int(today.strftime('%d')), int(today.strftime('%m')) 
year_hoy     = int(today.strftime('%Y'))

date2 = datetime.date(year_hoy, mon_hoy, hoy)

	#Some locators useful for the thicks
mondays = WeekdayLocator(MONDAY)        
alldays = DayLocator()              
weekFormatter = DateFormatter('%b %d')  
dayFormatter = DateFormatter('%d')      
months    = MonthLocator(range(1, 13), bymonthday=1, interval=1)
monthsFmt = DateFormatter("%d '%b")

if len(sys.argv) > 1:
   which_names ='%s'%(sys.argv[1])
else:
   sys.exit("""Options:
     which_names = 'All (+ Buy/Sell)'
     which_names = 'Long_term'
     which_names = 'On_line'
     which_names = 'Buy_sell'
     which_names = 'Careful'
     which_names = 'Just_trust'
     which_names = 'Have'
     which_names =  or the name of the Stock (+ 'hoy')
     """)


select = 'True'
if ((len(sys.argv) > 2) and (sys.argv[1] == 'All' or sys.argv[1] == 'Have')):
   action = '%s'%(sys.argv[2])
   if   'Buy'  in action: select = 'tol < -delta+0.01'
   elif 'Sell' in action: select = 'tol > delta-0.01'
   elif 'Hold' in action: select = '(tol < delta-0.01) and (tol > -delta+0.01)'


        # Stocks that I have
names_have = ['AMZN','NFLX','AXTELCPO','VOLARA','GOOG','MSFT','FB','SBUX','GRUMAB','AEROMEX',
		'DIS','EDZ','EDC','FAS','FAZ','GILD','ICA',
		'TSLA','NKE','AAPL','AZTECACPO','YHOO','TLEVISACPO']

long_term  = ['VOLARA','AMZN','NFLX','SBUX','TSLA','IBB','OMAB','GRUMAB'] 
on_line    = ['FB','NKE','DIS','AAPL','BA','ASURB'] 
buy_sell   = ['GILD','AEROMEX','GOOG','MSFT','TLEVISACPO','YHOO'] 
careful    = ['ICA','AXTELCPO','IAU','SLV','TWTR'] 
just_trust = ['EDZ','DOG','FAZ','EDC','FXI','FAS']

rest	   = ['CVS','GS','IYH','JPM','FDX','QQQ','UWM','DAL','INTC',
		'BABAN','VNQ']

if 'Long_term'    in which_names:   names = long_term 
elif 'On_line'    in which_names:   names = on_line 
elif 'Buy_sell'   in which_names:   names = buy_sell
elif 'Careful'    in which_names:   names = careful
elif 'Just_trust' in which_names:   names = just_trust
elif 'Have'       in which_names:   names = names_have
elif 'All'        in which_names:
        names = long_term + on_line + buy_sell + careful + just_trust + rest 

else:                               names = ['%s'%(which_names)]  



	#Functions
def errorfill(x, y, yerr, color=None, alpha_fill=0.05, ax=None):
    ax = ax if ax is not None else plt.gca()
    if color is None:
        color = ax._get_lines.color_cycle.next()
    if np.isscalar(yerr) or len(yerr) == len(y):
        ymin  = y - yerr
        ymax  = y + yerr
    elif len(yerr) == 2:
        ymin, ymax = yerr

    ax.plot(x, y, color=color)
    ax.fill_between(x, ymax, ymin, color=color, alpha=alpha_fill)


def modelfit(x, a, b, n):
#    n = 1
    return a - b*(x**n)

def modelfit2(x, a, b, n):
#    n = 1      
    return a - b*(x**n)

def model_err(x, pars, pcov):
    a, b, n = pars
    ipcov = pcov # np.linalg.inv(pcov)
    s=1
    fx = -b*x**n*np.log(x+0.001) 
    col1 = ipcov[0][0]**s - ipcov[0][1]**s*(x**n) + ipcov[0][2]**s*fx
    col2 = ipcov[1][0]**s - ipcov[1][1]**s*(x**n) + ipcov[1][2]**s*fx
    col3 = ipcov[1][1]**s - ipcov[1][2]**s*(x**n) + ipcov[2][2]**s*fx

    da = col1
    db = [a*b for a,b in zip(-x**n,col2)]
    dn = [a*b for a,b in zip(fx,col3)]

    value =  np.sqrt(abs(da + db +dn)*2.)      
    return value


def model(params, x):
    a, b, n = params
    return a - b*(x**(n))


def ln_likelihood(params, x, y, ivar):
    return np.sqrt((model(params, x) - y)**2 * ivar)


def draw_hline(name, color='y', ll = None):
    last_mond  = today - datetime.timedelta(days=today.weekday())
    last2_mond = today - datetime.timedelta(days=today.weekday()+7)

    quotes = quotes_historical_yahoo_ohlc(name+'.mx', last2_mond, last_mond)
    yi, yf = quotes[0][4], quotes[len(quotes)-1][4]

    if yi < yf: color = 'Lime'
    else:       color = 'Tomato'
    ax.axhline(y=yi, xmin=0, xmax=1, color = 'Gold', linewidth=3)     
    ax.axhline(y=yf, xmin=0, xmax=1, color = color, linewidth=3)
    if ll != None:
       ax.axhline(y=ll, xmin=0, xmax=1, color = 'cyan', linewidth=3) 


def draw_bar(d,m,y):
    date = datetime.date(2015, m, d)
    pylab.bar(date, y, 2, color='y', alpha=0.5)


def anota(text, color, xy= [0.4,0.90]):
    ax.annotate(text, xy= (xy[0], xy[1]),xycoords='axes fraction',
                   fontsize=30,horizontalalignment='right',verticalalignment='bottom', color= color)

def anotatep(text, xy, color='gold'):
    ax.annotate(text, xy=xy,xycoords='axes fraction', fontsize=18, horizontalalignment='right',  
                   bbox={'alpha':0.4,'pad':10,'facecolor':color},  verticalalignment='bottom')



	#Main body of the code
for name in names:
   print (name)	
   delta = 0.025	#for a year
   day_in, mon_in, year_in = hoy, int((mon_hoy + 12)%12), year_hoy-1

   if name in ['SBUX']:
      delta = 0.025
      day_in, mon_in, year_in = 15, 04, 2015
   elif name in ['IYH','TWTR']:
      day_in, mon_in, year_in = 15, 11, 2014	   
   elif name in ['EDZ','EDC','FAS']:
      day_in, mon_in, year_in = 21, 05, 2015 
   elif name in ['TSLA']:
      delta = 0.045
      day_in, mon_in, year_in = 15, 05, 2015
   elif name in ['AMZN','FDX','IBB','INTC','DAL','VNQ']:
      delta = 0.065
      day_in, mon_in, year_in = 25, 07, 2014
    
   elif name in ['BA','TLEVISACPO','FB','CVS', 'GOOG','DIS','AAPL','OMAB','GS','JPM']:
      delta = 0.04
   elif name in ['GILD']:
      delta = 0.05
   elif name in ['GRUMAB','MSFT','VNQ','INTC']:
      delta = 0.06
   elif name in ['AXTELCPO','VOLARA','AEROMEX','FXI','DAL','NFLX']:
      delta = 0.075	   
   if name in ['EDZ','EDC']:
      delta = 0.15  

   date1 = datetime.date(year_in, mon_in, day_in)
   
   if name in 'NADA':
      date3 = datetime.date(2015, 06, 25)	   
      quotes2 = quotes_historical_yahoo_ohlc(name+'.mx', date1, date3) 	   
      dates2 = [q[0] for q in quotes2]
      closes2 = [q[2] for q in quotes2]

      quotes3 = quotes_historical_yahoo_ohlc(name+'.mx', date3, date2)		
      dates3  = dates2 +  [q[0] for q in quotes3]
      closes3 = closes2 + [7.*q[2] for q in quotes3]


	#Fill up stock values
   quotes = quotes_historical_yahoo_ohlc(name+'.mx', date1, date2)
   if len(quotes) == 0:
		         raise SystemExit

   dates = [q[0]+1 for q in quotes]
   opens = [q[1] for q in quotes]
   closes = [q[4] for q in quotes]
   volumes2 = [q[5] for q in quotes]
   volumes =  volumes2/max(volumes2)*closes[-1]/1.5
   #print max(volumes2)
#   print len(closes), len(dates)
#   print dates, len(dates)
#   print dates[len(dates)-10:len(dates)]
   #for s in range(len(dates)-1,len(dates)-11,-1):

   ldates = len(dates)
   #print np.array(closes[ldates - 10 - i: ldates - i]).sum()
   ma, ma2, ma3, ma4 = 100, 50, 30, 10
   Mave  = [ np.array(closes[ldates - ma  - i: ldates - i]).sum()/ma  for i in range(0,ldates-ma)]  #ldates+ma ,-1,-1)]   
   Mave2 = [ np.array(closes[ldates - ma2 - i: ldates - i]).sum()/ma2 for i in range(0,ldates-ma2)] 
   Mave3 = [ np.array(closes[ldates - ma3 - i: ldates - i]).sum()/ma3 for i in range(0,ldates-ma3)] 
   Mave4 = [ np.array(closes[ldates - ma4 - i: ldates - i]).sum()/ma4 for i in range(0,ldates-ma4)] 
#   print  closes[ldates - ma4: ldates],  np.array(closes[ldates - ma4: ldates]).sum()/ma4
	#Fit data and get cov matrix
   p_opt, pcov = optimize.curve_fit(modelfit, np.array(dates[-1])-np.array(dates), closes)
#   p_opt2, pcov2 = optimize.curve_fit(modelfit2, np.array(dates[-1])-np.array(dates), closes)
   #stock_err = model_err(np.array(dates[-1]) - np.array(dates), p_opt, pcov)

	# a,b,n  Compute percentages and three diff point
   pars = [p_opt[0], p_opt[1], p_opt[2]]
#   pars2 = [p_opt2[0], p_opt2[1], 1.]
#   print 'params', pars

   y_ini   = model(pars, np.array(dates[-1]) - np.array(dates[0]))
   y_mid   = model(pars, np.array(dates[-1]) - np.array(dates[len(dates)//2]))
   y_today = model(pars, np.array(dates[-1]) - np.array(dates[len(dates)-1]))

   perc_tot  = ((y_today - y_ini)/y_today*100)
   perc_mid2 = ((y_today - y_mid)/y_today*100)
   perc_mid  = ((y_mid   - y_ini)/y_mid*100)

   tol= ((closes[-1] - y_today)/y_today)

	# Best fit value
   stock  = model(pars, np.array(dates[-1]) - np.array(dates)) 	
#   stock2  = model(pars2, np.array(dates[-1]) - np.array(dates))


	# draw figures
   if(eval(select)):
     fig = plt.figure(figsize=(11,9))
     gs = gridspec.GridSpec(2, 1, height_ratios=[3,1])
     #fig, (ax, ax2) = plt.subplots(2, sharex=True, figsize=(12,8))
     #fig, (ax,ax2) = plt.subplots(figsize=(12,8))
     gs.update(left=0.05, right=0.95, top=0.95, bottom =0.05, hspace = 0.)
     ax = fig.add_subplot(gs[0])
    # gs.update(left=0.05, right=0.48, wspace=0.05)
     ax2 = fig.add_subplot(gs[1])
     #fig.subplots_adjust(bottom=0.)
     #ax.xaxis.set_major_locator(months)
     #ax.xaxis.set_major_formatter(monthsFmt)
     ax.xaxis.set_major_locator(mondays)
     #ax.xaxis.set_minor_locator(alldays)
     ax.xaxis.set_major_formatter(weekFormatter)

     ax2.xaxis.set_major_formatter(monthsFmt)
     ax2.xaxis.set_major_locator(mondays)
     ax2.xaxis.set_minor_locator(alldays)
     ax2.xaxis.set_major_formatter(weekFormatter)

     if (candle):
        candlestick_ohlc(ax, quotes, width=0.6, colorup='g', colordown='r')
     if (volumen):
	ax2.bar(dates, volumes, 1, color='b', alpha=0.5)

     draw_hline(name)
     ax.plot_date(dates, closes, 'k-')

#Filling
#     fig.subplots_adjust(hspace=0)
#     if ( p_opt[1]>= 0 and p_opt[2]>= 0): #name in just_trust): 
#        errorfill(dates, stock, stock*delta, color='red', ax=ax)
#        ax.plot_date(dates, stock*(1+ delta), 'b-')
#        ax.plot_date(dates, stock*(1- delta), 'b-')
#	errorfill(dates, stock2, stock*delta, color='g')
	
     ax.plot_date(dates[ma:ldates] , Mave[::-1], 'r-')
     ax.plot_date(dates[ma2:ldates], Mave2[::-1], 'b-')
     ax.plot_date(dates[ma3:ldates], Mave3[::-1], 'g-')
     ax.plot_date(dates[ma4:ldates], Mave4[::-1], color='Gold',linestyle='-', fmt='')

     ax2.xaxis.set_major_locator(months)
     ax2.xaxis.set_major_formatter(monthsFmt)
     ax2.xaxis.set_minor_locator(mondays)
     ax2.xaxis.set_major_formatter(weekFormatter)
     ax.xaxis.set_major_locator(months)
     ax.xaxis.set_major_formatter(monthsFmt)
     ax.xaxis.set_minor_locator(mondays)
     ax.xaxis.set_major_formatter(weekFormatter)
     ax.set_title(name)
     ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
     ax.yaxis.grid(True,'minor')
     ax.yaxis.grid(True,'major', color='k',linestyle='-', alpha=0.8)
     ax.xaxis.grid(True, 'major')
     ax.xaxis.grid(True, 'minor')
     ax.grid(True)
     ax.yaxis.tick_right()
     ax.autoscale_view()   
#     ax2.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
#     ax2.yaxis.grid(True,'minor')
#     ax2.yaxis.grid(True,'major', color='k',linestyle='-', alpha=0.8)
#     ax2.xaxis.grid(True, 'major')
#     ax2.xaxis.grid(True, 'minor')
     ax2.grid(True)
#     ax2.yaxis.tick_right()
					
#     fig.autofmt_xdate()
#     plt.tight_layout()
#     plt.ylim(y_ini*(1-delta), plt.ylim()[-1])
#     ax.autoscale_view()
#     fig.subplots_adjust(hspace=0)
#     ax2 = fig.add_subplot(gs[1])
#     ax2.bar(dates, volumes, 1, color='b', alpha=0.5)
#     ax2.grid(True)

#Some comments for each plot

#     anotatep('Total: %2.2f%%, for %i months'%(perc_tot, mon_hoy-mon_in), xy=(0.6,0.2))
#     anotatep('1st half: %2.2f,\t 2nd half: %2.2f'%(perc_mid, perc_mid2) , xy=(0.6,0.1))
     if (1-p_opt[2]) > 0: acolor = 'green'
     else               : acolor = 'red'
     anotatep('1 - Tilt: %2.2f'%(1-p_opt[2]),xy=(0.5,0.02), color =acolor)

   
#     if tol > delta-0.01:                      anota('Sell, tol = %2.1f%%'%(tol*100),     color='red')
#     elif (tol < -delta+0.01 and tol > -0.07) : anota('Buy,  tol = %2.1f%%'%(tol*100),     color='green')
#     elif (tol < -0.07) :                      anota('Careful!, tol = %2.1f%%'%(tol*100), color='purple')
#     else:                                     anota('Hold, tol = %2.1f%%'%(tol*100),     color='blue')
     anota('$\Delta$ = %2.1f%%'%(delta*100),     color='Gold', xy= [0.4,0.80])

     draw_hline(name)


	#Stock that I have, and dates when I bought them
     if False:
      if name in names_have:
	if not (name in just_trust):
	   plt.ylim(y_ini*(1-delta), plt.ylim()[-1])
        if 'DAL' in name:
  	   draw_bar(24,06,668.1)
	   plt.ylim(y_ini*(1-5*delta), plt.ylim()[-1]) 
        elif 'DIS'        in name:     draw_bar(11,06, 1700.0 )
        elif 'GILD'       in name:     draw_bar(13,06, 1814.5 )
        elif 'GS'         in name:     draw_bar(31,05, 3180.5 )
	elif 'GRUMAB'     in name:     draw_bar(22,07, 206.5 )
        elif 'IBB'        in name:     draw_bar(23,06, 5900.5 )
        elif 'NFLX'       in name:     draw_bar(22,06, 1488.5)
        elif 'NKE'        in name:     draw_bar( 8,07, 1740.5 )
        elif 'OMAB'       in name:     draw_bar(26,06, 75.9   )
        elif 'SBUX'       in name:     draw_bar(26,05, 790.8  )
        elif 'TSLA'       in name:     draw_bar(21,05, 3782.8 )
        elif 'TWTR'       in name:     draw_bar(21,05, 577.8 )
        elif 'VOLARA'     in name:     draw_bar(21,07, 22.1   )
        elif 'ASURB'      in name:     draw_bar(9,07,  230.58 )
        elif 'AEROMEX'    in name:     draw_bar(9,07,  26.7   )
        elif 'SPORTS'     in name:     draw_bar(9,07,  20.7   )
        elif 'TLEVISACPO' in name:     draw_bar(13,07, 114.02 )
        elif 'AMZN'       in name:     draw_bar(13,07, 7153.02 )

   
     if ((len(sys.argv) > 2) and not ('All' in sys.argv[1] or 'Have' in sys.argv[1])):
        draw_hline(name, ll = sys.argv[2])	   

   #plt.draw()
   #plt.savefig(name+".pdf")
   plt.show()
