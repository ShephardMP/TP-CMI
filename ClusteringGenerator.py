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


    def __init__(self, nClust=8, init='k-means++', it=10):
        self.setParametros(nClust,init,it)   #si vacio, es default

    def setParametros(self, numClusters=8, inicializacion='k-means++', initIteraciones=10):
        self.kmeans = KMeans(n_clusters=numClusters, init=inicializacion, n_init=initIteraciones)

    def generarClustering(self, data,etiquetaX='',etiquetaY=''): #Data deberia ser un array-like o 2D-array, cualquier cosa, pensar Data=numpy.random.rand(3,4)

         #standarizedData=preprocessing.StandardScaler().fit_transform(data)
         standarizedData=data
         self.kmeans.fit(standarizedData)


         prediccion=self.kmeans.predict(standarizedData) #esto es mas de colores



         print('numClusters', self.kmeans.n_clusters)
         clusterGenerado=Clustering.Clustering(standarizedData,etiquetaX,etiquetaY,self.kmeans.labels_,self.kmeans.n_clusters,np.array(self.kmeans.cluster_centers_))



         return clusterGenerado
