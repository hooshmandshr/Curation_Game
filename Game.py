import networkx
import numpy.random as random
import sys, os
import pandas
import cfgparse
import numpy


def process(string, type='float'):
	
	string = string.replace(' ', '')
	string = string.split(',')
	l = []
	for element in string:
		command = 'l.append(' + type + '(element))'
		exec(command)
	l.sort()
	return l

class Game:
	
	def __init__(self):
		self.Graph = networkx.Graph()
		self.Class = {'content': [], 'publisher': [], 'reader': []}
		self.Value = None 
		self.Utility = {}
		self.ClassDistribution = {'content': 0.3, 'publisher': 0.5, 'reader': 1}

		self.Gain = {}

		self.Attention = 0 
		self.Size = 10
		
		self.initialize()

	def readers(self):
		return self.Class['reader']

	def contents(self):
		return self.Class['content']

	def publishers(self):
		return self.Class['publisher']

	def classes(self):
		return self.Class.keys()


	def initialize(self):

		self.configure()
	
		if self.Options.manualSetup == 1:
			self.manualSetup()	
			return

		#TODO setup graph nodes
		for i in range(1, self.Size):
			r = random.rand()
			for cl in self.ClassDistribution:
				if r < self.ClassDistribution[cl]:
					self.Graph.add_node(i, type=cl)
					self.Class[cl].append(i)
					break

		#TODO setup random values
		matrix = []
		for reader in self.readers():
			matrix.append([])
			for content in self.contents():
				matrix[-1].append(int(random.rand()*20)) 

		self.Value = pandas.DataFrame(matrix, index = self.readers(), columns = self.contents())

		#TODO set utility to zero
		for publisher in self.publishers():
			self.Utility[publisher] = 0

		#TODO setup subscribers
		for reader in self.readers():
			threshold = random.rand()
			for publisher in self.publishers():
				if (random.rand() < threshold):
					self.Graph.add_edge(reader, publisher)

		#TODO setup potential gains	
		self.updateGain()

		#TODO setup attention
		self.Attention = int(len(self.contents())/2)


	def manualSetup(self):

		command = "self.Class = " + self.Options.manualClass
		exec(command)

		#setting up the graph nodes
		for cl in self.Class:
			for node in self.Class[cl]:
				self.Graph.add_node(node, type=cl)

		#setting up the subscriptions
		edges = []
		command = "edges = " + self.Options.manualSubs
		exec(command)
		for e in edges:
			self.Graph.add_edge(e[0], e[1])

		#setting up the values
		values = {}
		matrix = []
		command = "values = " + self.Options.manualValues
		exec(command)
		for reader in self.readers():
			matrix.append([])
			for content in self.contents():
				matrix[-1].append(values[reader][content])	
		self.Value = pandas.DataFrame(matrix, index = self.readers(), columns = self.contents())

		# set utility to zero
		for publisher in self.publishers():
			self.Utility[publisher] = 0

		self.Attention = self.Options.limit

	def configure(self):

		configFile = 'config.ini'
		cparser = cfgparse.ConfigParser()

		cparser.add_option('size', dest='size', type='int', keys='DEFAULT')
		cparser.add_option('use_distribution', dest='flag', type='int', keys='DEFAULT')
		cparser.add_option('class_distribution', dest='cdf', type='string', keys='DEFAULT')
		cparser.add_option('class_population', dest='population', type='string', keys='DEFAULT')

		cparser.add_option('use_manual_definition', dest='manualSetup', type='int', keys='DEFAULT')
		cparser.add_option('class', dest='manualClass', type='string', keys='DEFAULT')
		cparser.add_option('values', dest='manualValues', type='string', keys='DEFAULT')
		cparser.add_option('subscriptions', dest='manualSubs', type='string', keys='DEFAULT')
		cparser.add_option('limit', dest='limit', type='int', keys='DEFAULT')

		cparser.add_file(configFile)

		self.Options = cparser.parse()

		self.Size = self.Options.size
		flag = self.Options.flag
		if flag:
			
			cdf = process(self.Options.cdf)
			self.ClassDistribution['content'] = cdf[0]
			self.ClassDistribution['publisher'] = cdf[1]
			self.ClassDistribution['reader'] = cdf[2]

		else:
			population = process(self.Options.population, type='int')
			self.Size = sum(population)

	def potential(self, publisher, content):

		gain = 0

		if not(publisher in self.publishers()) or not(content in self.contents()):
			
			print "Incorrect use of potential function..."
			return None

		neighbors = set(self.Graph.neighbors(publisher))
		subscribers = list(neighbors.difference(set(self.contents())))
		
		for reader in subscribers:
			followee = self.Graph.neighbors(reader)
			duplicate = []
			for pub in followee:
				if content in self.Graph.neighbors(pub):
					duplicate.append(pub)
				else:
					continue

			value = self.Value.lookup([reader], [content])
			duplicate = len(duplicate)

			if content in self.Graph.neighbors(publisher):
				#TODO change back to -=
				#gain -= float(value)/float(duplicate)
				gain += float(value)/float(duplicate)
			else:
				gain += float(value)/float(duplicate + 1)

		return gain

	# self.Gain in the form {..., publisher:[..., (gain, content#), ...], ...}
	def updateGain(self):
		self.Gain = {}
		for publisher in self.publishers():
			self.Gain[publisher] = []
			for content in self.contents():
				self.Gain[publisher].append((self.potential(publisher, content), content)) 

	
	def updateUtility(self):

		for publisher in self.Utility:
			self.Utility[publisher] = 0

		for reader in self.readers():
			for content in self.contents():
				rewardees = []
				for publisher in self.Graph.neighbors(reader):
					if content in self.Graph.neighbors(publisher):
						rewardees.append(publisher)
				raward = 0
				if len(rewardees) > 0:
					reward = float(self.Value.lookup([reader], [content]))/len(rewardees)
				for rewardee in rewardees:
					self.Utility[rewardee] += reward
	
	def playRound(self):
		
		self.updateGain()
		actionProfile = []
		for publisher in self.Gain:
			gainList = sorted(self.Gain[publisher])
			gainList.reverse()
			#print publisher
			#print gainList
			#print gainList[:self.Attention]

			for Tuple in gainList[:self.Attention]:
				content = Tuple[1]
				actionProfile.append((publisher, content))

		# delete previous strategies
		self.Graph.remove_edges_from(self.Graph.edges(self.contents()))
		
		# add the new action profile
		for edge in actionProfile:
			self.Graph.add_edge(edge[0], edge[1])

		self.updateUtility()

	def playIndividualRound(self):
		
		self.updateGain()

		publishers = self.publishers()
		publisher = publishers[self.Round % len(publishers)]
		

		actionProfile = []
		
		gainList = sorted(self.Gain[publisher])
		gainList.reverse()
		#print publisher
		#print gainList
		#print gainList[:self.Attention]

		for Tuple in gainList[:self.Attention]:
			content = Tuple[1]
			actionProfile.append((publisher, content))

		# delete previous strategies
		contents = self.contents()
		edges = self.Graph.edges(publisher)
		for edge in edges:
			if edge[0] in contents or edge[1] in contents:
				self.Graph.remove_edge(edge[0], edge[1])

		# add the new action profile
		for edge in actionProfile:
			self.Graph.add_edge(edge[0], edge[1])

		self.updateUtility()
		self.Round += 1
	
	'''
	def playIndividualRound(self, publisher):
		
		self.updateGain()

		publishers = self.publishers()	
		

		actionProfile = []
		
		gainList = sorted(self.Gain[publisher])
		gainList.reverse()
		#print publisher
		#print gainList
		#print gainList[:self.Attention]

		for Tuple in gainList[:self.Attention]:
			content = Tuple[1]
			actionProfile.append((publisher, content))

		# delete previous strategies
		contents = self.contents()
		edges = self.Graph.edges(publisher)
		for edge in edges:
			if edge[0] in contents or edge[1] in contents:
				self.Graph.remove_edge(edge[0], edge[1])

		# add the new action profile
		for edge in actionProfile:
			self.Graph.add_edge(edge[0], edge[1])

		self.updateUtility()
		self.Round += 1
	'''

	def playGame(self):

		self.Round = 0
		self.printGameConstants()	
		self.printGameVariables()

		previous = None
		current = set(self.Graph.edges(self.contents()))

		publishers = self.publishers()

		count = 0
		while True:

			if previous == current:
				stationary_steps += 1
			else:
				stationary_steps = 0

			if stationary_steps > len(publishers):
				break

			count += 1
			previous = current
			print "Round " + str(count) + ":"	
			#self.playRound()
			self.playIndividualRound()
			self.printGameVariables()
			current = set(self.Graph.edges(self.contents()))

		print self.Attention
			

	def printGameConstants(self):
	
		print "Contents:" 
		print self.Class["content"]
		print "Publishers:"
		print self.Class["publisher"]
		print "Readers:"
		print self.Class["reader"]
		print
		print "Intrinsic values:"
		print self.Value
		print
		print "Followers:"
		for publisher in self.publishers():
			followers = self.Graph.neighbors(publisher)
			followers = set(followers)
			followers = followers.difference(set(self.contents()))
			followers = list(followers)
			followers.sort()
			print str(publisher) + ":" + str(followers)
		print

	def printGameVariables(self):

		print "Shared Contents:"
		for publisher in self.publishers():
			followers = self.Graph.neighbors(publisher)
			followers = set(followers)
			followers = followers.difference(set(self.readers()))
			followers = list(followers)
			followers.sort()
			print str(publisher) + ":" + str(followers)
		print
		print "Utility: " 
		print self.Utility
		print

	
	def pureNash(self):
		print "Pure Nash"
		print self.publishers()
		print self.contents()
		print self.readers()
		print self.Value
		c = self.contents()
		r = self.readers()
		print self.Value.lookup([r[0]], [c[0]])


		
