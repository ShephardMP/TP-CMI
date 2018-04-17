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
from matplotlib.figure import Figure
#matplotlib.use('TkAgg') 
class ClusterKMeans(ClusterGenerator):
    kmeans=None
    

    def __init__(self, nClust=8, init='k-means++', it=10):
        self.setParametros(nClust,init,it)   #si vacio, es default
        
    def setParametros(self, numClusters=8, inicializacion='k-means++', initIteraciones=10):
        self.kmeans = KMeans(n_clusters=numClusters, init=inicializacion, n_init=initIteraciones)
        
    def generarCluster(self, data,etiquetaX='',etiquetaY=''): #Data deberia ser un array-like o 2D-array, cualquier cosa, pensar Data=numpy.random.rand(3,4)
         
         
         self.kmeans.fit(data)
         prediccion=self.kmeans.predict(data)
         fig=Figure(figsize=(6,6))
         #la idea es crear una figura con el cluster hecho pero no mostrarla todavia,
         #este es el modelo, asi no incluyo nada de interfaz
         #devuelvo una figura (o podria devolver un subplot) para que la interfaz decida 
         #como se debe visualizar
         cluster=fig.add_subplot(111)
         cluster.scatter(data[:, 0], data[:, 1],c=prediccion, s=50)
         
         cluster.set(xlabel=etiquetaX, ylabel=etiquetaY)
         cluster.axis('tight')
         
         #cluster.axis('tight',xmin=int(min(data[:, 0])),ymin=int(min(data[:, 1])),xmax=int(max(data[:, 0]))+1,ymax=int(max(data[:, 1]))+1) #scaling para los ejes del plot
         
         #tight muestra toda la info posible. Cualquier cosa referir a:
         # https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.axis.html#matplotlib.axes.Axes.axis
         '''
         auxX=[x for x in range (int(min(data[:, 0])),int(max(data[:, 0]))+1)]
         auxY=[x for x in range (int(min(data[:, 1])),int(max(data[:, 1]))+1)]
         cluster.set_xlim(auxX[0],auxX[1]) #establece el eje X a un rango 
         cluster.set_ylim(auxY[0],auxY[1])
        '''
        
         #fig.show() #muestra la figura
         return fig    #retorno de tipo MATPLOTLIB.FIGURE
        
        
         