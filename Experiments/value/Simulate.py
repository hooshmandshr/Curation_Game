
import numpy.random as random
from Game import Game
from numpy import random
import numpy

def matrix(C, R, alpha):

	matrix = []

	for c in range(0, C):
		matrix.append([])
		s = random.pareto(alpha)
		for r in range(0, R):
			matrix[-1].append(abs(s*random.normal()))

	Matrix = []
	for r in range(0, R):
		Matrix.append([])
		for c in range(0, C):
			Matrix[-1].append(matrix[c][r])

	return Matrix

def umatrix(C, R):

	matrix = []

	for r in range(0, R):
		matrix.append([])	
		for c in range(0, C):
			matrix[-1].append(abs(random.rand()*50))

	return matrix


report = open('output.o', 'w')

data = {'pareto': {}, 'uniform': {}}

alpha = 4

for size in range(20, 70):
	data['pareto'][size] = []
	data['uniform'][size] = []
	for i in range(0, 10):
		g = Game(size,0.5, 0.5, 0.3, 0.2)
		C = len(g.contents())
		R = len(g.readers())

		g.reset()
		g.setValue(matrix(C, R, 4))
		steps = g.playGame()
		g.reset()
		g.setValue(umatrix(C, R))
		usteps = g.playGame()

		data['pareto'][size].append(steps)
		data['uniform'][size].append(usteps)

report.write(str(data))

report.close()
