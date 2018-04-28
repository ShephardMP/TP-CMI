# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 19:28:37 2018

@author: Mauro
"""

class Cluster:
    figura=None #de tipo matplotlib.figure
    diccionarioClustersYPuntos=None 
    diccionarioClustersYColores=None
    
    coefCorr=None
    #es un diccionario que tiene como clave el label del cluster 
    #(ej: cluster A) y la cantidad de puntos que tiene
    def __init__(self, plot,coefCorr,diccLabelsXCantidadPuntos=None,diccLabelsXColores=None):
        self.diccionarioClustersYColores={}
        self.diccionarioClustersYPuntos={}
        self.figura=plot #esta figura se mostraria haciendo self.plot = FigureCanvasTkAgg(self.figura, master=top) en una interfaz
        self.diccionarioClustersYPuntos=diccLabelsXCantidadPuntos
        self.diccionarioClustersYColores=diccLabelsXColores
        self.coefCorr=coefCorr
    def getFigura(self):
        return self.figura
    
    
    def getCantPuntos(self,nombreCluster):
        return self.diccionarioClustersYPuntos[nombreCluster]
    
    
    def getNombresClusters(self):
        return self.diccionarioClustersYPuntos.keys() #retorna las labels para cada cluster
    
    def getClustersYPuntos(self):
        return self.diccionarioClustersYPuntos
    
    def getClustersYColores(self):
        return self.diccionarioClustersYColores
    def getCorrelacion(self):
        return self.coefCorr