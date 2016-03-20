

from People import *
import numpy as np

class Calculation:
    def __init__(self, Person, month, dates, depos):
        self.month   = month
        self.dates   = dates
        self.depos   = depos
        self.person  = Person
        self.months  = self.person.months + self.month



    def interest(self, hoy):
        self.lmonths = len(self.months)
        self.ldates  = len(self.dates)

        percentage= np.zeros(self.ldates)
        interes   = np.zeros(self.ldates)
        deposito  = np.zeros(self.ldates)

        tot_depos = np.zeros(self.lmonths)
        tot_inter = np.zeros(self.lmonths)
        lfraction = np.zeros(self.lmonths)


        i, k  = 0, 0

        for l, _ in enumerate(self.dates):
            deposito[l] = float(self.depos[l])

                #fraction of the percentage depending on the deposit day
            if self.month[-1] == self.dates[l][3:]:
                fraction   =  (hoy - float(self.dates[l][:2]))/30.
            else:
                fraction   =  (30 - float(self.dates[l][:2]))/30.

            percentage[l] = fraction*self.person.perct
            interes[l]    = deposito[l]*percentage[l]


                #account per month
            if self.months[i] in self.dates[l][3:]:
                tot_depos[i] += deposito[l]
                tot_inter[i] += interes[l]
                k += 1
            else:
                k = 0
                i += 1
                tot_depos[i] += deposito[l]
                tot_inter[i] += interes[l]


        self.kk        = k
        self.hoy       = hoy
        self.interes   = interes
        self.depos     = deposito
        self.tot_depos = tot_depos
        self.tot_inter = tot_inter




    def total(self):
        sum_tot_depos = np.zeros(self.lmonths)
        sum_tot_inter = np.zeros(self.lmonths)
        cumul_inter   = np.zeros(self.lmonths)
        final         = np.zeros(self.lmonths)

        tmp1, tmp2, cumul = 0, 0, 0

        for i in range(self.lmonths):
            tmp1            += self.tot_depos[i]
            tmp2            += self.tot_inter[i]

            sum_tot_depos[i]+= tmp1
            sum_tot_inter[i]+= tmp2

            #fraction of the month
            tmp3 = (self.hoy -1.)/30. if i==(self.lmonths-1) else 1

            cumul_inter[i]  = 0 if i==0 else sum_tot_depos[i-1]*self.person.perct*tmp3
            final[i]      = tmp1 + tmp2 + cumul_inter.sum()



        self.sum_tot_depos = sum_tot_depos
        self.sum_tot_inter = sum_tot_inter
        self.cumul_inter   = cumul_inter
        self.final         = final














