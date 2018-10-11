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
        
        