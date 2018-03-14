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
    merge=None
    newCluster=None
    def __init__(self):
        self.datasets={}
        self.filtros={}
        self.categorias={}
        self.cargadorDefecto=cd.CargadorDatosExcel() #esto puede cambiarse tranquilamente
        self.newCluster=clustGen.ClusterKMeans()

    def cargarDatos(self,rutaArchivo):
        aux=ds.Dataset()
        aux.cargarDatos(self.cargadorDefecto, rutaArchivo)
        self.datasets[rutaArchivo]=aux



        print(rutaArchivo)
        return aux
        #dataset.eliminarPorGrupo('fecha_ingreso','legajo',lambda x: x is not None and x==x.min())

    def cargarFiltros(self,rutaArchivo=None,archivoDatos=None):
        def decodificarFiltro(campo,cond,valor):
            if(cond == '>'):
                return fil.FiltroMayor(campo,valor)
            elif (cond == '<'):
                return fil.FiltroMenor(campo,valor)
            elif (cond== "="):
                return fil.FiltroIgual(campo,valor)
            else:
                raise ValueError('condicion no es un simbolo valido: < > =')


       # self.filtros=fil.FiltroAND(fil.FiltroMayor('fecha_ingreso','2015-01-01'),fil.FiltroMenor('fecha_ingreso','2017-12-12'))
        arch=open(rutaArchivo)
        lineas=arch.readlines()
        auxFiltro=None
        auxFiltroSimples={} #esto es un diccionario/mapa, la posta es que en la linea que aparece en el archivo hay un filtro
        #se puede dar la situacion que haya un NOT en la linea 2, y un filtro en la linea 3. luego por ser diccionario se puede conseguir facil ese filtro con la clave 3 y aplicarle el not
        auxFiltroCompuestos=[]
        NOT=[] #es una lista que tiene el index (-1) del filtro al que hay que hacerle not
        AND=[]# esta es una lista con indices, si en la lista aparece un 1, hay que hacer un and entre el filtro en la linea - y el filtro en la linea 2
        index=0
        for l in lineas:
            if(len(l)<5): #chequeo que sea algun AND NOT OR

                condCompuesta=l.split('\n')[0] #decodifico si es and or not
                if(condCompuesta=='AND'):
                    AND.append(index)
                elif (condCompuesta=='NOT'):
                    NOT.append(index)


            else:
                campo,condicion,valor=l.split('..')
                auxFiltroSimples[index]=decodificarFiltro(campo,condicion,valor)
            index=index+1

        for x in NOT:
            auxFiltroSimples[x+1]=fil.FiltroNOT(auxFiltroSimples[x+1])
        for x in AND:
            auxFiltroCompuestos.append(fil.FiltroAND(auxFiltroSimples[x-1],auxFiltroSimples[x+1]))
        if(len(auxFiltroCompuestos)>1): #solo hacer OR si existe mas de un filtro AND
            for x in range(0,len(auxFiltroCompuestos),2):
                auxFiltro=fil.FiltroOR(auxFiltroCompuestos[x],auxFiltroCompuestos[x+1])
        else:
            auxFiltro=auxFiltroCompuestos[0]
        self.filtros[archivoDatos]=auxFiltro
        arch.close()

        self.datasets[archivoDatos].filtrar(self.filtros[archivoDatos])

        return self.datasets[archivoDatos] #para visualizar los datos cambiados

    def cargarCategorias(self,rutaArchivo,archivoDatos=None):

        #hay que hacer una logica para trabajar sobre archivos
        archivo = open (rutaArchivo)
        lines= archivo.readlines()
        if(len(lines)>1):
            self.categorias[archivoDatos]=[]
        for l in lines:
            atributo,valorAsociado,keys = l.split('..') #separa por los distintos campos de cada linea con ..
            keys = keys.replace('\n', '') #para eliminar los saltos de linea
            claves = keys.split(',') #las claves de cada categoria se separan por ,
            categoriaNueva = cat.Categoria(atributo, valorAsociado, claves)
            self.categorias[archivoDatos].append(categoriaNueva)

        #HACE FALTA TRABAJAR SOBRE CATEGORIAS PARA AGREGAR VALORES INVALIDOS

        self.categoriasInvalidos= ['BACHILLER', 'TÉCNICO', 'BACHILLERATO']
        archivo.close()

        auxCategorias=self.categorias[archivoDatos] #obtengo las categorias asociadas a ese archivo
        atr=auxCategorias[0].getNombreAtributo() #por ejemplo 'titlo_secundario'
        self.datasets[archivoDatos].columnaToUpper(atr) #la categoria afecta a esto
        for i,item in enumerate(auxCategorias):   #tambien creo que se puede el elemento directo
            self.datasets[archivoDatos].reemplazarValores(atr,auxCategorias[i].getKeys(), auxCategorias[i].getValorAsociado())


        self.datasets[archivoDatos].reemplazarValores( atr, self.categoriasInvalidos, 'nan')
        self.datasets[archivoDatos].eliminarValoresInvalidos( atr, 'nan')

        return self.datasets[archivoDatos] #agregado para que puedan verse los cambios

    def configurarCluster(self, cantidadClusters = 8, iteraciones = 10):
        self.newCluster.setParametros(numClusters = cantidadClusters, initIteraciones = iteraciones)

    def generarCluster(self,columna1,columna2,dataframe=None):
        #esto esta pensado para que cuando se llame para generar el cluster se llame con las columnas propiamente dichas
        if(dataframe is None):
            if(self.merge is None):
                dataframe=self.hacerMergeDatasets()
            else:
                dataframe=self.merge

        dataCluster = ds.Dataset()
        #dataCluster.cargarDataframe(dataMerge.seleccionarColumnas(['titulo_secundario','nota']))
        dataCluster.cargarDataframe(dataframe.seleccionarColumnas([columna1,columna2]))

        self.newCluster.generarCluster(dataCluster.toArray(),columna1,columna2)


    def getDataset(self,rutaClave):
        return self.datasets[rutaClave]

    def getDatasets(self):
        return self.datasets

    def hacerMergeDatasets(self):
        if(len(self.datasets)<2):
            raise ValueError('no se puede realizar merge de menos de un archivo')
        dataMerge=None
        counter=0
        for clave in self.datasets:
            if(counter == 0):
                #necesito el primer datasets para poder ir uniendo con los demas
                dataMerge=self.datasets[clave]
                counter=counter+1
            else:

                dataMerge.mergeCon(self.datasets[clave])

        self.merge=dataMerge
        return dataMerge

    def getDatasetMerge(self):
        if(self.merge is None):
            raise ValueError('no hay merges en adminModelo')
        return self.merge


if __name__ == '__main__':
    adminMod=AdminModelo()
    adminMod.cargarDatos('alumnos.xlsx')
    adminMod.cargarDatos('Finales.xlsx')
    adminMod.cargarFiltros('filtros.txt','alumnos.xlsx')
    adminMod.cargarCategorias('categorias.txt','alumnos.xlsx')

    adminMod.generarCluster('titulo_secundario','nota',adminMod.hacerMergeDatasets())
