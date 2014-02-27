import numpy.random as random
from Game import Game

report = open('output.o', 'w')

data = {}

size = 50
while size < 60:

        size += 10
        data[size] = []
        for i in range(0, 5):

                density = 1
                if  0.1 * size > 7:
                        density = 7.0 / (density * 0.1)

                limit = 0.2 
                g = Game(size, density, limit, 0.3, 0.1)
                steps = g.playGame()
                data[size].append(steps)

report.write(str(data))

report.close()

