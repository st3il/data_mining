__author__ = 'Jackdecrack'

import pandas as pd;

import numpy as np;

import matplotlib.pyplot as plt;

s = pd.Series([1,3,5,np.nan, 6,8]);
print s;

# Creating a Series by passing a list of values, letting pandas create a default integer index

dates = pd.date_range('20130101', periods=6);

print("Datum: " + str(dates[1]));

df = pd.DataFrame(np.random.randn(6,4), index = dates, columns=list('abcd'))

print(df);

print(df.tail())

print(df.index)
df.reindex;
print(df.index)
