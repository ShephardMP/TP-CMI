# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 23:23:50 2018

@author: tomy-
"""


import Dataset as ds
import CargadorDatos as cd
import Filtro as fil
import Categoria as cat
import ClusterGenerator as clustGen


dataset = ds.Dataset()
dataset.cargarDatos(cd.CargadorDatosExcel(), 'alumnos.xlsx')


dataset.columnaToUpper('titulo_secundario')


dataset.filtrar(fil.FiltroAND(fil.FiltroMayor('fecha_ingreso','2015-01-01'),
                              fil.FiltroMenor('fecha_ingreso','2017-12-12')))

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

arrCat=[ECONOMIA,NATURALES,EXACTAS,HUMANIDADES,LENGUAS,ARTE,COMPUTACION,TURISMO,CONSTRUCCION,MECANICA,DOCENTE]

for i,item in enumerate(arrCat):   #tambien creo que se puede el elemento directo 
    dataset.reemplazarValores(arrCat[i].getNombreAtributo(),arrCat[i].getKeys(), arrCat[i].getValorAsociado())

dataset.reemplazarValores('titulo_secundario', ['BACHILLER', 'TÉCNICO', 'BACHILLERATO'], 'nan')
dataset.eliminarValoresInvalidos('titulo_secundario', 'nan')


dataAlumnos = dataset.datos()


datasetFinales = ds.Dataset()
datasetFinales.cargarDatos(cd.CargadorDatosExcel(),'Finales.xlsx')
dataset.eliminarPorGrupo('fecha_ingreso','legajo',lambda x: x is not None and x==x.min())

dataFinales = datasetFinales.datos()
dataFinalesMergeAlumnos=dataset.getMerge(datasetFinales,clave='legajo')

dataFinalesMergeAlumnosDatos=dataFinalesMergeAlumnos.datos()

dataCluster = ds.Dataset()
dataCluster.cargarDataframe(dataFinalesMergeAlumnos.seleccionarColumnas(['titulo_secundario','nota']))

#datasetNuevo = Dataset()
#datasetNuevo.cargarDatos(ce,'alumnos.xlsx')
#datasetNuevo.eliminarPorGrupo('fecha_ingreso','legajo',lambda x: x is not None and x==x.min())
#datasetNuevo.filtrar(FiltroAND(FiltroMayor('fecha_ingreso','2003-01-01' ),FiltroMenor('fecha_ingreso','2017-12-31'))) #vamos a controlar el ingreso para que este entre dos fechas
#
#
#dataNuevo=datasetNuevo.datos()
#
#print(dataNuevo['fecha_ingreso'])
import numpy as np

X = np.random.rand(30,2)
print(X)

newClust = clustGen.ClusterKMeans()
newClust.generarCluster(dataCluster.toArray())


# hacer not de examen equivalente