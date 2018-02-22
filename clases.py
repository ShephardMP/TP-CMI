# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 21:56:29 2017

@author: tomasmed18
"""

from abc import ABCMeta, abstractmethod #para la creación de clases abstractas
import pandas as pandas #biblioteca para trabajar con data frames

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"


class CargadorDatos:
    __metaclass__ = ABCMeta #Clase abstracta

    @abstractmethod
    def cargarArchivo(self, nombreArchivo): pass #Retorna un dataframe

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"


class CargadorDatosExcel(CargadorDatos):
    "Carga los datos desde un archivo .xlsx"

    def cargarArchivo(self, nombreArchivo):
        return pandas.read_excel(nombreArchivo)

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"


class Dataset:
    ds = []

    def cargarDatos(self, cargadorDatos, nombreArchivo): #Dado un cargador de datos que devuelva un Dataframe y un archivo, lo guarda como nuevo dataset
        self.ds = cargadorDatos.cargarArchivo(nombreArchivo)


    def cargarDataframe(self, dataframe): #Carga el dataframe enviado como parámetro
        self.ds = dataframe


    def datos(self): #Retorna el Dataframe
        return self.ds


    def mergeCon(self, otroDataset, clave, forma='inner'):
        self.ds = self.getMerge(otroDataset, clave, forma).datos()


    def getMerge(self, otroDataset, clave, forma='inner'):
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



"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"


class FiltroDataframe:
    __metaclass__ = ABCMeta #Clase abstracta

    @abstractmethod
    def cumple(self, dataframe): pass

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"


class FiltroSimple(FiltroDataframe):
    __metaclass__ = ABCMeta #Clase abstracta
    columna = ''
    valor = 0

    def __init__(self, columna, valor):
        self.columna = columna
        self.valor = valor

    def setColumna(self, columna):
        self.columna = columna

    def setValor(self, valor):
        self.valor = valor

    def getColumna(self):
        return self.columna

    def getValor(self):
        return self.valor

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"


class FiltroMayor(FiltroSimple):

    def cumple(self, dataframe):
        return dataframe[self.getColumna()] > self.getValor()

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"


class FiltroMenor(FiltroSimple):

    def cumple(self, dataframe):
        return dataframe[self.getColumna()] < self.getValor()

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"


class FiltroIgual(FiltroSimple):

    def cumple(self, dataframe):
        return dataframe[self.getColumna()] == self.getValor()

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"

class FiltroNOT(FiltroDataframe):
    filtro = None

    def __init__(self, filtro):
        self.filtro = filtro

    def cumple(self, dataframe):
        return ~(self.filtro.cumple(dataframe))

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"


class FiltroCompuesto(FiltroDataframe):
    __metaclass__ = ABCMeta #Clase abstracta
    f1 = None
    f2 = None

    def __init__(self, f1, f2):
        self.f1 = f1
        self.f2 = f2

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"


class FiltroAND(FiltroCompuesto):

    def cumple(self, dataframe):
        return self.f1.cumple(dataframe) & self.f2.cumple(dataframe)

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"


class FiltroOR(FiltroCompuesto):

    def cumple(self, dataframe):
        return self.f1.cumple(dataframe) | self.f2.cumple(dataframe)

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"

class Categoria:
    keys = []
    nombreAtributo = None
    valorAsociado = None

    def __init__(self, nombreAtributo, valorAsociado = 0, claves=[]):
        self.nombreAtributo = nombreAtributo
        self.valorAsociado = valorAsociado
        self.keys=[] #sin esto ES RE FLASHERO LO QUE PASA, se van concatenando las keys. Es como si la estructura esta fuera compartida y a la vez no.
        self.agregarKeys(claves)

    def getValorAsociado(self):
        return self.valorAsociado

    def getNombreAtributo(self):
        return self.nombreAtributo

    def getKeys(self):
        return self.keys

    def setValorAsociado(self, valor):
        self.valorAsociado = valor

    def setNombreAtributo(self, nombre):
        self.nombreAtributo = nombre

    def agregarKeys(self, nuevasKeys):
        self.keys[0:0] = nuevasKeys #Se insertan las nuevas keys al principio


"----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
"----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"

class ClusterGenerator:
     __metaclass__ = ABCMeta #Clase abstracta
     
     
     @abstractmethod
     def generarCluster(self,data): pass
    
"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

class ClusterKMeans(ClusterGenerator):
    kmeans=None
    

    def __init__(self, nClust=8, init='k-means++', it=10):
        self.setParametros(nClust,init,it)   #si vacio, es default
        
    def setParametros(self, numClusters=8, inicializacion='k-means++', initIteraciones=10):
        self.kmeans = KMeans(n_clusters=numClusters, init=inicializacion, n_init=initIteraciones)
        
    def generarCluster(self, data): #Data deberia ser un array-like o 2D-array, cualquier cosa, pensar Data=numpy.random.rand(3,4)
         
         #plt.scatter(data[:, 0], data[:, 1], s=50) 
         self.kmeans.fit(data)
         prediccion=self.kmeans.predict(data)
         
         plt.scatter(data[:, 0], data[:, 1],c=prediccion, s=50)
        
"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"








dataset = Dataset()
dataset.cargarDatos(CargadorDatosExcel(), 'alumnos.xlsx')


dataset.columnaToUpper('titulo_secundario')


dataset.filtrar(FiltroAND(FiltroMayor('fecha_ingreso','2005-01-01'),FiltroMenor('fecha_ingreso','2017-12-12')))
ECONOMIA = Categoria('titulo_secundario',0,['IMPOSITIVO', 'BS. Y SERV.', 'GESTION', 'ADMIN', 'EMPRESAS', 'BANCARIAS', 'ECONOMICAS', 'COMERCIAL','MERCANTIL','ECONOMIA','ADM', 'MUTUALES','CONTABLE','ECONOMÍA','BIENES', 'EMPRESA', 'EMPRESARIAL'])
NATURALES= Categoria('titulo_secundario',1,['AGROPECUARIO', 'NATURALES', 'SALUD', 'CIENCIASBIOLOG','AGROPECUARIA', 'PROD. AGROP.', 'AMBIENTALES', 'BIOLOGICAS', 'LABORAT.', 'BIOLOGICA', 'NATURAL', 'ALIMENTACION', 'GANADERIA', 'LABORATORIO', 'AGRARIA', 'BIOTECNOLOGICO', 'AGRARIO', 'QUIMICA', 'BIOLOGIA', 'QUIMICO', 'BIOLOGICO', 'AGRICOLA', 'AGRONOMO'])
EXACTAS= Categoria('titulo_secundario',2, ['EXACTAS', 'MATEMATICAS', 'FISICO-MATEMATICO', 'FÍSICO-MATEMÁTICAS', 'CIENCIASFISICO-MATEMAT.', 'FÍSICO-MATEMATICA'])
HUMANIDADES=Categoria('titulo_secundario',3,['SOCIALES', 'HUMANIDADES', 'HUMANAS', 'SOCIAL', 'HUMANISTA', 'HUMAN.', 'COMUNICACION', 'HUMANISTICAS'])
LENGUAS= Categoria('titulo_secundario',3, ['IDIOMAS', 'LENGUAS', 'LETRAS', 'IDIOMA'])
ARTE= Categoria('titulo_secundario',4,['ARTE', 'DISEÑO', 'MUSICA', 'MUSICAL', 'ARTISTICA'])
COMPUTACION = Categoria ('titulo_secundario',5,['COMPUTACION', 'INFORMATICA', 'A.DE SISTEM', 'INFORMACION', 'INFORMÁTICA', 'COMPUTACIÓN', 'COMPUTADORAS', 'PROGRAMACION'])
TURISMO = Categoria('titulo_secundario',6,['TURISMO', 'TURISTICOS'])
CONSTRUCCION = Categoria ('titulo_secundario',7,['CONSTRUCCION', 'MAESTRO MAYOR', 'CARPINTERO'])
MECANICA = Categoria ('titulo_secundario',8,['MECANICA', 'ELECTROMECANICA', 'ELECTROMECANICO', 'ELECTRICISTA', 'MECANICO', 'AUTOMOTORES', 'ELECTRÓNICA', 'ELECTRONICA', 'ELECTRONICO', 'ELECTROTECNIA'])
DOCENTE = Categoria ('titulo_secundario',9, ['DOCENTE', 'PEDAGOGICO', 'PEDAGÓGICO', 'PEDAGOGICA', 'EDUCACION FISICA'])

arrCat=[ECONOMIA,NATURALES,EXACTAS,HUMANIDADES,LENGUAS,ARTE,COMPUTACION,TURISMO,CONSTRUCCION,MECANICA,DOCENTE]

for i,item in enumerate(arrCat):   #tambien creo que se puede el elemento directo 
    dataset.reemplazarValores(arrCat[i].getNombreAtributo(),arrCat[i].getKeys(), arrCat[i].getValorAsociado())

dataset.reemplazarValores('titulo_secundario', ['BACHILLER', 'TÉCNICO', 'BACHILLERATO'], 'nan')
dataset.eliminarValoresInvalidos('titulo_secundario', 'nan')


dataAlumnos = dataset.datos()


datasetFinales = Dataset()
datasetFinales.cargarDatos(CargadorDatosExcel(),'Finales.xlsx')
dataset.eliminarPorGrupo('fecha_ingreso','legajo',lambda x: x is not None and x==x.min())

dataFinales = datasetFinales.datos()
dataFinalesMergeAlumnos=dataset.getMerge(datasetFinales,clave='legajo')

dataFinalesMergeAlumnosDatos=dataFinalesMergeAlumnos.datos()

dataCluster=Dataset()
dataCluster.cargarDataframe(dataFinalesMergeAlumnos.seleccionarColumnas(['titulo_secundario','nota']))

#datasetNuevo = Dataset()
#datasetNuevo.cargarDatos(ce,'alumnos.xlsx')
#datasetNuevo.eliminarPorGrupo('fecha_ingreso','legajo',lambda x: x is not None and x==x.min())
#datasetNuevo.filtrar(FiltroAND(FiltroMayor('fecha_ingreso','2003-01-01' ),FiltroMenor('fecha_ingreso','2017-12-31'))) #vamos a controlar el ingreso para que este entre dos fechas
#
#
#dataNuevo=datasetNuevo.datos()
#
#print(dataNuevo['fecha_ingreso'])
import numpy as np

X = np.random.rand(30,2)
print(X)

newClust=ClusterKMeans()
newClust.generarCluster(dataCluster.toArray())


# hacer not de examen equivalente
