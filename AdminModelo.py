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
        self.categoriasInvalidos={}

    def cargarDatos(self,rutaArchivo):
        aux=ds.Dataset()
        aux.cargarDatos(self.cargadorDefecto, rutaArchivo)

        nombreArch=rutaArchivo.split('/')[-1]

        #nombreArch=nombreArch+'_'
        #aux.agregarPrefijoNombresColumnas(nombreArch)
        self.datasets[rutaArchivo]=aux


        print(rutaArchivo)
        return aux
        #dataset.eliminarPorGrupo('fecha_ingreso','legajo',lambda x: x is not None and x==x.min())

    def cargarFiltros(self,rutaArchivo=None,archivoDatos=None):

        def decodificarFiltro(campo,cond,valor):
            #self.datasets[archivoDatos].cambiarColumnaAString(campo) #para homogeneizar los tipos de datos
            #print ("TIPO",self.datasets[archivoDatos].columnaNumerica(campo))
            valorInstanciado=None
            if(self.datasets[archivoDatos].columnaNumerica(campo)):
                valorInstanciado=int(valor)
            else:
                valorInstanciado=str(valor)
            if(cond == '>'):
                return fil.FiltroMayor(campo,valorInstanciado)
            elif (cond == '<'):
                return fil.FiltroMenor(campo,valorInstanciado)
            elif (cond== '='):
                return fil.FiltroIgual(campo,valorInstanciado)
            elif (cond=='!='):
                return fil.FiltroNoIgual(campo,valorInstanciado)
            else:
                raise ValueError('condicion no es un simbolo valido: < > =')


       # self.filtros=fil.FiltroAND(fil.FiltroMayor('fecha_ingreso','2015-01-01'),fil.FiltroMenor('fecha_ingreso','2017-12-12'))
        arch=open(rutaArchivo)
        lineas=arch.readlines()
        auxFiltro=None
        auxFiltroSimples={} #esto es un diccionario/mapa, la posta es que en la linea que aparece en el archivo hay un filtro
        #se puede dar la situacion que haya un NOT en la linea 2, y un filtro en la linea 3. luego por ser diccionario se puede conseguir facil ese filtro con la clave 3 y aplicarle el not
        auxFiltroCompuestos=[]
        OR=[]
        AND=[]# esta es una lista con indices, si en la lista aparece un 1, hay que hacer un and entre el filtro en la linea - y el filtro en la linea 2
        index=0
        if(archivoDatos not in self.filtros):
            self.filtros[archivoDatos]=[]
        for l in lineas:
            if(len(l)<5): #chequeo que sea algun AND NOT OR

                condCompuesta=l.split('\n')[0] #decodifico si es and or not
                if(condCompuesta=='AND'):
                    AND.append(index)
                if(condCompuesta=='OR'):
                    OR.append(index)

            else:
                campo,condicion,valor=l.split('..')
                auxFiltroSimples[index]=decodificarFiltro(campo,condicion,valor)
            index=index+1


        indexCompuesto=-1
        simplesCubiertos=[]
        '''
        print ("AND",AND)
        print ("OR",OR)
        '''
        for x in range(0,index):
            print("x",x)
            if(x in AND):
                if((x-2)>0 and ((x-2) in AND)): #la operacion anterior era AND, debo hacer seguir la cadena
                    auxFiltroCompuestos[indexCompuesto]=fil.FiltroAND(auxFiltroCompuestos[indexCompuesto],auxFiltroSimples[x+1])

                else:
                    auxFiltroCompuestos.append(fil.FiltroAND(auxFiltroSimples[x-1],auxFiltroSimples[x+1]))
                    simplesCubiertos.append(x-1)
                    indexCompuesto=indexCompuesto+1
                simplesCubiertos.append(x+1) #por el if o por el else

        transformarACompuesto=[]
        for x in range(0,index):
            if (x not in simplesCubiertos and x not in AND and x not in OR):
                transformarACompuesto.append(x)


        for x in transformarACompuesto:
            #esto es porque pueden quedar algunos filtros aislados por operadores OR, si los hago compuestos entonces se hace el filtro automaticamente
            auxFiltroCompuestos.append(auxFiltroSimples[x])

        '''
        for x in AND:

                auxFiltroCompuestos.append(fil.FiltroAND(auxFiltroSimples[x-1],auxFiltroSimples[x+1]))
            print(x)
        '''
        if(len(auxFiltroCompuestos)>1): #solo hacer OR si existe mas de un filtro AND
            for x in range(0,len(auxFiltroCompuestos),2):
                auxFiltro=fil.FiltroOR(auxFiltroCompuestos[x],auxFiltroCompuestos[x+1])

        else:
            if(len(auxFiltroCompuestos)==1):
                auxFiltro=auxFiltroCompuestos[0]

            else:
                auxFiltro=list(auxFiltroSimples.values())[0] #values retorna dict_values, que es una view, no una lista, por lo que hay que hacer la ista con list()


        self.filtros[archivoDatos]=auxFiltro


        arch.close()

        self.datasets[archivoDatos].filtrar(self.filtros[archivoDatos])

        return self.datasets[archivoDatos] #para visualizar los datos cambiados

    def cargarCategorias(self,rutaArchivo,archivoDatos=None):

        nuevosInvalidos=False
        #hay que hacer una logica para trabajar sobre archivos
        archivo = open(rutaArchivo)
        if (archivoDatos not in self.categorias):
            self.categorias[archivoDatos]=[]
            self.categoriasInvalidos[archivoDatos]=[]


        while True:
            lines = archivo.readline()

            #LEE LA SIGUIENTE LINEA, ESTA FORMA PERMITE UN PROCESAMIENTO MAS RAPIDO
            #NO HAY QUE LEER TODO EL ARCHIVO DE UNA
            if not lines:
                break

            atributo,valorAsociado,keys = lines.split('..') #separa por los distintos campos de cada linea con ..
            keys = keys.replace('\n', '') #para eliminar los saltos de linea
            claves = keys.split(',') #las claves de cada categoria se separan por ,
            if (valorAsociado == 'invalid'):
                nuevosInvalidos=True
                for c in claves:
                    self.categoriasInvalidos[archivoDatos].append(c)

            else:

                categoriaNueva = cat.Categoria(atributo, valorAsociado, claves)
                self.categorias[archivoDatos].append(categoriaNueva)


        archivo.close()

        auxCategorias=self.categorias[archivoDatos] #obtengo las categorias asociadas a ese archivo
        atr=auxCategorias[-1].getNombreAtributo() #por ejemplo 'titulo_secundario', esto tomo siempre el ultimo, asi que guarda de mezclar categorias en un mismo archivo
        self.datasets[archivoDatos].columnaToUpper(atr) #la categoria afecta a esto
        for i,item in enumerate(auxCategorias):   #tambien creo que se puede el elemento directo
            self.datasets[archivoDatos].reemplazarValores(atr,auxCategorias[i].getKeys(), auxCategorias[i].getValorAsociado())

        if(nuevosInvalidos==True):
            self.datasets[archivoDatos].reemplazarValores(atr, self.categoriasInvalidos[archivoDatos], 'nan')
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
        dataCluster.sacarNaN(0,'any') #por fila, y si algun elemento es nan
        self.newCluster.generarCluster(dataCluster.toArray(),columna1,columna2)


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



    def hacerMergeDatasets(self, datosMerge):
        if(len(datosMerge) != 2):
            raise ValueError('Solo se pueden mergear 2 archivos')

        ds1 = None #defino los datasets que voy a mergear
        ds2 = None
        columnas1 = None
        columnas2 = None
        nombre1 = '' #estas variables van a servir para renombrar las columnas con igual nombre
        nombre2 = ''

        for ds in self.datasets:
            nombreDataset = ds.split('/')[-1] #obtengo sólo el nombre del archivo
            if nombreDataset in datosMerge:
                if ds1 is None:
                    ds1 = self.datasets[ds] #guardo el dataset1
                    nombre1 = nombreDataset #su nombre
                    columnas1 = datosMerge[nombreDataset] #y las columnas que quiero mergear
                else:
                    ds2 = self.datasets[ds]
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
        datasetMergeNombre = nombre1 + ' + ' + nombre2
        datasetMerge.mergeCon(ds2, left_on = columnas1, right_on = columnas2)

        self.datasets[datasetMergeNombre] = datasetMerge #se guarda el nuevo dataset en el diccionario de datasets

        return [datasetMergeNombre, datasetMerge] #retorna el nombre del nuevo dataset y el dataset mismo


    
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
