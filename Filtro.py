# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 23:48:37 2018

@author: tomy-
"""

from abc import ABCMeta, abstractmethod #para la creación de clases abstractas

class FiltroDataframe:
    __metaclass__ = ABCMeta #Clase abstracta

    @abstractmethod
    def cumple(self, dataframe): pass

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"


class FiltroSimple(FiltroDataframe):
    __metaclass__ = ABCMeta #Clase abstracta
    columna = ''
    valor = 0

    def __init__(self, columna, valor):
        self.columna = columna
        self.valor = valor

    def setColumna(self, columna):
        self.columna = columna

    def setValor(self, valor):
        self.valor = valor

    def getColumna(self):
        return self.columna

    def getValor(self):
        return self.valor

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"


class FiltroMayor(FiltroSimple):

    def cumple(self, dataframe):
        return dataframe[self.getColumna()] > self.getValor()

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"


class FiltroMenor(FiltroSimple):

    def cumple(self, dataframe):
        return dataframe[self.getColumna()] < self.getValor()

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"


class FiltroIgual(FiltroSimple):

    def cumple(self, dataframe):
        return dataframe[self.getColumna()] == self.getValor()
    

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"
class FiltroNoIgual(FiltroSimple):

    def cumple(self, dataframe):
        return dataframe[self.getColumna()] != self.getValor()
    

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"
class FiltroNOT(FiltroDataframe):
    filtro = None

    def __init__(self, filtro):
        self.filtro = filtro

    def cumple(self, dataframe):
        return ~(self.filtro.cumple(dataframe))

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"


class FiltroCompuesto(FiltroDataframe):
    __metaclass__ = ABCMeta #Clase abstracta
    f1 = None
    f2 = None

    def __init__(self, f1, f2):
        self.f1 = f1
        self.f2 = f2

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"


class FiltroAND(FiltroCompuesto):

    def cumple(self, dataframe):
        return self.f1.cumple(dataframe) & self.f2.cumple(dataframe)

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"


class FiltroOR(FiltroCompuesto):

    def cumple(self, dataframe):
        return self.f1.cumple(dataframe) | self.f2.cumple(dataframe)