# With this exercise we will work on finding a station of the path given certain coordinates
#
__authors__='TO_BE_FILLED'
__group__='DL01'
# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Grau en Enginyeria Informatica
# Curs 2018- 2019
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________

from SearchAlgorithm import *
from SubwayMap import *
import os

def main():


    #------------------------------------------------------------------#
    city_string="Lyon_smallCity"

    filename = os.path.join(os.path.dirname(__file__), "..", "CityInformation", city_string, "Stations.txt")
    stationList = readStationInformation(filename)


    filename = os.path.join(os.path.dirname(__file__), "..", "CityInformation", city_string, "Time.txt")
    timeStations = readCostTable(filename)


    # Now we want to analyze extra information from the files.
    # Velocity of the lines
    filename = os.path.join(os.path.dirname(__file__), "..", "CityInformation", city_string, "InfoVelocity.txt")
    infoVelocity = readInformation(filename)


    # we save the global information of the city in 'city' variable.
    # Analyze which information contains an element of the class CityInfo.
    city = CityInfo(infoVelocity, stationList, timeStations)



    #------------------------------------------------------------------#

    origin=Node(stationList[1],None)            # Charpennes L1
    destination=Node(stationList[4],None)


    #------------------------------------------------------------------#
    # Creeu una funció on donat un node d'origen, un node desti i la informació de la ciutat segueixi un algoritme de cerca basic (el descrit a l'exercici 5)
    # i mostreu quin es el cami que proposa des de una estació d'origen fins a una de desti.

    cami=expansio(origin,destination,city)
    print(cami)
    print(" Current: [" + str(cami.station.id) + "] " + cami.station.name + " L" + str(cami.station.line))
    for i in cami.parentsID:
        nodee=Node(stationList[i-1],None)
        print(nodee.station.name + " " + str(nodee.station.line))


def expansio(Node_origen,node_desti, city):
    node_cami=[]
    node_cami.append(Node_origen)
    node_actual=node_cami[-1]
    while(node_actual.station.id != node_desti.station.id):


        node_cami.remove(node_actual)

        childrenList=Expand(node_actual,city)
        childrenList=RemoveCycles(childrenList)
        for x in childrenList:
            node_cami.append(x)
        node_actual = node_cami[-1]

    return node_cami[-1]










if __name__ == '__main__':
    main()