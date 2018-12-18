# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 00:47:13 2018

@author: Mauro
"""

class Cluster:

    ID=None
    diccPuntoID_Valores=None
    media=None
    def __init__(self,clusterID,diccPuntoID_Valores,centro):
        self.ID=clusterID
        self.diccPuntoID_Valores=diccPuntoID_Valores
        self.media=centro

    def getID(self):
        return self.ID


    def getMedia(self):
        return self.media
    def getDiccionarioPuntos(self):
        #este es un diccionario que tiene el punto y las coordenadas que lo representan (ej, plan 1988 materia 40 era el punto 37)
        #la entrada sera (37,[1988,40])
        return self.diccPuntoID_Valores


    def getCantidadPuntos(self):
        return len(self.diccPuntoID_Valores.keys())

    def getColumnasAbarcadas(self):
        aux=[]
        for k in self.diccPuntoID_Valores.keys():
            val=self.diccPuntoID_Valores[k][0] #la primera dimension por alguna razon es columnas
            if val not in aux:
                aux.append(val)

        return len(aux)

    def getVolumen(self):
        return self.getCantidadPuntos()/self.getColumnasAbarcadas()


    def getCantidadPuntosEnAxis(self,axis=0,valorAxis=0): #axis=0 es columnas, axis=1 es filas
        suma=0
        for k in self.diccPuntoID_Valores.keys():
                val=self.diccPuntoID_Valores[k]
                if(val[axis]==valorAxis): #se obtiene la lista a partidar de la clave y se verifica que el primer elemento, que es columna, sea lo pedido
                    suma+=1
        return suma

    def getCantidadPuntosEnColumna(self,columna):
        return self.getCantidadPuntosEnAxis(0,columna)

    def getCantidadPuntosEnFila(self,fila):
        return self.getCantidadPuntosEnAxis(1,fila)
