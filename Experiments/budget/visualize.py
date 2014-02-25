import numpy as np
import matplotlib.pyplot as plt

dataFile = open('output.o', 'r')

data = dataFile.read()
exec("data = " + str(data))
dataFile.close()


x = []
y = []
error = []

for size in sorted(data.keys()):
	l = data[size]
	x.append(size)
	y.append(np.mean(l))
	error.append(np.std(l))
	

fig, ax0 = plt.subplots(nrows=1, sharex=True)
ax0.errorbar(x, y, yerr=error, fmt='-o')
ax0.set_title('')
ax0.set_xlabel('Attention Budget Ratio')
ax0.set_ylabel('Steps')


plt.show()
