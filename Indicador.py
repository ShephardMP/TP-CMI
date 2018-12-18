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
class IndicadorParametrizado(Indicador):
    __metaclass__ = ABCMeta #Clase abstracta

    listaParametros=None
    @abstractmethod
    def __init__(self, nombre):
          super().__init__(nombre)


    @abstractmethod
    def evaluarCluster(self,cluster):
        pass


    def setParametros(self,listaParametros):
        self.listaParametros=listaParametros

class IndicadorGlobal(Indicador):
    __metaclass__ = ABCMeta #Clase abstracta

    clustering=None

    @abstractmethod
    def __init__(self, nombre):
          super().__init__(nombre)


    @abstractmethod
    def evaluarCluster(self,cluster):
        pass


    def setClustering(self,clustering):
        self.clustering=clustering

    def getClustering(self):
        return self.clustering

#---------------------------------FIN DEF ABSTRACTAS-----------------------------#



class IndicadorCantPuntos(Indicador):

     def __init__(self, nombre):
         super().__init__(nombre)

     def evaluarCluster(self,cluster):

        return cluster.getCantidadPuntos()


class IndicadorMediaX(Indicador):

     def __init__(self, nombre):
         super().__init__(nombre)

     def evaluarCluster(self,cluster):

        return cluster.getMedia()[0]

class IndicadorMediaY(Indicador):

     def __init__(self, nombre):
         super().__init__(nombre)

     def evaluarCluster(self,cluster):

        return cluster.getMedia()[1]

class IndicadorColoreo(Indicador):
    #indicador pensado para colorear los clusters
     def __init__(self, nombre):
         super().__init__(nombre)

     def evaluarCluster(self,cluster):

        return cluster.getMedia()[1]+cluster.getMedia()[0]

class IndicadorColumnasAbarcadas(Indicador):
     def __init__(self, nombre):
         super().__init__(nombre)

     def evaluarCluster(self,cluster):

        return cluster.getColumnasAbarcadas()

class IndicadorVolumen(Indicador):
    def __init__(self, nombre):
        super().__init__(nombre)

    def evaluarCluster(self,cluster):

       return cluster.getVolumen()


class IndicadorCantPuntosEnColumna(IndicadorParametrizado):

    columna=None
    def __init__(self, nombre):
         super().__init__(nombre)

    def evaluarCluster(self,cluster):
         if(self.columna is None):
             raise ValueError("columna no seteada")
         return cluster.getCantidadPuntosEnColumna(self.columna)

    def setParametros(self,listaParametros):
         if(len(listaParametros)!=1):
             raise ValueError("indicador espera solo un parametro")
         self.columna=listaParametros[0]



class IndicadorCantPuntosEnFila(IndicadorParametrizado):
    #es bastante similar al de columna, pero no se justifica otro nivel de abstraccion por solo dos ejemplos
    fila=None
    def __init__(self, nombre):
         super().__init__(nombre)

    def evaluarCluster(self,cluster):
         if(self.fila is None):
             raise ValueError("fila no seteada")
         return cluster.getCantidadPuntosEnFila(self.fila)

    def setParametros(self,listaParametros):
         if(len(listaParametros)!=1):
             raise ValueError("indicador espera solo un parametro")
         self.fila=listaParametros[0]




class IndicadorProporcionDelCluster(IndicadorGlobal):
    #puntos cluster/total puntos
     def __init__(self, nombre):
         super().__init__(nombre)

     def evaluarCluster(self,cluster):

        return cluster.getCantidadPuntos()/self.getClustering().getTotalPuntos()


class IndicadorPorcentajeDePuntosEnColumna(IndicadorGlobal,IndicadorParametrizado):



    def __init__(self, nombre):
         super().__init__(nombre)

    def evaluarCluster(self,cluster):
         if(self.listaParametros is None):
             raise ValueError("parametros no seteados")
         columna=self.listaParametros[0]
         return 100*cluster.getCantidadPuntosEnColumna(columna)/self.getClustering().getCantPuntosColumna(columna) #lo del cluster/ el total

class IndicadorPorcentajeDePuntosEnFila(IndicadorGlobal,IndicadorParametrizado):



    def __init__(self, nombre):
         super().__init__(nombre)

    def evaluarCluster(self,cluster):
         if(self.listaParametros is None):
             raise ValueError("parametros no seteados")
         fila=self.listaParametros[0]
         return 100*cluster.getCantidadPuntosEnFila(fila)/self.getClustering().getCantPuntosFila(fila) #lo del cluster/ el total
