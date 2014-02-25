
"""
.. versionadded:: 1.1.0
   This demo depends on new features added to contourf3d.
"""

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy

dataFile = open('output.o', 'r')

data = dataFile.read()
exec("data = " + str(data))
dataFile.close()	

X = data[0]
Y = data[1]
Z = data[2]

print len(X)
print len(Y)
print len(Z)

print X
print Y
print Z

fig = plt.figure()
ax = fig.gca(projection='3d')


ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.3)
cset = ax.contourf(X, Y, Z, zdir='z', offset=-250, cmap=cm.coolwarm)
cset = ax.contourf(X, Y, Z, zdir='x', offset=-0.2, cmap=cm.coolwarm)
cset = ax.contourf(X, Y, Z, zdir='y', offset=-0.1, cmap=cm.coolwarm)

ax.set_xlabel('Fraction of nodes that are contents')
ax.set_xlim(-0.2, 1)
ax.set_ylabel('Fraction of nodes that are publishers')
ax.set_ylim(-0.1, 1)
ax.set_zlabel('Steps')
ax.set_zlim(-250, 250)

plt.show()

