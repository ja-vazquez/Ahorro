
import os,sys
import pandas as pd

df = pd.read_csv('inv_names.csv',names=['names'])
inv_names = df['names'].tolist()

for inv in inv_names:
	os.system(r"python2.7 Cuenta.py %s"%(inv))

os.system("python2.7 my_account.py")

