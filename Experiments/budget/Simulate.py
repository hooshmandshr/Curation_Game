
import numpy.random as random
from Game import Game
import numpy

report = open('output.o', 'w')

data = {}

size = 50

for attention in numpy.arange(0.05, 0.95, 0.05):
	data[attention] = []
	for i in range(0, 5):
		g = Game(size, attention, 0.3, 0.3)
		steps = g.playGame()
		data[attention].append(steps)

report.write(str(data))

report.close()
