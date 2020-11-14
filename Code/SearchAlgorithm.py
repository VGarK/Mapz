# This file contains all the required routines to make an A* search algorithm.
#
__authors__ = 'TO_BE_FILLED'
__group__ = 'DL01'
# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Grau en Enginyeria Informatica
# Curs 2018- 2019
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________

from SubwayMap import *
import math


class Node:
	# __init__ Constructor of Node Class.
	def __init__(self, station, father):
		"""
		__init__: 	Constructor of the Node class
		:param
				- station: STATION information of the Station of this Node
				- father: NODE (see Node definition) of his father
		"""

		self.station = station  # STATION information of the Station of this Node
		self.father = father  # NODE pointer to his father

		if father == None:
			self.parentsID = []
		else:
			self.parentsID = [father.station.id]
			self.parentsID.extend(father.parentsID)  # TUPLE OF NODES (from the origin to its father)

		self.g = 0  # REAL cost - depending on the type of preference -
		# to get from the origin to this Node
		self.h = 0  # REAL heuristic value to get from the origin to this Node
		self.f = 0  # REAL evaluate function
		self.time = 0  # REAL time required to get from the origin to this Node
		# [optional] Only useful for GUI
		self.num_stopStation = 0  # INTEGER number of stops stations made from the origin to this Node
		# [optional] Only useful for GUI
		self.walk = 0  # REAL distance made from the origin to this Node
		# [optional] Only useful for GUI
		self.transfers = 0  # INTEGER number of transfers made from the origin to this Node
		# [optional] Only useful for GUI

	def setEvaluation(self):
		"""
		setEvaluation: 	Calculates the Evaluation Function. Actualizes .f value

		"""
		self.f = self.g + self.h

	def setHeuristic(self, typePreference, station_destination, city):
		""""
		setHeuristic: 	Calculates the heuristic depending on the preference selected
		:params
				- typePreference: INTEGER Value to indicate the preference selected:
								0 - Null Heuristic
								1 - minimum Time
								2 - minimum Distance
								3 - minimum Transfers
								4 - minimum Stops
				- station_destination: destination station
				- city: CITYINFO with the information of the city (see CityInfo class definition)
		"""
		if typePreference == 1:
			if self.station.id != station_destination.station.id:
				print(self.station.name)
				print(city.StationList[self.station.id-1].destinationDic)
				self.h = min(city.StationList[self.station.id-1].destinationDic.values())
			else:
				self.h = 0

		elif typePreference == 2:
			self.h = (self.station.x - station_destination.station.x)**2 + (self.station.y - station_destination.station.y)**2

		elif typePreference == 3:
			if self.station.line != station_destination.station.line:
				self.h = 1
			else:
				self.h = 0

		elif typePreference == 4:
			if self.station.line == station_destination.station.line:
				self.h = abs(self.station.id - station_destination.station.id)
			elif self.station.name != station_destination.station.name:
				self.h = 1
			else:
				self.h = 0



	def setRealCost(self, costTable, timeCostTable, distanceCostTable, transfersCostTable, stopsCostTable):
		"""
		setRealCost: 	Calculates the real cost depending on the preference selected
		:params
				 - costTable: DICTIONARY. Relates each station with their adjacency an their real cost. NOTE that this
							 cost can be in terms of any preference.
		"""
		self.g = self.father.g + costTable[self.station.id][self.father.station.id]
		self.time =  self.father.time + timeCostTable[self.station.id][self.father.station.id]
		self.walk= self.father.walk + distanceCostTable[self.station.id][self.father.station.id]
		self.transfers = self.father.transfers + transfersCostTable[self.station.id][self.father.station.id]
		self.num_stopStation = self.father.num_stopStation + stopsCostTable[self.station.id][self.father.station.id]

def coord2station(coord, stationList):
	"""
	coord2station :	  From coordinates, it searches the closest station.
	:param
			- coord:  LIST of two REAL values, which refer to the coordinates of a point in the city.
			- stationList: LIST of the stations of a city. (- id, destinationDic, name, line, x, y -)

	:return:
			- possible_origins: List of the Indexes of the StationList structure, which corresponds to the closest
			station
	"""
	minimum=[]
	distMin=float("inf")
	for i, station in enumerate(stationList):
		distStation=(station.x-coord[0])**2+(station.y-coord[1])**2
		if distStation<distMin:
			minimum=[i]
			distMin=distStation
		elif distStation==distMin:
			minimum.append(i)
	return minimum


