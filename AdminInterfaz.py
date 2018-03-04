# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 21:35:15 2018

@author: Mauro
"""

import mainWindow
import VentanaSeleccion
import AdminModelo
class AdminInterfaz:
    
    #SE ESPERA QUE SEAN STRINGS CON EL PATH A LSO ARCHIVOS DE DATOS
    adminModelo=None
    
    def __init__(self,referenciaAdminModelo=None):
        self.adminModelo=referenciaAdminModelo
        mainWindow.vp_start_gui(self)
        
    
    def mostrarDatos(self, nombreArchivo):
        
        #dejo el metodo hecho, pero la idea es que en la ventana principal cuando se quiera mostrar los datos se llame a este metodo
        #que se comunica con los otros admin para obtener el dataset que se quiera ya que se espera msotrar los dataset por pestañas
        pass
    
    def mostrarFiltros (self):
        
        #este metodo muestra en otro frame los filtros cargados, los filtros cargados para uso preferentemente se habririan y usarian 
        #en el modelo
        pass
    
    
    def mostrarCluster(self, nombreArchivos):
        
        mapArchivoYColumnas={}
        opcionesElegidas={}
        opciones=[x for x in nombreArchivos.keys()] #lista por comprension, tiene los nombres resumidos
        for K in nombreArchivos:
            #nombrearchivos[K] es la ruta ABSOLUTA del archivo, la idea es obtener
            #las columnas del dataset para mostrar el nombre resumido del archivo y las columnas.
            auxDataset=self.adminModelo.getDataset(nombreArchivos[K])
            mapArchivoYColumnas[K]=auxDataset.nombresColumnas()
    
        VentanaSeleccion.vp_start_gui(mapArchivoYColumnas,opcionesElegidas)
        
        if(len(opcionesElegidas)<2):
            raise ValueError('no se eligieron dos opciones para hacer clustering')
        dataset=self.adminModelo.hacerMergeDatasets()
        self.adminModelo.generarCluster(opcionesElegidas[opciones[0]],opcionesElegidas[opciones[1]],dataset)
        print ('end cluster')
        
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

if __name__ == '__main__':
    model=AdminModelo.AdminModelo()
    admin= AdminInterfaz(model)


