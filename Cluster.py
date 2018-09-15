# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 19:28:37 2018

@author: Mauro
"""
import numpy as np
class Cluster:
    
    #el cluster tiene nada mas que sus datos clusterisados, etiquetas y como se distribuyen los puntos en base el algoritmo de clustering
  
    diccionarioClustersYPuntos=None 
    labelX=None
    labelY=None
    data=None
    coefCorr=None
    distribucion=None
    cantClusters=None
    centros=None
    def __init__(self, datos,labelX=None,labelY=None,distribucion=None,numClusters=None,centros=None):
        self.data=datos #ya cambiados en base a una tecnica de clustering
        self.cantClusters=numClusters
        self.centros=centros
        self.diccionarioClustersYPuntos={}
        
        puntosClusters={i: np.where(distribucion == i)[0] for i in range(numClusters)} 
        self.diccionarioClustersYPuntos={i: sum(1 for x in puntosClusters[i]) for i in puntosClusters.keys()} 
        
      
        #lo anterior crea un diccionar con el numero de cluster como clave y todos los puntos como contenido
        #i es clave y el np.where es una lista por comprension
        #lo siguiente es un diccionario con los cluster y los puntos que tienen
        
        self.distribucion=distribucion
        
        correlacion=np.corrcoef(datos[:, 0],datos[:, 1])
        correlacionXY=float("{0:.5f}".format(correlacion[0,1])) #correlacion es una matriz de todo x con todo y, tiene 1 en la diagonal
        self.coefCorr=correlacionXY
        
        self.labelX=labelX
        self.labelY=labelY
         #self.figura=plot #esta figura se mostraria haciendo self.plot = FigureCanvasTkAgg(self.figura, master=top) en una interfaz
    def getData(self):
        return self.data
    
 

    
    def getCantPuntos(self,nombreCluster):
        return self.diccionarioClustersYPuntos[nombreCluster]
    
    
    def getNombresClusters(self):
        return self.diccionarioClustersYPuntos.keys() #retorna las labels para cada cluster
    
    def getClustersYPuntos(self):
        return self.diccionarioClustersYPuntos
    
    def getCantClusters(self):
        return self.cantClusters

    def getDistribucion(self):
        return self.distribucion
    
    
    def getCorrelacion(self):
        return self.coefCorr
    
    def getEtiquetaX(self):
        return self.labelX
    
    def getEtiquetaY(self):
        return self.labelY
    
    def getCenters(self):
        return self.centros