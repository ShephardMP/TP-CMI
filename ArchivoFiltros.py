
import Filtro as fil

class ArchivoFiltros:

    def cargar(self, rutaArchivo, dataset):
        def decodificarFiltro(campo,cond,valor):
            valorInstanciado=None
            if(dataset.columnaNumerica(campo)):
                valorInstanciado=int(valor)
            else:
                valorInstanciado=str(valor)
                dataset.cambiarColumnaAString(campo)
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


        arch=open(rutaArchivo)
        lineas=arch.readlines()
        auxFiltro=None
        auxFiltroSimples={} #esto es un diccionario/mapa, la posta es que en la linea que aparece en el archivo hay un filtro
        #se puede dar la situacion que haya un NOT en la linea 2, y un filtro en la linea 3. luego por ser diccionario se puede conseguir facil ese filtro con la clave 3 y aplicarle el not
        auxFiltroCompuestos=[]
        OR=[]
        AND=[]# esta es una lista con indices, si en la lista aparece un 1, hay que hacer un and entre el filtro en la linea - y el filtro en la linea 2
        index=0
        for l in lineas:
            sacarSaltoDeLinea=l.split('\n')[0] #esto anda tenga o no un salto de linea
            if(len(l)<5): #chequeo que sea algun AND NOT OR

                condCompuesta=sacarSaltoDeLinea #decodifico si es and or not
                if(condCompuesta=='AND'):
                    AND.append(index)
                if(condCompuesta=='OR'):
                    OR.append(index)
            else:
                campo,condicion,valor=sacarSaltoDeLinea.split('..')
                auxFiltroSimples[index]=decodificarFiltro(campo,condicion,valor)
            index=index+1


        indexCompuesto=-1
        simplesCubiertos=[]

        for x in range(0,index):
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


        if(len(auxFiltroCompuestos)>1): #solo hacer OR si existe mas de un filtro AND
            auxFiltro=auxFiltroCompuestos[0]
            for x in range(1,len(auxFiltroCompuestos)):
                orAUX=fil.FiltroOR(auxFiltro,auxFiltroCompuestos[x])
                auxFiltro=orAUX

        else:
            if(len(auxFiltroCompuestos)==1):
                auxFiltro=auxFiltroCompuestos[0]

            else:
                auxFiltro=list(auxFiltroSimples.values())[0] #values retorna dict_values, que es una view, no una lista, por lo que hay que hacer la ista con list()

        arch.close()
        return auxFiltro
