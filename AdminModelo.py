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
    categorias=None
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
            atr=arrCat[0].getNombreAtributo() #por ejemplo 'titlo_secundario'
            self.datasets[rutaArchivo].columnaToUpper(atr) #la categoria afecta a esto
            for i,item in enumerate(arrCat):   #tambien creo que se puede el elemento directo 
                    self.datasets[rutaArchivo].reemplazarValores(atr,arrCat[i].getKeys(), arrCat[i].getValorAsociado())
                    #HACE FALTA TRABAJAR SOBRE CATEGORIAS PARA AGREGAR VALORES INVALIDOS
                    
           
            self.datasets[rutaArchivo].reemplazarValores( atr, self.categoriasInvalidos, 'nan')
            self.datasets[rutaArchivo].eliminarValoresInvalidos( atr, 'nan')
    
        #dataset.eliminarPorGrupo('fecha_ingreso','legajo',lambda x: x is not None and x==x.min())

    def cargarFiltros(self,rutaArchivo=None):
        
        self.filtros=fil.FiltroAND(fil.FiltroMayor('fecha_ingreso','2015-01-01'),fil.FiltroMenor('fecha_ingreso','2017-12-12'))
        
    
    def cargarCategorias(self,rutaArchivo=None):
        
        #hay que hacer una logica para trabajar sobre archivos
        ECONOMIA = cat.Categoria('titulo_secundario',0,['IMPOSITIVO', 'BS. Y SERV.', 'GESTION', 'ADMIN', 'EMPRESAS', 'BANCARIAS', 'ECONOMICAS', 'COMERCIAL','MERCANTIL','ECONOMIA','ADM', 'MUTUALES','CONTABLE','ECONOMÍA','BIENES', 'EMPRESA', 'EMPRESARIAL'])
        NATURALES = cat.Categoria('titulo_secundario',1,['AGROPECUARIO', 'NATURALES', 'SALUD', 'CIENCIASBIOLOG','AGROPECUARIA', 'PROD. AGROP.', 'AMBIENTALES', 'BIOLOGICAS', 'LABORAT.', 'BIOLOGICA', 'NATURAL', 'ALIMENTACION', 'GANADERIA', 'LABORATORIO', 'AGRARIA', 'BIOTECNOLOGICO', 'AGRARIO', 'QUIMICA', 'BIOLOGIA', 'QUIMICO', 'BIOLOGICO', 'AGRICOLA', 'AGRONOMO'])
        EXACTAS = cat.Categoria('titulo_secundario',2, ['EXACTAS', 'MATEMATICAS', 'FISICO-MATEMATICO', 'FÍSICO-MATEMÁTICAS', 'CIENCIASFISICO-MATEMAT.', 'FÍSICO-MATEMATICA'])
        HUMANIDADES = cat.Categoria('titulo_secundario',3,['SOCIALES', 'HUMANIDADES', 'HUMANAS', 'SOCIAL', 'HUMANISTA', 'HUMAN.', 'COMUNICACION', 'HUMANISTICAS'])
        LENGUAS = cat.Categoria('titulo_secundario',3, ['IDIOMAS', 'LENGUAS', 'LETRAS', 'IDIOMA'])
        ARTE = cat.Categoria('titulo_secundario',4,['ARTE', 'DISEÑO', 'MUSICA', 'MUSICAL', 'ARTISTICA'])
        COMPUTACION = cat.Categoria ('titulo_secundario',5,['COMPUTACION', 'INFORMATICA', 'A.DE SISTEM', 'INFORMACION', 'INFORMÁTICA', 'COMPUTACIÓN', 'COMPUTADORAS', 'PROGRAMACION'])
        TURISMO = cat.Categoria('titulo_secundario',6,['TURISMO', 'TURISTICOS'])
        CONSTRUCCION = cat.Categoria ('titulo_secundario',7,['CONSTRUCCION', 'MAESTRO MAYOR', 'CARPINTERO'])
        MECANICA = cat.Categoria ('titulo_secundario',8,['MECANICA', 'ELECTROMECANICA', 'ELECTROMECANICO', 'ELECTRICISTA', 'MECANICO', 'AUTOMOTORES', 'ELECTRÓNICA', 'ELECTRONICA', 'ELECTRONICO', 'ELECTROTECNIA'])
        DOCENTE = cat.Categoria ('titulo_secundario',9, ['DOCENTE', 'PEDAGOGICO', 'PEDAGÓGICO', 'PEDAGOGICA', 'EDUCACION FISICA'])
        
        self.categorias=[ECONOMIA,NATURALES,EXACTAS,HUMANIDADES,LENGUAS,ARTE,COMPUTACION,TURISMO,CONSTRUCCION,MECANICA,DOCENTE]
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
                print (type(self.datasets[clave]))
                dataMerge.mergeCon(self.datasets[clave])
        dataCluster = ds.Dataset()
        #dataCluster.cargarDataframe(dataMerge.seleccionarColumnas(['titulo_secundario','nota']))
        dataCluster.cargarDataframe(dataMerge.seleccionarColumnas([columna1,columna2]))
        newClust = clustGen.ClusterKMeans()
        newClust.generarCluster(dataCluster.toArray())
        
if __name__ == '__main__':
    adminMod=AdminModelo()
    adminMod.cargarFiltros()
    adminMod.cargarCategorias()
    adminMod.cargarDatos('alumnos.xlsx',True,True)
    adminMod.cargarDatos('Finales.xlsx')
    adminMod.generarCluster('titulo_secundario','nota')