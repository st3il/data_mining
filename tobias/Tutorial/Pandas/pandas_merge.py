import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


first = pd.DataFrame({'key': ['eins', 'zwei'], 'links': ['drei', 'vier']})
second = pd.DataFrame({'key': ['eins', 'zwei'], 'rechts': ['drei2', 'vier2']})

print first
print '\n'
print pd.merge(first, second, on='key')