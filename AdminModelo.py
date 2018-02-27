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
class AdminModelo:
    datasets = None  
    #es una Map<> o diccionario, la idea es que pueda indexarlos de acuerdo a la ruta
    #por ejemplo si la ruta es alumnos.xls se puete dataset[alumnos]=data
    
   
    filtros=None
    cargadorDefecto=None
    categorias=[]
    categoriasInvalidos=None
    
    def __init__(self):
        self.datasets={}
        self.cargadorDefecto=cd.CargadorDatosExcel() #esto puede cambiarse tranquilamente
       
    
    def cargarDatos(self,rutaArchivo,aplicarFiltros=False,aplicarCategorias=False):
        aux=ds.Dataset()
        aux.cargarDatos(self.cargadorDefecto, rutaArchivo)
        self.datasets[rutaArchivo]=aux
       
        if(self.filtros is not None and aplicarFiltros is True):
            self.datasets[rutaArchivo].filtrar(self.filtros)
        if(self.categorias is not None and aplicarCategorias is True):
            atr=self.categorias[0].getNombreAtributo() #por ejemplo 'titlo_secundario'
            self.datasets[rutaArchivo].columnaToUpper(atr) #la categoria afecta a esto
            for i,item in enumerate(self.categorias):   #tambien creo que se puede el elemento directo 
                    self.datasets[rutaArchivo].reemplazarValores(atr,self.categorias[i].getKeys(), self.categorias[i].getValorAsociado())
                    #HACE FALTA TRABAJAR SOBRE CATEGORIAS PARA AGREGAR VALORES INVALIDOS
                    
           
            self.datasets[rutaArchivo].reemplazarValores( atr, self.categoriasInvalidos, 'nan')
            self.datasets[rutaArchivo].eliminarValoresInvalidos( atr, 'nan')
            
        print(rutaArchivo)
    
        #dataset.eliminarPorGrupo('fecha_ingreso','legajo',lambda x: x is not None and x==x.min())

    def cargarFiltros(self,rutaArchivo=None):
        
        self.filtros=fil.FiltroAND(fil.FiltroMayor('fecha_ingreso','2015-01-01'),fil.FiltroMenor('fecha_ingreso','2017-12-12'))
        
    
    def cargarCategorias(self,rutaArchivo):
        
        #hay que hacer una logica para trabajar sobre archivos
        archivo = open (rutaArchivo)
        lines= archivo.readlines()
        for l in lines:
            atributo,valorAsociado,keys = l.split('..') #separa por los distintos campos de cada linea con ..
            keys = keys.replace('\n', '') #para eliminar los saltos de linea
            claves = keys.split(',') #las claves de cada categoria se separan por ,
            categoriaNueva = cat.Categoria(atributo, valorAsociado, claves)
            self.categorias.append(categoriaNueva)
        
        
        self.categoriasInvalidos= ['BACHILLER', 'TÉCNICO', 'BACHILLERATO']
        pass
    
    def generarCluster(self,columna1,columna2):
        #esto esta pensado para que cuando se llame para generar el cluster se llame con las columnas propiamente dichas
        
        dataMerge=None
        counter=0
        for clave in self.datasets:
            if(counter == 0):
                #necesito el primer datasets para poder ir uniendo con los demas
                dataMerge=self.datasets[clave]
                counter=counter+1
            else:
               
                dataMerge.mergeCon(self.datasets[clave])
        dataCluster = ds.Dataset()
        #dataCluster.cargarDataframe(dataMerge.seleccionarColumnas(['titulo_secundario','nota']))
        dataCluster.cargarDataframe(dataMerge.seleccionarColumnas([columna1,columna2]))
        newClust = clustGen.ClusterKMeans()
        newClust.generarCluster(dataCluster.toArray())
        
        
if __name__ == '__main__':
    adminMod=AdminModelo()
    adminMod.cargarFiltros()
    adminMod.cargarCategorias('categorias.txt')
    adminMod.cargarDatos('alumnos.xlsx',True,True)
    adminMod.cargarDatos('Finales.xlsx')
    adminMod.generarCluster('titulo_secundario','nota')