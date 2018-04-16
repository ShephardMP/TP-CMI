# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 23:51:42 2018

@author: tomy-
"""

from abc import ABCMeta, abstractmethod #para la creación de clases abstractas


class ClusterGenerator:
     __metaclass__ = ABCMeta #Clase abstracta
     
     
     @abstractmethod
     def generarCluster(self,data): pass
    
"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"
from sklearn.cluster import KMeans
import tkinter as tk
import matplotlib.pyplot
#matplotlib.use('TkAgg') 
class ClusterKMeans(ClusterGenerator):
    kmeans=None
    

    def __init__(self, nClust=8, init='k-means++', it=10):
        self.setParametros(nClust,init,it)   #si vacio, es default
        
    def setParametros(self, numClusters=8, inicializacion='k-means++', initIteraciones=10):
        self.kmeans = KMeans(n_clusters=numClusters, init=inicializacion, n_init=initIteraciones)
        
    def generarCluster(self, data,etiquetaX='',etiquetaY=''): #Data deberia ser un array-like o 2D-array, cualquier cosa, pensar Data=numpy.random.rand(3,4)
         
         #plt.scatter(data[:, 0], data[:, 1], s=50) 
         self.kmeans.fit(data)
         prediccion=self.kmeans.predict(data)
         
         fig,cluster=matplotlib.pyplot.subplots() #crea nueva figura, otra ventana para renderizar el plot, no funciona dentro del IDE spyder a menos
         #que se se configure una opcion
         cluster.scatter(data[:, 0], data[:, 1],c=prediccion, s=50)
         
         cluster.set(xlabel=etiquetaX, ylabel=etiquetaY)
         auxX=[x for x in range (0,int(max(data[:, 0]))+1)]
         auxY=[x for x in range (0,int(max(data[:, 1]))+1)]
         matplotlib.pyplot.xticks(auxX) #establece que el x vaya de 1 a 10 (lo que hay en aux)
         matplotlib.pyplot.yticks(auxY)
         #plt.xticks(aux,etiquetasCategorias) mapea index del axis a las etiquetas de categorias
         
         matplotlib.pyplot.show(block=False) #muestra la figura
         
        
        
         