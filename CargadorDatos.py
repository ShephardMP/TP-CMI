# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 23:44:58 2018

@author: tomy-
"""

from abc import ABCMeta, abstractmethod #para la creación de clases abstractas
import pandas as pandas #biblioteca para trabajar con data frames

class CargadorDatos:
    __metaclass__ = ABCMeta #Clase abstracta

    @abstractmethod
    def cargarArchivo(self, nombreArchivo): pass #Retorna un dataframe

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"


class CargadorDatosExcel(CargadorDatos):
    "Carga los datos desde un archivo .xlsx"

    def cargarArchivo(self, nombreArchivo):
        return pandas.read_excel(nombreArchivo)