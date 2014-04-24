import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

z = np.random.randn(4,4)

#ts = Series(randn(1000), index=date_range('1/1/2000', periods=1000))

ts = pd.DataFrame(z, index=['a', 'b', 'c', 'd'], columns=['x','v','b','n' ])

#print ts
#print ts['x']
#print ts[1:3]
print ts
print '\n'
print ts.sort_index(axis=0, ascending=False)
print '\n'
print ts.sort(columns='x', ascending=False)
