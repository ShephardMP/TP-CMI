from abc import ABCMeta, abstractmethod #para la creación de clases abstractas
import pandas as pandas #biblioteca para trabajar con data frames

class GuardadorDataframe:
    __metaclass__ = ABCMeta #Clase abstracta
    #clase pensada para guardar dataframes, en principio a excel pero que sea facilmente extensible
    @abstractmethod
    def guardarDataframe(self, dataframe, nombreArchivo): pass #Retorna un dataframe

"------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------"


class GuardadorDataframeExcel(GuardadorDataframe):
    "guarda el dataframe en un excel para psoterior uso"

    def guardarDataframe(self, dataframe, nombreArchivo):
        #NOTESE, SI EL DATAFRAM ES MUY GUASO PUEDE QUE TARDE EN GUARDARSE
        #ES BASICAMENTE UNA ESCRITURA A DISCO, PUEDE TARDAR MUCHO
        if('xlsx' not in nombreArchivo):
            nombreArchivo=nombreArchivo+'.xlsx'


        writer = pandas.ExcelWriter(nombreArchivo) #ej 'output.xlsx'

        dataframe.to_excel(writer,'Hoja1')

        writer.save()
