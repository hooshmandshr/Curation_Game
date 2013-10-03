import sys, os
import networkx as nx
import numpy.random as rand 
import math
from CurationGame import CurationGame


g = CurationGame()
g.initialize()
g.updateUtility()

publishers = g.Class['publisher']
contents = g.Class['content']

profile = {}

for p in publishers:
	profile[p] = []
	threshold = rand.rand()
	for c in contents:
		if rand.rand() > threshold:
			profile[p].append(c)
print len(g.Graph.edges())

g.carryOutActionProfile(profile)
print len(g.Graph.edges())
g.updateUtility()

print g.Utility


'''
for reader in g.Value:
	print g.Value[reader]
print g.Class
print g.Graph.edges()
print g.Utility
'''
