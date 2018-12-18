# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 23:51:42 2018

@author: tomy-
"""

from abc import ABCMeta, abstractmethod #para la creación de clases abstractas


class ClusteringGenerator:
     __metaclass__ = ABCMeta #Clase abstracta


     @abstractmethod
     def generarClustering(self,data): pass

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"
from sklearn.cluster import KMeans
from sklearn import preprocessing

import Clustering as Clustering
import numpy as np
class ClusteringKMeans(ClusteringGenerator):
    kmeans=None


    def __init__(self, nClust=8, init='k-means++', it=100):
        self.setParametros(nClust,init,it)   #si vacio, es default

    def setParametros(self, numClusters=8, inicializacion='k-means++', initIteraciones=100):
        self.kmeans = KMeans(n_clusters=numClusters, init=inicializacion, n_init=initIteraciones)
        #self.kmeans = KMeans(n_clusters=numClusters, init=inicializacion, n_init=initIteraciones,random_state=1)#random_state es una seed para que no se vaya de mambo haciendo distintos clusters
    def generarClustering(self, data,etiquetaX='',etiquetaY=''): #Data deberia ser un array-like o 2D-array, cualquier cosa, pensar Data=numpy.random.rand(3,4)
         #data debiera ser una representacion en numpy


         rangos=[min(data[:,0]), max(data[:,0]), min(data[:,1]), max(data[:,1])] #en este orden, el min y max del eje X y el min y max del eje Y

         MinMaxScaler=preprocessing.MinMaxScaler()
         standarizedData=MinMaxScaler.fit_transform(data)
         #standarizedData=data
         self.kmeans.fit(standarizedData)


         #prediccion=self.kmeans.predict(standarizedData) #esto es mas de colores.

         """
         print(rangos)
         print('numClusters', self.kmeans.n_clusters)

         minScaleX= min(self.kmeans.cluster_centers_[:,0])
         maxScaleX= max(self.kmeans.cluster_centers_[:,0])
         minScaleY= min(self.kmeans.cluster_centers_[:,1])
         maxScaleY= max(self.kmeans.cluster_centers_[:,1])

         def reScale(OldValue, OldMin, OldMax, NewMin, NewMax): #funcion de utilidad para reposicionar los centros
             print('{}'.format(OldMin,OldMax,NewMin,NewMax))
             OldRange = (OldMax - OldMin)
             NewRange = (NewMax - NewMin)
             NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
             return NewValue

         """
         self.kmeans.cluster_centers_=MinMaxScaler.inverse_transform(self.kmeans.cluster_centers_) #reposiciono los centros para mostrarlos mejor

         #el sentido de lo anterior es que debo hacaer el clustering sobre los datos standarizados, obtener las labels correctas pero mostrar los valores viejos
         #en los ejes. Es decir, tengo los beneficios de hacer buen clustering y ademas no mostrar la data escalada que no ayuda en el analisis
         #en lo siguiente puedo usar la data antes del transform ya que los labels ya fueron asignados
         #si utilizo el inverse_transform del standarized data puede que tenga errores de precision minusculos que no permitan
         #usar correctamente indicadores, ej 1 != 0.99999 .....
         clusterGenerado=Clustering.Clustering(data,etiquetaX,etiquetaY,self.kmeans.labels_,self.kmeans.n_clusters,np.array(self.kmeans.cluster_centers_),rangos)



         return clusterGenerado
