import sys, os
import networkx as nx
import numpy.random as rand 
import math


class CurationGame:
	
	def __init__(self):
		
		self.Graph = nx.Graph()
		self.Class = {'content': [], 'publisher': [], 'reader': []}
		self.Value = {}
		self.Utility = {}

	def initialize(self):

		N = 50
		# cumulative distribution
		ClassDistribution = {'content': 0.3, 'publisher': 0.5, 'reader': 1}
		Classes = self.Class.keys()
		for i in range(1, N):
			r = rand.rand()
			for c in Classes:				
				if r < ClassDistribution[c]:

					self.Graph.add_node(i, label=c)
					break

		Readers = self.Class['reader']
		Publishers = self.Class['publisher']
		Contents = self.Class['content']

		# aggregating nodes of different class
		V = self.Graph.nodes()
		for v in V:
			classes = self.Class.keys()
			for c in classes:
				if self.Graph.node[v]['label'] == c:
					self.Class[c].append(v)
					break

		# Constructing intrinsic values of the 
		for v in Readers:
			self.Value[v] = {}
			for u in Contents:
				self.Value[v][u] = int(rand.rand()*20)


		# Constructing Utility List
		for v in Publishers:
			self.Utility[v] = 0

		# Adding Edges
		for v in Readers:
			threshold = rand.rand()

			for u in Publishers:
				r = rand.rand()
				if r > threshold and u != v:
					self.Graph.add_edge(v, u)

	# action profile is a dictionary {..., publisher_1:[..., content_i_j, ...], ...}
	def carryOutActionProfile(self, ActionProfile):

		ActionProfileEdgeList = []
		if isinstance(ActionProfile, dict):
			#ActionProfileEdgeList = []
			for publisher in ActionProfile:
				for content in ActionProfile:
					ActionProfileEdgeList.append((content, publisher))
		else:
			ActionProfileEdgeList = ActionProfile

		Publishers = self.Class['publisher']
		PreviousProfile = set(self.Graph.edges(Publishers))
		NextProfile = set(ActionProfileEdgeList)
		
		ToBeRemoved = PreviousProfile.difference(NextProfile)
		ToBeAdded = NextProfile.difference(PreviousProfile)

		ContentEdges = self.Graph.edges(self.Class['content'])
		self.Graph.remove_edges_from(ContentEdges)

		self.Graph.add_edges_from(ActionProfileEdgeList)
		print self.Graph.edges(self.Class['publisher'])
		
		print self.Class['content']
		print self.Class['publisher']
		print self.Class['reader']
		#update potential values of all readers (amount that they can contribute for next step)
	

	def updateUtility(self):

		Sharer = {}
		for content in self.Class['content']:
			Sharer[content] = set(self.Graph.edges(content))

		Medium = {}
		for reader in self.Class['reader']:
			Medium[reader] = set(self.Graph.edges(reader))

		print Sharer
		print Medium
		for reader in self.Class['reader']:
			for content in self.Class['content']:
				RewardedPublishers = Medium[reader].intersection(Sharer[content])
				if len(RewardedPublishers) > 0:
					Reward = float(self.Value[reader][content])/float(len(RewardedPublishers))
				for publisher in RewardedPublishers:
					self.Utility[publisher] += Reward 
		#TODO
		
		Readers = self.Class['reader']
		for publisher in self.Utility:
			self.Utility[publisher] = 0

		for reader in Readers:
			ShareCount = {}
			for content in self.Class['content']:
				ShareCount[content] = []
			followee = self.Graph.neighbors(reader)
			for publisher in followee:
				SharedContent = self.Graph.neighbors(publisher)	
				SharedContent = list( set(SharedContent).difference(set(self.Class['reader'])) )
				#print SharedContent
				for content in SharedContent:
					ShareCount[content].append(publisher)
			
			for content in self.Value[reader]:
				for publisher in ShareCount[content]:
					self.Utility[publisher] += float(self.Value[reader][content])/float(len(ShareCount))

		
	# TODO
	#def singleStepBestResponse(self, publisher):

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


