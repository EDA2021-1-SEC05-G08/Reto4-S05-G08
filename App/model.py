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


from os import access
from sys import path
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
from DISClib.ADT import orderedmap as om
from DISClib.ADT.graph import gr
from DISClib.Utils import error as error
import requests
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.ADT import stack
from prettytable import PrettyTable
from math import radians, cos, sin, asin, sqrt

#•••••••••••••••••••••••••••••••••••••••••
#   Inicializacion del analizador.
#•••••••••••••••••••••••••••••••••••••••••

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
            "noDirectedGraph": None,
            "directedGraph": None,
            "airportsFull": None,
            "routesFull": None,
            "worldCities": None,
            "airportDestinations": None,
            "directedGraphAdded": None,
            "cities": None,
            'paths': None
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

    analyzer["noDirectedGraph"] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000,
                                              comparefunction=None)

    analyzer["directedGraphAdded"] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=None)

    analyzer["citiesByASCII"] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=None)

    return analyzer

#•••••••••••••••••••••••••••••••••••••••••
#   Funciones de consulta.
#•••••••••••••••••••••••••••••••••••••••••

def reqSix(analyzer, departureCity, destinationCity):

        posibleDepartureCitiesList = me.getValue(mp.get(analyzer["citiesByASCII"], departureCity))
        posibleDestinationCitiesList = me.getValue(mp.get(analyzer["citiesByASCII"], destinationCity))

        print(f"\nThere are {lt.size(posibleDepartureCitiesList)} departure cities posibilities, this is the list:\n")

        departureCityPosition = 1
        for i in lt.iterator(posibleDepartureCitiesList):
                print(f"{departureCityPosition}. {i['city']}, {i['country']}, {i['lat']}, {i['lng']}")
                departureCityPosition += 1

        departureCityPosition = int(input("\nSelect one by number: "))
        departureCityMap = lt.getElement(posibleDepartureCitiesList, departureCityPosition)

        print(f"\nThere are {lt.size(posibleDestinationCitiesList)} destination cities posibilities, this is the list:\n")

        destinationCityPosition = 1
        for i in lt.iterator(posibleDestinationCitiesList):
                print(f"{destinationCityPosition}. {i['city']}, {i['country']}, {i['lat']}, {i['lng']}")
                destinationCityPosition += 1

        destinationCityPosition = int(input("\nSelect one by number: "))
        destinationCityMap = lt.getElement(posibleDestinationCitiesList, destinationCityPosition)

        departureCityLatitude = departureCityMap["lat"]
        departureCityLongitude = departureCityMap["lng"]

        destinationCityLatitude = destinationCityMap["lat"]
        destinationCityLongitude = destinationCityMap["lng"]

        acessToken = getAcessToken()

        APIData = {
                        "departureData": queryAPI(departureCityLatitude, departureCityLongitude, acessToken)["data"],
                        "destinatioData": queryAPI(destinationCityLatitude, destinationCityLongitude, acessToken)["data"]
                }

        path = None
        pathList = lt.newList("ARRAY_LIST")
        counter = 1

        if len(APIData["departureData"]) == 0:
                answer = "No airports found in departure city."
        
        elif len(APIData["destinatioData"]) == 0:
                answer = "No airports found in destination city."
        
        else: 
                departureAirportIATA = APIData["departureData"][0]["iataCode"]
                destinationAirportIATA = APIData["destinatioData"][0]["iataCode"]
                minimumCostPaths(analyzer, departureAirportIATA)
                path = minimumCostPath(analyzer, destinationAirportIATA)

                if path is not None:
                    pathlen = stack.size(path)
                    print('El camino es de longitud: ' + str(pathlen))
                    while (not stack.isEmpty(path)):
                        stop = stack.pop(path)
                        lt.addLast(pathList, stop)

                routeDistance = 0

                pathTable = PrettyTable([
                                                "Airport A",
                                                "Airport B",
                                                "Distance"
                                        ])

                while counter <= lt.size(pathList):
                        distancee = lt.getElement(pathList, counter)['weight']
                        routeDistance += distancee
                        pathTable.add_row(
                                                [
                                                        lt.getElement(pathList, counter)['vertexA'],
                                                        lt.getElement(pathList, counter)['vertexB'],
                                                        distancee
                                                ]
                                        )

                        counter += 1

                departureAirportLatitude = APIData["departureData"][0]["geoCode"]["latitude"]
                departureAirportLongitude = APIData["departureData"][0]["geoCode"]["longitude"]

                destinationAirportLatitude = APIData["destinatioData"][0]["geoCode"]["latitude"]
                destinationAirportLongitude = APIData["destinatioData"][0]["geoCode"]["longitude"]

                distanceBetweenDepartureCityAndDepartureAirport = haversine(departureAirportLatitude, departureAirportLongitude, departureCityLatitude, departureAirportLongitude)
                distanceBetweenDestinationCityAndDestinationAirport = haversine(destinationAirportLatitude, destinationAirportLongitude, destinationCityLatitude, departureCityLongitude)

                answer = f"\nDeparture Airport: {APIData['departureData'][0]['name']}\nDestination Airport: {APIData['destinatioData'][0]['name']}\n\nRuta:\n{pathTable}\n\nTotal route distance: {routeDistance} kilometers\nDistance between departure city and departure airport: {distanceBetweenDepartureCityAndDepartureAirport} miles\nDistance between destination city and destination airport: {distanceBetweenDestinationCityAndDestinationAirport}miles\n"

        return answer

