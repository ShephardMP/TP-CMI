# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 01:16:49 2018

@author: Mauro
"""
from abc import ABCMeta, abstractmethod
class Indicador:
    #pensado para usar como un patron visitor
    nombre=None
    __metaclass__ = ABCMeta #Clase abstracta

    @abstractmethod
    def __init__(self, nombre):
         self.nombre=nombre

    def getNombreIndicador(self):
         return self.nombre


    @abstractmethod
    def evaluarCluster(self,cluster):
         #el cluster es de tipo Cluster y debiera tener metodos que permitieran extraer info.
         #el indicador debiera ser de cada cluster y no de todos, ya que eso corresponde a una metrica global
         #el mas simple es por cantidad de puntos aunque puede haber otros por error cuadratico
         #o por cantidad de puntos en determinada categoria(columna)

         #es decir este metodo debiera siempre retornar un valor discernible, sea int float etc.
        pass


class IndicadorCantPuntos(Indicador):

     def __init__(self, nombre):
         super().__init__(nombre)

     def evaluarCluster(self,cluster):

        return cluster.getCantidadPuntos()


class IndicadorCantPuntosEnColumna(Indicador):

     columna=3
     def __init__(self, nombre,col):
         super().__init__(nombre)
         self.columa=col

     def evaluarCluster(self,cluster):

        return cluster.getCantidadPuntosEnColumna(self.columa)
