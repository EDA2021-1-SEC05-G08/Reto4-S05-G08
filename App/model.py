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
    
    analyzer = mp.newMap(
                        5,
                        maptype = "CHAINING",
                        loadfactor = 4.0,
                        comparefunction = None
                    )

    mp.put(
            analyzer,
            "cases",
            lt.newList(
                        'ARRAY_LIST'
                        )
            )

    mp.put(
            analyzer,
            "casesSize",
            lt.size(
                    me.getValue(
                                mp.get(
                                        analyzer, "cases"
                                    )
                                )
                    ) 
            )

    mp.put(
            analyzer,
            "casesByCity",
            om.newMap(  
                        omaptype='RBT',
                        comparefunction=None
                    )
            )

    mp.put(
            analyzer,
            "casesBySeconds",
            om.newMap(  
                        omaptype='RBT',
                        comparefunction=None
                        )
            )

    mp.put(
            analyzer,
            "casesByHour",
            om.newMap(  
                        omaptype='RBT',
                        comparefunction=None
                    )
            )

    return analyzer

def loadData(analyzer):

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

    return None