#•••••••••••••••••••••••••••••••••••••••••
#   Funciones para añadir información al catalogo.
#•••••••••••••••••••••••••••••••••••••••••

def addAirporttFullRow(analyzer, row):

        """

                Añade cada fila del archivo "airports_full"
                como elemento a un arreglo que se encuentra
                como valor del analizador en la llave 
                "airportsFull".

        """

        list = analyzer["airportsFull"]
        lt.addLast(list, row)
        return analyzer

def addRoutesFullRow(analyzer, row):

        """

                Añade cada fila del archivo "routes_full"
                como elemento a un arreglo que se encuentra
                como valor del analizador en la llave 
                "routesFull".

        """

        list = analyzer["routesFull"]
        lt.addLast(list, row)
        return analyzer

def addworldCitiesRow(analyzer, row):

        """

                Añade cada fila del archivo "worldcities"
                como elemento a un arreglo que se encuentra
                como valor del analizador en la llave 
                "worldCities".

        """

        list = analyzer["worldCities"]
        lt.addLast(list, row)
        return analyzer

def addAirportDestinationkeys(analyzer, row):

        """

                Añade como llave el IATA de un aeropuerto a
                un mapa y como valor un arreglo vacio, donde
                se almacenará mas adelante en otra funcion
                los IATA de los aeropuertos a los que desde
                el aeropuerto que se encuentro en la llave se
                puede ir.

        """

        map = analyzer["airportDestinations"]   
        airportIATA = row["IATA"]
        mp.put(map, airportIATA, lt.newList("ARRAY_LIST"))

def addAirportDestinationValuesaAndConnections(analyzer, row):

        """

                Anañade 

        """

        map = analyzer["airportDestinations"]   
        departureAirportIATA = row["Departure"]
        destinationAirportIATA = row["Destination"]
        distance = float(row["distance_km"])
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