def Expand(fatherNode, city, station_destination=None, typePreference=0, costTable=None, timeCostTable=None, distanceCostTable=None, transfersCostTable=None, stopsCostTable=None):
	"""
		Expand: It expands a node and returns the list of connected stations (childrenList)
		:params
				- fatherNode: NODE of the current node that should be expanded
				- city: CITYINFO with the information of the city (see CityInfo class definition)
				- station_destination: Station (see Station definition) of the destination
				- typePreference: INTEGER Value to indicate the preference selected:
								0 - Null Heuristic
								1 - minimum Time
								2 - minimum Distance
								3 - minimum Transfers
								4 - minimum Stops
				- costTable: DICTIONARY. Relates each station with their adjacency an their real cost. NOTE that this
							 cost can be in terms of any preference.

		:returns
				- childrenList:  LIST of the set of child Nodes for this current node (fatherNode)

	"""
	import math

	children=fatherNode.station.destinationDic.keys()
	childrenList=list(map(lambda x: Node(city.StationList[x-1], fatherNode), children))
	for child in childrenList:
		child.setHeuristic(typePreference, station_destination, city)
		child.setRealCost(costTable, timeCostTable, distanceCostTable, transfersCostTable, stopsCostTable)
		child.setEvaluation()
	return childrenList



def RemoveCycles(childrenList):
	"""
		RemoveCycles: It removes from childrenList the set of childrens that include some cycles in their path.
		:params
				- childrenList: LIST of the set of child Nodes for a certain Node
		:returns
				- listWithoutCycles:  LIST of the set of child Nodes for a certain Node which not includes cycles
	"""
	return list(filter(lambda y:sorted(list(set(list(map(lambda x: x.station.id, (lambda a:lambda v:a(a,v))(lambda s,x: x[1:] if x[0]==None else s(s, [x[0].father]+x))([y]))))))==sorted(list(map(lambda x: x.station.id, (lambda a:lambda v:a(a,v))(lambda s,x: x[1:] if x[0]==None else s(s, [x[0].father]+x))([y])))), childrenList)) #One Line to rule them all, One Line to find them, One Line to bring them all, and in the darkness bind them



def RemoveRedundantPaths(childrenList, nodeList, partialCostTable):
	"""
		RemoveRedundantPaths:   It removes the Redundant Paths. They are not optimal solution!
								If a node is visited and have a lower g in this moment, TCP is updated.
								In case of having a higher value, we should remove this child.
								If a node is not yet visited, we should include to the TCP.
		:params
				- childrenList: LIST of NODES, set of childs that should be studied if they contain rendundant path
								or not.
				- nodeList : LIST of NODES to be visited
				- partialCostTable: DICTIONARY of the minimum g to get each key (station id) from the origin Node
		:returns
				- childrenList: LIST of NODES, set of childs without rendundant path.
				- nodeList: LIST of NODES to be visited updated (without redundant paths)
				- partialCostTable: DICTIONARY of the minimum g to get each key (station id) from the origin Node (updated)
	"""
	def gen_parents(node):
		while node:
			yield node
			node = node.father
	newChildrenList=[]
	for child in childrenList:
		if child.station.id in partialCostTable and child.g<partialCostTable[child.station.id]:
			partialCostTable[child.station.id]=child.g
			nodeList=list(filter(lambda x: child.station.id not in [y.station.id for y in gen_parents(x)], nodeList))
		elif child.station.id in partialCostTable and child.g>partialCostTable[child.station.id]:
			continue
		elif child.station.id not in partialCostTable:
			partialCostTable[child.station.id]=child.g
		newChildrenList.append(child)
	return newChildrenList, nodeList, partialCostTable



def sorted_insertion(nodeList, childrenList):
	""" Sorted_insertion: 	It inserts each of the elements of childrenList into the nodeList.
							The insertion must be sorted depending on the evaluation function value.

		: params:
			- nodeList : LIST of NODES to be visited
			- childrenList: LIST of NODES, set of childs that should be studied if they contain rendundant path
								or not.
		:returns
				- nodeList: sorted LIST of NODES to be visited updated with the childrenList included
	"""
	return sorted(nodeList+childrenList, key=lambda x: x.f)


