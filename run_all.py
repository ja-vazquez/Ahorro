
import os,sys
import pandas as pd

df = pd.read_csv('inv_names.csv',names=['names'])
inv_names = df['names'].tolist()


for inv in inv_names:
	os.system(r"python2.7 Cuenta.py %s"%(inv))

commd = """
python2.7 my_account.py
cd ../Investing/
python2.7 investing.py
python2.7 investing.py e"""
os.system(commd)
