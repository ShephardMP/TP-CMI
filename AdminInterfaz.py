# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 21:35:15 2018

@author: Mauro
"""

import mainWindow
import VentanaSeleccion
import AdminModelo
import VentanaMerge
import Dataset as ds
class AdminInterfaz:

    #SE ESPERA QUE SEAN STRINGS CON EL PATH A LSO ARCHIVOS DE DATOS
    adminModelo=None
    mw = None

    def __init__(self,referenciaAdminModelo=None):
        self.adminModelo=referenciaAdminModelo
        mainWindow.vp_start_gui(self)

    def setMainWindow(self, mainwindow):
        self.mw = mainwindow

    def mostrarDatos(self, nombreArchivo):

        #dejo el metodo hecho, pero la idea es que en la ventana principal cuando se quiera mostrar los datos se llame a este metodo
        #que se comunica con los otros admin para obtener el dataset que se quiera ya que se espera msotrar los dataset por pestañas
        pass

    def mostrarFiltros (self):

        #este metodo muestra en otro frame los filtros cargados, los filtros cargados para uso preferentemente se habririan y usarian
        #en el modelo
        pass


    def abrirVentanaCluster(self, nombreArchivos):
        #nombreArchivo es el nombre del archivo con el que quiero hacaer clustering, se espera tho, que sea el del merge
        self.listArchivoYColumnas=[]
        self.opcionesElegidas=[]
        numClusters=[]
        #for K in nombreArchivos:
            #nombrearchivos[K] es la ruta ABSOLUTA del archivo, la idea es obtener
            #las columnas del dataset para mostrar el nombre resumido del archivo y las columnas.
        auxDataset=self.adminModelo.getDataset(nombreArchivo)
        self.listArchivoYColumnas=auxDataset.nombresColumnas()

        #ventanaSeleccion es responsable de mostrar un el nobre del archivo y sus columnas para poder ser elegidas
        VentanaSeleccion.vp_start_gui(nombreArchivo.split('/')[-1], self.listArchivoYColumnas,self.opcionesElegidas,numClusters)
        
        if(len(self.opcionesElegidas)<2):
            raise ValueError('no se eligieron dos opciones para hacer clustering')
        if(len(numClusters)!=1):
            raise ValueError ("hubo error en seleccion de numero de clusters")
        self.configurarCluster(numClusters[0])
        self.mostrarCluster(nombreArchivo)




    def configurarCluster(self, ventanaSeleccion, cantClusters = 4):
        self.adminModelo.configurarCluster(cantidadClusters = cantClusters)




    def mostrarCluster(self, datosMerge):
        dataset = self.adminModelo.getDataset(rutaArchivo)
        self.adminModelo.generarCluster(self.opcionesElegidas[0],self.opcionesElegidas[1],dataset)
        print ('end cluster')


    def abrirVentanaMerge(self, nombresDatasetsAMergear):
        datasetsAMergear = []
        columnas = self.adminModelo.getNombresColumnasDatasets(nombresDatasetsAMergear)
        VentanaMerge.vp_start_gui(self, columnas)

    def realizarMerge(self, selecciones):
        datasetMerge = self.adminModelo.hacerMergeDatasets(selecciones)
        self.mw.agregarDataset(datasetMerge[1], datasetMerge[0]) # se manda el dataset y el nombre


    def mostrarArbol(self):
        pass

    def cargarDatos(self,ruta=None):
        #cuando en la interfaz se preciona el boton de cargar el excel, se llama a este metodo que llama al metodo en adminModelo para cargar los datos
        print('adminInterfazCargarDatos')
        #aplica filtros y categorias a los archivos despues de cargar o no filtros



        return self.adminModelo.cargarDatos(ruta)



    def cargarCategorias(self,ruta=None,aArchivo=None):
        print('adminInterfazCargarCategorias')
        return self.adminModelo.cargarCategorias(ruta,aArchivo)


        #parecido a lo de filtro, llamar a la logica de adminModelo

    def cargarFiltros(self,ruta=None,aArchivo=None):
        #parecido a lo de arriba, hay que definir un metodo en adminModelo que permita cargar los filtros
        print('adminInterfazCargarFiltros')
        return self.adminModelo.cargarFiltros(ruta,aArchivo)




    def obtenerDataset(self,claveDataset):
        return self.adminModelo.getDataset(claveDataset)

    def __test__(self):
        dataframe=self.adminModelo.hacerMergeDatasets()

        dataCluster = ds.Dataset()
        #dataCluster.cargarDataframe(dataMerge.seleccionarColumnas(['titulo_secundario','nota']))
        dataCluster.cargarDataframe(dataframe.seleccionarColumnas(["titulo_secundario","nota"]))
        return dataCluster

if __name__ == '__main__':
    model=AdminModelo.AdminModelo()
    admin= AdminInterfaz(model)
