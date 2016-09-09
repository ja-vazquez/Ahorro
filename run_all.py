
import os,sys
import pandas as pd

df = pd.read_csv('inv_names.csv',names=['names'])
inv_names = df['names'].tolist()

for inv in inv_names:
	os.system(r"python Cuenta.py %s"%(inv))

os.system("python my_account.py")

