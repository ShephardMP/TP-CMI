# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 04:57:25 2018

@author: Mauro
"""
import Dataset as ds
import CargadorDatos as cd
import Filtro as fil
import Categoria as cat
import ClusterGenerator as clustGen
import ArchivoCategorias as archCat
import ArchivoFiltros as archFil


class AdminModelo:
    datasets = None
    #es una Map<> o diccionario, la idea es que pueda indexarlos de acuerdo a la ruta
    #por ejemplo si la ruta es alumnos.xls se puete dataset[alumnos]=data
    cargadorDefecto=None
    merge=None
    newCluster=None

    def __init__(self):
        self.datasets={}
        self.cargadorDefecto=cd.CargadorDatosExcel() #esto puede cambiarse tranquilamente
        self.newCluster=clustGen.ClusterKMeans()

    def cargarDatos(self,rutaArchivo):
        aux=ds.Dataset()
        aux.cargarDatos(self.cargadorDefecto, rutaArchivo)

        nombreArch=rutaArchivo.split('/')[-1]

        self.datasets[rutaArchivo]=aux
        print(rutaArchivo)
        return aux

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
            self.datasets[archivoDatos].columnaToUpper(atributo)
            self.datasets[archivoDatos].reemplazarValores(atributo, keys, valor)

        for categoria in invalidas:
            atributo = categoria.getNombreAtributo()
            valor = categoria.getValorAsociado()
            keys = categoria.getKeys()
            self.datasets[archivoDatos].columnaToUpper(atributo)
            self.datasets[archivoDatos].reemplazarValores(atributo, keys, valor)
            self.datasets[archivoDatos].eliminarValoresInvalidos(atributo, 'nan')

        return self.datasets[archivoDatos] #agregado para que puedan verse los cambios



    def configurarCluster(self, cantidadClusters = 8, iteraciones = 10):
        self.newCluster.setParametros(numClusters = cantidadClusters, initIteraciones = iteraciones)

    def generarCluster(self,columna1,columna2,dataframe=None):
        #esto esta pensado para que cuando se llame para generar el cluster se llame con las columnas propiamente dichas
        if(dataframe is None):
            raise ValueError('el dataframe para generar el cluster no puede ser None')

        dataCluster = ds.Dataset()
        #dataCluster.cargarDataframe(dataMerge.seleccionarColumnas(['titulo_secundario','nota']))
        dataCluster.cargarDataframe(dataframe.seleccionarColumnas([columna1,columna2]))
        dataCluster.cambiarColumnaANumerica(columna1)
        dataCluster.cambiarColumnaANumerica(columna2)
        dataCluster.sacarNaN(0,'any') #por fila, y si algun elemento es nan
        self.newCluster.generarCluster(dataCluster.toArray(),columna1,columna2)


    def getDataset(self,rutaClave):
        return self.datasets[rutaClave]

    def getDatasets(self):
        return self.datasets

    def hacerMergeDatasets(self, datosMerge):


        if(len(self.datasets)<2):
            raise ValueError('no se puede realizar merge de menos de un archivo')
        dataMerge=None
        counter=0
        palabrasClavesAnt=None
        palabrasClavesAct=None
        for clave in self.datasets: #clave sería la ruta absoluta del archivo
            nombreArchivo = clave.split('/')[-1] #obtengo sólo el nombre del archivo

            if(counter == 0): #necesito el primer datasets para poder ir uniendo con los demas
                dataMerge=self.datasets[clave].getCopia()
                palabrasClavesAnt=datosMerge[nombreArchivo]


            else:
                if (datosMerge[nombreArchivo] != None):
                    print  (datosMerge[nombreArchivo])
                    palabrasClavesAct= datosMerge[nombreArchivo]

                    dataMerge.mergeCon(self.datasets[clave], left_on=palabrasClavesAnt,right_on= palabrasClavesAct)
                    palabrasClavesAnt=palabrasClavesAct

                '''
                este else se tendría que agregar solo si se quiere que, si
                no se seleccionan columnas para hacer el merge, se haga por
                todas las columnas en comun.

                else:
                    dataMerge.mergeCon(self.datasets[clave])
                '''
            counter += 1

        print (dataMerge.nombresColumnas())

        self.merge=dataMerge

        '''
        solo testing
        import test as test
        test.vp_start_gui(dataMerge)
        '''

        return dataMerge

    def getDatasetMerge(self):
        if(self.merge is None):
            raise ValueError('no hay merges en adminModelo')
        return self.merge

    def removeDataset(self,rutaClave):
        #es necesario limpiar la entrada del dataset y los filtros y categorias asociados
        self.datasets.pop(rutaClave)
        self.filtros.pop(rutaClave)
        self.categorias.pop(rutaClave)
        self.categoriasInvalidas.pop(rutaClave)

if __name__ == '__main__':
    adminMod=AdminModelo()
    adminMod.cargarDatos('alumnos.xlsx')
    adminMod.cargarDatos('Finales.xlsx')
    adminMod.cargarFiltros('filtros.txt','alumnos.xlsx')
    adminMod.cargarCategorias('categorias.txt','alumnos.xlsx')

    adminMod.generarCluster('titulo_secundario','nota',adminMod.hacerMergeDatasets())
