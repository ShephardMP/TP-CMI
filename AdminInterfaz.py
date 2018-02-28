# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 21:35:15 2018

@author: Mauro
"""

import mainWindow
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
    
    
    def mostrarCluster(self, columna1='titulo_secundario',columna2='nota'):
        self.adminModelo.generarCluster(columna1,columna2)
        print ('end cluster')
        
    def mostrarArbol(self):
        pass
    
    def cargarDatos(self,ruta=None):
        #cuando en la interfaz se preciona el boton de cargar el excel, se llama a este metodo que llama al metodo en adminModelo para cargar los datos
        print('adminInterfazCargarDatos')
        #aplica filtros y categorias a los archivos despues de cargar o no filtros
        self.adminModelo.cargarDatos(ruta)
      
    
    def cargarCategorias(self,ruta=None,aArchivo=None):
        self.adminModelo.cargarCategorias(ruta,aArchivo)
       
        print('adminInterfazCargarCategorias')
        #parecido a lo de filtro, llamar a la logica de adminModelo
      
    def cargarFiltros(self,ruta=None,,aArchivo=None):
        #parecido a lo de arriba, hay que definir un metodo en adminModelo que permita cargar los filtros
        self.adminModelo.cargarFiltros(ruta,aArchivo)
        
        print('adminInterfazCargarFiltros')
        
    


if __name__ == '__main__':
    model=AdminModelo.AdminModelo()
    admin= AdminInterfaz(model)


