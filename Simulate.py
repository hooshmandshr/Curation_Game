
import numpy.random as random
from Game import Game


g = Game()
g.playGame()

'''
print "Intrinsic content values:"
print g.Value
print '\n'

print "Potential Gain of publishing contents:"
g.updateGain
print g.Gain
print '\n'


R = g.readers()
P = g.publishers()
C = g.contents()

print "Edges:"
print g.Graph.edges()
print '\n'

print "Contents:\t" + str(g.contents())
print "Publishers:\t" + str(g.publishers())
print "Readers:\t" + str(g.readers())
print '\n'

print "Utilities:"
g.updateUtility()
print g.Utility
print '\n'

print "Potential Gain:"
g.updateGain()
print g.Gain
print '\n'

i = 0
previous = g.Graph.edges(g.contents())
#print g.Gain
g.playRound()
print "Round " + str(i) + ":"
print g.Graph.edges(g.contents())
current = g.Graph.edges(g.contents())
g.updateUtility
print g.Utility
while not(set(current) == set(previous)): 
	i += 1
	print "Round " + str(i) + ":" 
	#print g.Gain
	previous = current
	current = g.Graph.edges(g.contents())
	g.playRound()
	print g.Graph.edges(g.contents())
	g.updateUtility
	print g.Utility
'''

