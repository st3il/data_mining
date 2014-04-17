import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0, 6, 0.2)

plt.subplot(241)
plt.plot(t**2, 'r')
plt.axis([0, 6, 0, 0.5])
plt.title('Foo')





plt.show()