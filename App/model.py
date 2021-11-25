"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
from DISClib.ADT import orderedmap as om
from DISClib.ADT.graph import gr
from DISClib.Utils import error as error

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

def newAnalyzer():

    """ 
        Inicializa el analizador.
        Crea un nuevo Map para cargar el archivo, dentro de este se
        crea una lista vacia para cargar alli todos los casos de
        avistamientos. También, crea indices para la busqueda de los
        avistamientos por criterios de casos por ciudad, casos por
        duración de segundos y casos por hora de avistamiento, los datos
        se indicarán en los indices dentro de un Map de tipo RBT. 
        Retorna el analizador inicializado.
    """
    
    analyzer = {
            "airportsFull": None,
            "routesFull": None,
            "worldCities": None,
            "airportDestinations": None,
            "directedGraph": None
    }
    
    analyzer["airportsFull"] = lt.newList("ARRAY_LIST")
    analyzer["routesFull"] = lt.newList("ARRAY_LIST")
    analyzer["worldCities"] = lt.newList("ARRAY_LIST")

    analyzer["airportDestinations"] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=None)
    
    analyzer["directedGraph"] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=None)

    return analyzer


def addAirporttFullRow(analyzer, row):
        list = analyzer["airportsFull"]
        lt.addLast(list, row)
        return analyzer

def addRoutesFullRow(analyzer, row):
        list = analyzer["routesFull"]
        lt.addLast(list, row)
        return analyzer

def addworldCitiesRow(analyzer, row):
        list = analyzer["worldCities"]
        lt.addLast(list, row)
        return analyzer


def addAirportDestinationkeys(analyzer, row):
        map = analyzer["airportDestinations"]   
        airportIATA = row["IATA"]
        mp.put(map, airportIATA, lt.newList("ARRAY_LIST"))

def addAirportDestinationValuesaAndConnections(analyzer, row):
        map = analyzer["airportDestinations"]   
        departureAirportIATA = row["Departure"]
        destinationAirportIATA = row["Destination"]
        distance = row["distance_km"]
        list = me.getValue(mp.get(map, departureAirportIATA))
        if lt.isPresent(list, destinationAirportIATA) == 0:
                lt.addLast(list, destinationAirportIATA)
                gr.addEdge(analyzer['directedGraph'], departureAirportIATA, destinationAirportIATA, distance)


def addAirport(analyzer,row):
        graph = analyzer["directedGraph"]
        airportIATA = row["IATA"]
        try:
                if not gr.containsVertex(graph, airportIATA):
                        gr.insertVertex(graph, airportIATA)
                return analyzer
        except Exception as exp:
                error.reraise(exp, 'model:addairport') 