def addAirpotCommonDestination(analyzer, row):

        addedMap = analyzer["directedGraphAdded"]

        departureAirportIATA = row["Departure"]
        destinationAirportIATA = row["Destination"]

        if not mp.contains(addedMap, departureAirportIATA):
                mp.put(addedMap, departureAirportIATA, lt.newList("ARRAY_LIST"))

        if not mp.contains(addedMap, destinationAirportIATA):
                mp.put(addedMap, destinationAirportIATA, lt.newList("ARRAY_LIST"))

        distance = float(row["distance_km"])

        airportDestinationsMap = analyzer["airportDestinations"]

        departureAirportAirportDestinationsList = me.getValue(mp.get(airportDestinationsMap, departureAirportIATA))
        destinationAirportAirportDestinationsList = me.getValue(mp.get(airportDestinationsMap, destinationAirportIATA))
        
        graph = analyzer["noDirectedGraph"]

        if lt.isPresent(me.getValue(mp.get(addedMap, departureAirportIATA)), destinationAirportIATA) == 0 and lt.isPresent(me.getValue(mp.get(addedMap, destinationAirportIATA)), departureAirportIATA) == 0:

                if lt.isPresent(departureAirportAirportDestinationsList,  destinationAirportIATA) != 0 and lt.isPresent(destinationAirportAirportDestinationsList,  departureAirportIATA) != 0:
                        try:
                                if not gr.containsVertex(graph, departureAirportIATA):
                                        gr.insertVertex(graph, departureAirportIATA)
                                if not gr.containsVertex(graph, destinationAirportIATA):
                                        gr.insertVertex(graph, destinationAirportIATA)
                                gr.addEdge(graph, departureAirportIATA, destinationAirportIATA, distance)
                                lt.addLast(me.getValue(mp.get(addedMap, departureAirportIATA)), destinationAirportIATA)
                                lt.addLast(me.getValue(mp.get(addedMap, destinationAirportIATA)), departureAirportIATA)
                                return analyzer
                        except Exception as exp:
                                error.reraise(exp, 'model:addairpotcommondestination')

def addCity(analyzer, row):
        city = row["city_ascii"]
        map = analyzer["citiesByASCII"]

        mapCity = {
                        "city": row["city"],
                        "city_ascii": row["city_ascii"],
                        "lat": row["lat"],
                        "lng": row["lng"],
                        "country": row["country"],
                        "iso2": row["iso2"],
                        "iso3": row["iso3"],
                        "admin_name": row["admin_name"],
                        "capital": row["capital"],
                        "population": row["population"],
                        "id": row["id"]
                }

        if not mp.contains(map, city):
                mp.put(map, city, lt.newList("ARRAY_LIST"))
                lt.addLast(me.getValue(mp.get(map, city)), mapCity)
        else:
                lt.addLast(me.getValue(mp.get(map, city)), mapCity)

#•••••••••••••••••••••••••••••••••••••••••
#   Funciones para consultar la API.
#•••••••••••••••••••••••••••••••••••••••••

def getAcessToken():

        # https://docs.python-requests.org/en/latest/
        # https://developers.amadeus.com/self-service/apis-docs/guides/authorization-262

        url="https://test.api.amadeus.com/v1/security/oauth2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data ={
          "grant_type": "client_credentials", 
          "client_id": "R26UdEoEUobh9EpW6ECoCUA5QAOcr9Kz",
          "client_secret": "lIogqm05SknXsOA7"
        }

        r = requests.post('https://test.api.amadeus.com/v1/security/oauth2/token', headers=headers, data=data)

        return (r.json()["access_token"])

def queryAPI(latitude, longitude, acessToken):

        # https://developers.amadeus.com/self-service/category/air/api-doc/airport-nearest-relevant/api-reference

        access_token = acessToken
        headers = {"Authorization": "Bearer " + access_token}
        params = {
          "latitude": float(latitude),
          "longitude": float(longitude),
          "radius": 500
        }

        r = requests.get('https://test.api.amadeus.com/v1/reference-data/locations/airports', headers=headers, params=params)

        #print(r.text)     #Solo para imprimir
        return (r.json()) #Para procesar

#•••••••••••••••••••••••••••••••••••••••••
#   Funciones adicionales.
#•••••••••••••••••••••••••••••••••••••••••

def minimumCostPaths(analyzer, initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    analyzer['paths'] = djk.Dijkstra(analyzer["directedGraph"], initialStation)

def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(analyzer['paths'], destStation)
    return path

def haversine(lat1, lon1, lat2, lon2): 
        lat1 = float(lat1)
        lon1 = float(lon1)
        lat2 = float(lat2)
        lon2 = float(lon2)
        R = 3959.87433 # this is in miles. For Earth radius in kilometers use 6372.8 km
        dLat = radians(lat2 - lat1)
        dLon = radians(lon2 - lon1)
        lat1 = radians(lat1)
        lat2 = radians(lat2)
        a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
        c = 2*asin(sqrt(a)) 
        return R * c