def setCostTable(typePreference, city):
	"""
	setCostTable :	  Real cost of a travel.
	:param
			- typePreference: INTEGER Value to indicate the preference selected:
								0 - Adjacency
								1 - minimum Time
								2 - minimum Distance
								3 - minimum Transfers
								4 - minimum Stops
			- city: CITYINFO with the information of the city (see CityInfo class definition)
	:return:
			- costTable: DICTIONARY. Relates each station with their adjacency an their g, depending on the
								 type of Preference Selected.
	"""
	mydic = {}
	for i in city.StationList:
		mydic[i.id] = {}
	if typePreference == 1:
		return dict(zip(range(1, len(city.StationList)+1), list(map(lambda x: x.destinationDic, city.StationList))))
	elif typePreference == 2:
		for i in mydic:
			for j in city.StationList[i-1].destinationDic:
				mydic[i][city.StationList[j-1].id] = ((city.StationList[j-1].x-city.StationList[i-1].x)**2+(city.StationList[j-1].y-city.StationList[i-1].y)**2)
		return mydic

	elif typePreference == 3:
		for i in mydic:
			for j in city.StationList[i-1].destinationDic:
				if city.StationList[j-1].line != city.StationList[i-1].line:
					mydic[i][city.StationList[j-1].id] = 1
				else:
					mydic[i][city.StationList[j-1].id] = 0
		return mydic
	elif typePreference == 4:
		for i in mydic:
			for j in city.StationList[i-1].destinationDic:
				if city.StationList[j-1].line != city.StationList[i-1].line:
					mydic[i][city.StationList[j-1].id] = 0
				else:
					mydic[i][city.StationList[j-1].id] = 1
		return mydic




def AstarAlgorithm(coord_origin, coord_destination, typePreference, city, flag_redundants):
	"""
	 AstarAlgorithm: main function. It is the connection between the GUI and the AStar search code.
	 INPUTS:
			- stationList: LIST of the stations of a city. (- id, name, destinationDic, line, x, y -)
			- coord_origin: TUPLE of two values referring to the origin coordinates
			- coord_destination: TUPLE of two values referring to the destination coordinates
			- typePreference: INTEGER Value to indicate the preference selected:
								0 - Adjacency
								1 - minimum Time
								2 - minimum Distance
								3 - minimum Transfers
								4 - minimum Stops
			- city: CITYINFO with the information of the city (see CityInfo class definition)
			- flag_redundants: [0/1]. Flag to indicate if the algorithm has to remove the redundant paths (1) or not (0)

	OUTPUTS:
			- time: REAL total required time to make the route
			- distance: REAL total distance made in the route
			- transfers: INTEGER total transfers made in the route
			- stopStations: INTEGER total stops made in the route
			- num_expanded_nodes: INTEGER total expanded nodes to get the optimal path
			- depth: INTEGER depth of the solution
			- visitedNodes: LIST of INTEGERS, IDs of the stations corresponding to the visited nodes
			- idsOptimalPath: LIST of INTEGERS, IDs of the stations corresponding to the optimal path
			(from origin to destination)
			- min_distance_origin: REAL the distance of the origin_coordinates to the closest station
			- min_distance_destination: REAL the distance of the destination_coordinates to the closest station



			EXAMPLE:
			return optimalPath.time, optimalPath.walk, optimalPath.transfers,optimalPath.num_stopStation,
			len(expandedList), len(idsOptimalPath), visitedNodes, idsOptimalPath, min_distance_origin,
			min_distance_destination
	"""
	typePreference = int(typePreference)
	paths = []
	visitedNodes = []
	costTable = setCostTable(typePreference, city)
	timeCostTable = setCostTable(1, city)
	distanceCostTable = setCostTable(2, city)
	transfersCostTable = setCostTable(3, city)
	stopsCostTable = setCostTable(4, city)
	possible_origins = coord2station(coord_origin, city.StationList)
	distStationOrigin=math.sqrt((city.StationList[possible_origins[0]].x-coord_origin[0])**2+(city.StationList[possible_origins[0]].y-coord_origin[1])**2)
	destination = coord2station(coord_destination, city.StationList)
	destination = city.StationList[destination[0]]
	distStationDest=math.sqrt((destination.x-coord_destination[0])**2+(destination.y-coord_destination[1])**2)
	expanded_nodes=0;
	for i in possible_origins:
		paths.append(Node(city.StationList[i], None))
	while len(paths) > 0 and paths[0].station.id != destination.id:
		C = paths[0]
		visitedNodes.append(C.station.id)
		E = Expand(C, city, Node(destination, None), typePreference, costTable, timeCostTable, distanceCostTable, transfersCostTable, stopsCostTable)
		expanded_nodes+=len(E)
		E = RemoveCycles(E)
		if flag_redundants:
			E = RemoveRedundantPaths(E, paths, {})[0]
		paths = sorted_insertion(E, paths[1:])
	idsOptimalPath = (list(map(lambda x: x.station.id, (lambda a:lambda v:a(a,v))(lambda s,x: x[1:] if x[0]==None else s(s, [x[0].father]+x))([paths[0]]))))
	return paths[0].time, paths[0].walk, paths[0].transfers,paths[0].num_stopStation,expanded_nodes,len(idsOptimalPath),visitedNodes,idsOptimalPath,distStationOrigin,distStationDest
