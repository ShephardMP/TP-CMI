# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 23:46:25 2018

@author: tomy-
"""

import pandas as pandas #biblioteca para trabajar con data frames

from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
class Dataset:
    ds = []

    def cargarDatos(self, cargadorDatos, nombreArchivo): #Dado un cargador de datos que devuelva un Dataframe y un archivo, lo guarda como nuevo dataset
        self.ds = cargadorDatos.cargarArchivo(nombreArchivo)
        
  

    def cargarDataframe(self, dataframe): #Carga el dataframe enviado como parámetro
        self.ds = dataframe


    def datos(self): #Retorna el Dataframe
        return self.ds

    def getCopia(self):
        out= Dataset()
        out.cargarDataframe(self.ds.copy(deep=True))
        return out
    
    def mergeCon(self, otroDataset, clave=None, forma='inner'):
        self.ds = self.getMerge(otroDataset, clave, forma).datos()


    def getMerge(self, otroDataset, clave=None, forma='inner'):
        out = Dataset()
        out.cargarDataframe(pandas.merge(self.datos(),otroDataset.datos(), on=clave,how=forma))
        return out


    def reemplazarValores(self, columna, valoresAReemplazar, nuevoValor): #Reemplaza, de una columna, todos los valores que contengan alguna palabra
                                                                         #dentro de valoresAReemplazar
        self.ds.loc[self.ds[columna].str.contains('|'.join(valoresAReemplazar),na=False), columna]=str(nuevoValor)


    def reemplazarValoresLista(self, listaReemplazos):
        for x in listaReemplazos:
            self.reemplazarValores(x[0], x[1], x[2])


    def columnaToUpper(self, columna): #Dado el nombre de una columna, convierte todos los valores de la misma a mayúsculas
        self.ds[columna] = self.ds[columna].str.upper()


    def seleccionarColumnas(self, columnas): #Dada una lista de nombres de columnas, retorna un dataframe con los valores de esas columnas
        return self.ds.filter(items = columnas)


    def filtrar(self, filtro):
        self.ds = self.ds.loc[filtro.cumple(self.ds)]


    def eliminarColumna(self, columna): #Dado el nombre de una columna, la elimina del dataset
        self.ds = self.ds.drop([columna], axis = 1)


    def eliminarValoresInvalidos(self, columna, valor):
        self.ds = self.ds[self.ds[columna].str.contains(valor)==False]


    def eliminarPorGrupo(self, columna, agrupamiento, funcion):
        #metodo pensado para eliminar filas dentro de un agrupamiento segun una condicion (dada en function, debe ser algo estilo lambda)
        #por ejemplo, para hacer que un grupo de filas de mismo legajo tenga el minimo de fecha entre ellos
        #self.ds=self.ds[self.ds.fecha_ingreso.groupby(datasetAlumnos.legajo).apply(lambda x: x is not None and x==x.min())]

        self.ds=self.ds[self.ds[columna].groupby(self.ds[agrupamiento]).apply(funcion)]
        
    def toArray(self):
        return self.ds.values
    
    def nombresColumnas(self):
        return list(self.ds.columns.values)
    
    def getFila(self, index):
        fila = self.ds.ix[index]
        salida = []
        for i in range(0, len(fila)):
            salida.append(fila[i])
        return salida
    
    def cantidadFilas(self):
        return len(self.ds.index)
    
    def sacarNaN(self,axis=0,how='any'): 
        #axis =0 es filas, how puede ser any o all
        self.ds=self.ds.dropna(axis,how)
    
    def cambiarColumnaAString(self,columna):
        self.ds[columna]= self.ds[columna].apply(str)
    
    def columnaNumerica(self,columna):
        return is_numeric_dtype(self.ds[columna])
    
    
        
if __name__ == '__main__':
    import numpy as np
    df=Dataset()
    df.cargarDataframe(pandas.DataFrame([[np.nan, 2, np.nan, 0], [3, 4, np.nan, 1],
                   [np.nan, np.nan, np.nan, 5]],
                  columns=list('ABCD')))
    print(df.toArray(),'\n')
    df.sacarNaN(1)
    print(df.toArray())
