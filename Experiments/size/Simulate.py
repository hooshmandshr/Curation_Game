
import numpy.random as random
from Game import Game

report = open('output.o', 'w')

data = {}

size = 10
while size < 100:

	size += 10
	data[size] = []
	for i in range(0, 10):
		g = Game(size, 0.5, 0.5, 0.3, 0.3)
		steps = g.playGame()
		data[size].append(steps)

report.write(str(data))

report.close()
