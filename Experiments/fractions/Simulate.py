
import numpy.random as random
from Game import Game
import numpy as np

report = open('output.o', 'w')

data = {}


size = 50



X = []
Y = []
Z = []

for alpha in np.arange(0, 1, 0.05):
	X.append([])
	Y.append([])
	Z.append([])
	for beta in np.arange(0, 1, 0.05):
		X[-1].append(alpha)
		Y[-1].append(beta)
		if alpha+beta>1:
			Z[-1].append(0)
			continue
		g =  Game(size, 0.5, alpha, beta)
		steps = g.playGame()
		Z[-1].append(steps)
		

data = [X, Y, Z]
report.write(str(data))

report.close()
