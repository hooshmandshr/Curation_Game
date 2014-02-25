import numpy as np
import matplotlib.pyplot as plt

dataFile = open('output.o', 'r')

data = dataFile.read()
exec("data = " + str(data))
dataFile.close()


x = {}
y = {}

error = {}

for distribution in (data.keys()):
	y[distribution] = [] 
	error[distribution] = []
	x[distribution] = []
	for size in sorted(data[distribution].keys()):
		l = data[distribution][size]
		x[distribution].append(size)
		y[distribution].append(np.mean(l))
		error[distribution].append(np.std(l))
	

fig, ax0 = plt.subplots(nrows=1, sharex=True)
ax0.errorbar(x['uniform'], y['uniform'], yerr=error['uniform'], fmt='-o')
ax0.errorbar(x['pareto'], y['pareto'], yerr=error['pareto'], color='r', fmt='-o')

ax0.set_title('')
ax0.set_xlabel('Size')
ax0.set_ylabel('Steps')

print data

plt.show()
