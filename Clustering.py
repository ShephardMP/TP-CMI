# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 19:28:37 2018

@author: Mauro
"""
import numpy as np
from Cluster import Cluster
class Clustering:

    #el cluster tiene nada mas que sus datos clusterisados, etiquetas y como se distribuyen los puntos en base el algoritmo de clustering

    diccionarioClustersYPuntos=None
    labelX=None
    labelY=None
    data=None
    coefCorr=None
    distribucion=None
    cantClusters=None
    centros=None
    puntosClusters=None
    clusters=None
    rangos=None #esto es por el escalado de la data, quisiera mantener los valores originales para ploteo e info estadistica. Es una lista
    totalPuntos=None
    def __init__(self, datos,labelX=None,labelY=None,distribucion=None,numClusters=None,centros=None,rangos=None):
        self.data=datos #ya cambiados en base a una tecnica de clustering
        self.cantClusters=numClusters
        self.centros=centros
        self.diccionarioClustersYPuntos={}
        self.rangos=rangos
        self.puntosClusters={i: np.where(distribucion == i)[0] for i in range(numClusters)} #diccionario con clave i que tiene como valor un array de todos los puntos que fueron labeleados con i (ej, cluster 0)

        self.clusters=[]
        for i in range(numClusters):
            self.clusters.append(Cluster(i,{p : self.data[p] for p in self.puntosClusters[i] },self.centros[i]))

       # print("clusters {}".format(self.clusters[0].getDiccionarioPuntos().items()))

        #self.diccionarioClustersYPuntos={i: sum(1 for x in self.puntosClusters[i]) for i in self.puntosClusters.keys()}
        self.diccionarioClustersYPuntos={i:self.clusters[i].getCantidadPuntos() for i in range(numClusters)}

        self.totalPuntos=sum([self.diccionarioClustersYPuntos[i] for i in range(numClusters)])

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


    def getTotalPuntos(self):
        return self.totalPuntos

    def getCantPuntosCluster(self,nombreCluster):
        return self.diccionarioClustersYPuntos[nombreCluster]

    def getCantPuntosColumna(self,columna):

        return sum(x.getCantidadPuntosEnColumna(columna) for x in self.clusters)

    def getCantPuntosFila(self,fila):
        return sum(x.getCantidadPuntosEnFila(fila) for x in self.clusters)

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

    def getRangos(self):
        return self.rangos
    def getOrdenClusters(self, indicador):
        #clusters = self.puntosClusters.keys() #esperado , cluster 0, 1, 2....
        #clusters.sort(key=lambda c:indicador.evaluarCluster())
        clustersOrdenados=sorted(self.clusters,key=lambda c:indicador.evaluarCluster(c),reverse=True) #creo una nueva lista que este ordenada descendentemente por el valor que diga el indicador
        return clustersOrdenados
