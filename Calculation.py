

from People import *
import numpy as np

class Calculation:
    def __init__(self, Person, months, dates, depos):
        self.person  = Person
        self.months  = months
        self.dates   = dates
        self.depos   = depos
        self.all_months  = self.person.init_month + self.months



    def interest(self, today):
        self.today   = today
        self.lmonths = len(self.all_months)
        self.ldates  = len(self.dates)

        interes   = np.zeros(self.ldates)
        deposito  = np.zeros(self.ldates)

        tot_depos = np.zeros(self.lmonths)
        tot_inter = np.zeros(self.lmonths)


        i, k  = 0, 0

        for l, _ in enumerate(self.dates):
            deposito[l] = float(self.depos[l])

                #fraction of the percentage depending on the deposit day
            if self.all_months[-1] == self.dates[l][3:]:
                fraction   =  (self.today - float(self.dates[l][:2]))/30.
            else:
                fraction   =  (30 - float(self.dates[l][:2]))/30.


            interes[l] = deposito[l]*fraction*self.person.perct

                #account per month
            if self.all_months[i] in self.dates[l][3:]:
                tot_depos[i] += deposito[l]
                tot_inter[i] += interes[l]
                k += 1
            else:
                k = 0
                i += 1
                tot_depos[i] += deposito[l]
                tot_inter[i] += interes[l]


        self.kk        = k
        self.interes   = interes
        self.tot_depos = tot_depos
        self.tot_inter = tot_inter




    def total(self):
        self.sum_tot_depos = np.zeros(self.lmonths)
        self.sum_tot_inter = np.zeros(self.lmonths)
        self.cumul_inter   = np.zeros(self.lmonths)
        self.final         = np.zeros(self.lmonths)

        tmp1, tmp2, cumul = 0, 0, 0

        for i in range(self.lmonths):
            tmp1            += self.tot_depos[i]
            tmp2            += self.tot_inter[i]

            self.sum_tot_depos[i]+= tmp1
            self.sum_tot_inter[i]+= tmp2

            #fraction of the month
            frac = (self.today -1.)/30. if i==(self.lmonths-1) else 1

            self.cumul_inter[i]  = 0 if i==0 else self.sum_tot_depos[i-1]*self.person.perct*frac
            self.final[i]      = tmp1 + tmp2 + self.cumul_inter.sum()
















