# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 21:35:15 2018

@author: Mauro
"""

import mainWindow
class AdminInterfaz:
    
    #SE ESPERA QUE SEAN STRINGS CON EL PATH A LSO ARCHIVOS DE DATOS
    adminModelo=None
    def __init__(self,referenciaAdminModelo=None):
        adminModelo=referenciaAdminModelo
        mainWindow.vp_start_gui(self)
        
    
    def mostrarDatos(self, nombreArchivo):
        
        #dejo el metodo hecho, pero la idea es que en la ventana principal cuando se quiera mostrar los datos se llame a este metodo
        #que se comunica con los otros admin para obtener el dataset que se quiera ya que se espera msotrar los dataset por pestañas
        pass
    
    def mostrarFiltros (self):
        
        #este metodo muestra en otro frame los filtros cargados, los filtros cargados para uso preferentemente se habririan y usarian 
        #en el modelo
        pass
    
    
    def mostrarCluster(self):
            pass
        
    def mostrarArbol(self):
        pass
    
    def cargarDatos(self):
        #cuando en la interfaz se preciona el boton de cargar el excel, se llama a este metodo que llama al metodo en adminModelo para cargar los datos
        print('adminInterfazCargarDatos')
        pass
    
    def cargarCategorias(self):
        print('adminInterfazCargarCategorias')
        #parecido a lo de filtro, llamar a la logica de adminModelo
        pass
    def cargarFiltros(self):
        #parecido a lo de arriba, hay que definir un metodo en adminModelo que permita cargar los filtros
        print('adminInterfazCargarFiltros')
        pass
    


if __name__ == '__main__':
    admin= AdminInterfaz()


