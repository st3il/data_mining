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

dates = pd.date_range('20140101', periods=6);



df.index = dates;

print(df);
print(df.iloc[0:2, 0:2]);


ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))

ts.cumsum()
ts.plot()
print(ts);

plt.figure();
ts.plot(style='k--', label='Series');
plt.legend()
df.plot(subplots=True, figsize=(6, 6)); plt.legend(loc='best')

plt.show()

