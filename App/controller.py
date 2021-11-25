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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

def newAnalyzer():
    return model.newAnalyzer()

def loadData(analyzer, airportsFullFile, routesFullFile, worldCitiesFile):
    
    airportsFullFile = cf.data_dir + airportsFullFile
    airportsFullFile = csv.DictReader(open(airportsFullFile, encoding="utf-8"), delimiter=",")

    routesFullFile = cf.data_dir + routesFullFile
    routesFullFile = csv.DictReader(open(routesFullFile, encoding="utf-8"), delimiter=",")

    worldCitiesFile = cf.data_dir + worldCitiesFile
    worldCitiesFile = csv.DictReader(open(worldCitiesFile, encoding="utf-8"), delimiter=",")

    for row in airportsFullFile:
        model.addAirporttFullRow(analyzer, row)
        model.addAirport(analyzer, row)
        model.addAirportDestinationkeys(analyzer, row)
        

    for row in routesFullFile:
        model.addRoutesFullRow(analyzer, row)
        model.addAirportDestinationValuesaAndConnections(analyzer, row)

    for row in worldCitiesFile:
        model.addworldCitiesRow(analyzer, row)

    return analyzer