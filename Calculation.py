

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

        tot_depos = np.zeros(self.lmonths)
        tot_inter = np.zeros(self.lmonths)
        interes = []
        i, k  = 0, 0

        for l, _ in enumerate(self.dates):
            deposito = float(self.depos[l])

                #fraction of the percentage depending on the deposit day
            percentage = (hoy - float(self.dates[l][:2]))/30. * self.person.perct
            interes.append(deposito*percentage)

                #account for each month
            if self.months[i] in self.dates[l][3:]:
                tot_depos[i] += deposito
                tot_inter[i] += deposito*percentage
                k += 1
            else:
                k = 0
                i += 1
                tot_depos[i] += deposito
                tot_inter[i] += deposito*percentage

        self.tot_depos = tot_depos
        self.tot_inter = tot_inter




    def total(self):
        sum_tot_depos = np.zeros(self.lmonths)
        final         = np.zeros(self.lmonths)
        tmp1, sum_tot_inter, cumul_inter = 0, 0, 0

        for i in range(self.lmonths):
            tmp1            += self.tot_depos[i]
            sum_tot_inter   += self.tot_inter[i]
            sum_tot_depos[i]+= tmp1

            cumul_inter  += 0 if i==0 else sum_tot_depos[i-1]*self.person.perct
            final[i]      = tmp1 + sum_tot_inter + cumul_inter

        return sum_tot_depos, final
















