
import numpy.random as random
from Game import Game
import numpy

report = open('output.o', 'w')

data = {}

size = 30
density = 0
g = Game(size, density, 0.5, 0.3, 0.3)
count = 0
for r in g.readers():
	for p in g.publishers():
		g.reset()
		g.Graph.add_edge(r, p)
		steps = g.playGame()
		count += 1
		data[count] = []
		data[count].append(steps)

report.write(str(data))

report.close()
