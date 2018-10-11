# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 00:47:13 2018

@author: Mauro
"""

class Cluster:

    ID=None
    diccPuntoID_Valores=None
    def __init__(self,clusterID,diccPuntoID_Valores):
        self.ID=clusterID
        self.diccPuntoID_Valores=diccPuntoID_Valores

    def getID(self):
        return self.ID

    def getDiccionarioPuntos(self):
        #este es un diccionario que tiene el punto y las coordenadas que lo representan (ej, plan 1988 materia 40 era el punto 37)
        #la entrada sera (37,[1988,40])
        return self.diccPuntoID_Valores


    def getCantidadPuntos(self):
        return len(self.diccPuntoID_Valores.keys())

    def getCantidadPuntosEnColumna(self,columna):
        suma=0
        for k in self.diccPuntoID_Valores.keys():
                val=self.diccPuntoID_Valores[k]
                if(val[0]==columna): #se obtiene la lista a partidar de la clave y se verifica que el primer elemento, que es columna, sea lo pedido
                    suma+=1
        return suma
