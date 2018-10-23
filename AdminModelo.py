# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 04:57:25 2018

@author: Mauro
"""
import Dataset as ds
import CargadorDatos as cd
import GuardadorDataframe as gd
import Filtro as fil
import Categoria as cat
import ClusteringGenerator as clustGen
import ArchivoCategorias as archCat
import ArchivoFiltros as archFil
import Indicador as indicador

class AdminModelo:
    datasets = None
    #es una Map<> o diccionario, la idea es que pueda indexarlos de acuerdo a la ruta
    #por ejemplo si la ruta es alumnos.xls se puete dataset[alumnos]=data
    cargadorDefecto=None
    guardadorDefecto=None
    merge=None
    indicadores=None

    newClustering=None

    def __init__(self):
        self.datasets={}
        self.indicadores=[]
        self.cargadorDefecto=cd.CargadorDatosExcel() #esto puede cambiarse tranquilamente
        self.guardadorDefecto=gd.GuardadorDataframeExcel()
        self.newClustering=clustGen.ClusteringKMeans()

        self.indicadores.append(indicador.IndicadorCantPuntos("Cantidad de puntos por cluster"))
        self.indicadores.append(indicador.IndicadorCantPuntosEnColumna("Cantidad de puntos en columna"))
        self.indicadores.append(indicador.IndicadorCantPuntosEnFila("Cantidad de puntos en fila"))

    def cargarDatos(self,rutaArchivo):
        dataset=ds.Dataset()
        dataset.cargarDatos(self.cargadorDefecto, rutaArchivo)

        rutaArchivo = self.obtenerNombreDatasetNoRepetido(rutaArchivo, dataset)

        self.datasets[rutaArchivo]=dataset #la clave rutaArchivo es un path absoluto



        return dataset, rutaArchivo

    def cargarFiltros(self,rutaArchivo=None,archivoDatos=None):


        archivoFiltros = archFil.ArchivoFiltros()
        filtro = archivoFiltros.cargar(rutaArchivo, self.datasets[archivoDatos]) #se obtiene el filtro


        self.datasets[archivoDatos].filtrar(filtro) #se filtra el dataset

        return self.datasets[archivoDatos] #para visualizar los datos cambiados



    def cargarCategorias(self,rutaArchivo,archivoDatos=None):

        archivoCategorias = archCat.ArchivoCategorias()
        categorias, invalidas = archivoCategorias.cargar(rutaArchivo)

        for categoria in categorias:
            atributo = categoria.getNombreAtributo()
            valor = categoria.getValorAsociado()
            keys = categoria.getKeys()
            self.datasets[archivoDatos].cambiarColumnaAString(atributo)
            #sea el tipo que sea la columna la transforma a String, sea numero o string o datetime
            self.datasets[archivoDatos].columnaToUpper(atributo)
            self.datasets[archivoDatos].reemplazarValores(atributo, keys, valor)

        for categoria in invalidas:
            atributo = categoria.getNombreAtributo()
            valor = categoria.getValorAsociado()
            keys = categoria.getKeys()
            self.datasets[archivoDatos].cambiarColumnaAString(atributo)
            self.datasets[archivoDatos].columnaToUpper(atributo)
            self.datasets[archivoDatos].reemplazarValores(atributo, keys, valor)
            self.datasets[archivoDatos].eliminarValoresInvalidos(atributo, 'NAN')

        return self.datasets[archivoDatos] #agregado para que puedan verse los cambios



    def configurarCluster(self, cantidadClusters = 8, iteraciones = 10):
        self.newClustering.setParametros(numClusters = cantidadClusters, initIteraciones = iteraciones)

    def generarClustering(self,columna1,columna2,dataframe=None):
        #esto esta pensado para que cuando se llame para generar el cluster se llame con las columnas propiamente dichas
        if(dataframe is None):
            raise ValueError('el dataframe para generar el cluster no puede ser None')

        dataCluster = ds.Dataset()
        #dataCluster.cargarDataframe(dataMerge.seleccionarColumnas(['titulo_secundario','nota']))
        dataCluster.cargarDataframe(dataframe.seleccionarColumnas([columna1,columna2]))
        dataCluster.cambiarColumnaANumerica(columna1)
        dataCluster.cambiarColumnaANumerica(columna2)
        dataCluster.sacarNaN(0,'any') #por fila, y si algun elemento es nan
        return self.newClustering.generarClustering(dataCluster.toArray(),columna1,columna2)


    def getDataset(self,rutaClave):
        return self.datasets[rutaClave]

    def getDatasets(self):
        return self.datasets

    def getNombresColumnasDatasets(self, nombresDatasets):
        columnas = {}
        for n in nombresDatasets:
            for d in self.datasets:
                nombreArchivo = d.split('/')[-1]
                if (nombreArchivo == n):
                    columnas[n] = self.datasets[d].nombresColumnas()
        return columnas



    def hacerMergeDatasets(self, datosMerge, tipoMerge = 'nombre'):
        if(len(datosMerge) != 2):
            raise ValueError('Solo se pueden mergear 2 archivos')

        ds1 = None #defino los datasets que voy a mergear
        ds2 = None
        columnas1 = None
        columnas2 = None
        nombre1 = '' #estas variables van a servir para renombrar las columnas con igual nombre
        nombre2 = ''

        for dataset in self.datasets:
            nombreDataset = dataset.split('/')[-1] #obtengo sólo el nombre del archivo
            if nombreDataset in datosMerge:
                if ds1 is None:
                    ds1 = self.datasets[dataset] #guardo el dataset1
                    nombre1 = nombreDataset #su nombre
                    columnas1 = datosMerge[nombreDataset] #y las columnas que quiero mergear
                else:
                    ds2 = self.datasets[dataset]
                    nombre2 = nombreDataset
                    columnas2 = datosMerge[nombreDataset]

        ds1 = ds1.getCopia()
        ds2 = ds2.getCopia()



        columnasRepetidas = list(set(ds1.nombresColumnas()) & set(ds2.nombresColumnas())) # todas las columnas repetidas de los datasets
        columnasRepetidas = list(set(columnasRepetidas) - set(set(columnas1) | set(columnas2))) #elimino las columnas seleccionadas
        for repetida in columnasRepetidas:
            ds1.reemplazarNombreColumna(repetida, repetida + ' - ' + nombre1)
            ds2.reemplazarNombreColumna(repetida, repetida + ' - ' + nombre2)


        datasetMerge = ds1

        datasetMergeNombre = nombre1 + '+' + nombre2
        if (tipoMerge == 'nombre'):
            datasetMerge.mergeCon(ds2, clave = list(set(set(columnas1) | set(columnas2))))
        elif (tipoMerge == 'posicion'):
            datasetMerge.mergeCon(ds2, left_on = columnas1, right_on = columnas2)
        else:
            raise ValueError ("Error en el tipo de merge")

        datasetMergeNombre = self.obtenerNombreDatasetNoRepetido(datasetMergeNombre, datasetMerge)

        self.datasets[datasetMergeNombre] = datasetMerge #se guarda el nuevo dataset en el diccionario de datasets

        return [datasetMergeNombre, datasetMerge] #retorna el nombre del nuevo dataset y el dataset mismo



    def getDatasetMerge(self):
        if(self.merge is None):
            raise ValueError('no hay merges en adminModelo')
        return self.merge

    def obtenerNombreDatasetNoRepetido(self, nombre, dataset):
        n = 1
        while nombre in self.datasets:
            if (n > 1):
                nombre = nombre[0 : -4]
            nombre = nombre + '(' + str(n) + ')'
            dataset.setNombre(nombre.split('/')[-1])
            n = n + 1
        return nombre

    def eliminarDataset(self,rutaClave):



        self.datasets.pop(rutaClave)

    def guardarDataset(self,rutaClave,nombre):
        print("archivo ",nombre)
        print('ruta', rutaClave)
        print('existe', self.datasets[rutaClave])
        print('existe', self.datasets)
        self.guardadorDefecto.guardarDataframe(self.datasets[rutaClave].datos(),nombre) #datasets es un arreglo de datasets, lo que quiero guardar son dataframe de pandas que se consiguen mediante el metodo datos() de dataset

    def getIndicadoresClusters(self):

        return self.indicadores


if __name__ == '__main__':
    adminMod=AdminModelo()
    adminMod.cargarDatos('alumnos.xlsx')
    adminMod.cargarDatos('Finales.xlsx')
    adminMod.cargarFiltros('filtros.txt','alumnos.xlsx')
    adminMod.cargarCategorias('categorias.txt','alumnos.xlsx')

    adminMod.generarClustering('titulo_secundario','nota',adminMod.hacerMergeDatasets())
