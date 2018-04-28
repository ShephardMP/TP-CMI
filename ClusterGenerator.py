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

import matplotlib.pyplot
from matplotlib.figure import Figure
import Cluster as Cluster
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as color
class ClusterKMeans(ClusterGenerator):
    kmeans=None
    

    def __init__(self, nClust=8, init='k-means++', it=10):
        self.setParametros(nClust,init,it)   #si vacio, es default
        
    def setParametros(self, numClusters=8, inicializacion='k-means++', initIteraciones=10):
        self.kmeans = KMeans(n_clusters=numClusters, init=inicializacion, n_init=initIteraciones)
        
    def generarCluster(self, data,etiquetaX='',etiquetaY=''): #Data deberia ser un array-like o 2D-array, cualquier cosa, pensar Data=numpy.random.rand(3,4)
         
         
         self.kmeans.fit(data)
         prediccion=self.kmeans.predict(data)
         
         colormap = cm.rainbow(np.linspace(0, 1, self.kmeans.n_clusters))
         
         puntosClusters={i: np.where(self.kmeans.labels_ == i)[0] for i in range(self.kmeans.n_clusters)} 
         #lo anterior crea un diccionar con el numero de cluster como clave y todos los puntos como contenido
         #i es clave y el np.where es una lista por comprension
         #lo siguiente es una version mejorada que cuenta la cantidad de puntos de forma directa
         
         diccClustersXCantPuntos={i: sum(1 for x in puntosClusters[i]) for i in puntosClusters.keys()} 
         diccClustersXColores={}
         
         auxColor=0
         for i in puntosClusters.keys():
             diccClustersXColores[i]=color.to_hex(colormap[auxColor]) #transformo el color a hexadecimal para ser mas portable
             auxColor+=1
             #auxColor siempre esta entre 0 y n_clusters por lo que no hay errores de rango
         
         
         fig=Figure(figsize=(6,6))
         #la idea es crear una figura con el cluster hecho pero no mostrarla todavia,
         #este es el modelo, asi no incluyo nada de interfaz
         #devuelvo un Cluster() con una figura (o podria devolver un subplot) para que la interfaz decida 
         #como se debe visualizar
        
         
       
        
         plot=fig.add_subplot(111)
         #labels=['cluster '+str(i) +': ' + str( diccClustersXCantPuntos[i]) for i in range(0,self.kmeans.n_clusters)]
        
         
         plot.scatter(data[:, 0], data[:, 1],c=colormap[self.kmeans.labels_])
         correlacion=np.corrcoef(data[:, 0],data[:, 1])
         print ('coeficiente de correlacion\n', correlacion)
         
         #plot.scatter(data[:, 0], data[:, 1],c=prediccion)
         #plot.legend(colormap,labels,bbox_to_anchor=(0.0,0.0), loc=2, borderaxespad=0.)
         
         plot.set(xlabel=etiquetaX, ylabel=etiquetaY)
         plot.axis('tight')
         
         #cluster.axis('tight',xmin=int(min(data[:, 0])),ymin=int(min(data[:, 1])),xmax=int(max(data[:, 0]))+1,ymax=int(max(data[:, 1]))+1) #scaling para los ejes del plot
         
         #tight muestra toda la info posible. Cualquier cosa referir a:
         # https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.axis.html#matplotlib.axes.Axes.axis
         '''
         auxX=[x for x in range (int(min(data[:, 0])),int(max(data[:, 0]))+1)]
         auxY=[x for x in range (int(min(data[:, 1])),int(max(data[:, 1]))+1)]
         cluster.set_xlim(auxX[0],auxX[1]) #establece el eje X a un rango 
         cluster.set_ylim(auxY[0],auxY[1])
        '''
        
         
         clusterGenerado=Cluster.Cluster(fig,correlacion,diccClustersXCantPuntos,diccClustersXColores)
         return clusterGenerado    #retorno de tipo MATPLOTLIB.FIGURE
        
        
         