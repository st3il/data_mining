import numpy as np
import matplotlib.pyplot as plt
rnd = np.random.normal(0, 1, 1000)
data = [rnd]
plt.boxplot(data)
plt.show()