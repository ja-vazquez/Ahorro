#!/usr/bin/env python
import pylab
import matplotlib.pyplot as plt

def Compu(init, inters, months):	
    val=0
    init = init*(1.0 + inters)**(months)
    for i in range(1,months+1):
        val+=(1+inters)**(i) 
    val_mon = pay_mon*val
    final = init + val_mon
    return final

init   = 13000
pay_mon= 7000

#m=[1,2,3,4,5,6,7,8,9,10,11,12]
m=[6,12,18,24,36,48,60,72,84,96,108,120,180,240]
#m=[2,4,6,7,8,9,10,12,18,24,36,48,60,72,84,96,108,120,180,240]
ml=[]
sal=[]
invl=[]
for months in m:
 months = months*1

 saving =init + months*pay_mon
 invest =Compu(init, 0.025  ,months)
 bank  =Compu(init, 0.007 ,months)

 print '# months: ', months
 print 'Investing:  %.2f'%(invest), 'earnings: %.2f'%(invest - saving)
 print 'Bank:       %.2f'%(bank), 'earnings: %.2f'%(bank - saving)
 print 'Saving:   ', saving
 print '---------'

 ml.append(months)
 sal.append(saving)
 invl.append(invest)

#fig = plt.figure(figsize=(10,4))
#ax=fig.add_subplot(1,1,1)
#ax.plot(ml, invl, 'g--', label = "$\Omega_{dm}$")
#ax.plot(ml, [16000, 16517.11, 21047.22, 31820.15, 40146.15])
#plt.show()

