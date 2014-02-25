
import numpy.random as random
from Game import Game

report = open('output.o', 'w')

data = {}

size = 200
g = Game(size, 0.5, 0.5, 0.3, 0.3)
steps = g.playGame()
print steps

report.write(str(data))

report.close()
