
import Categoria as cat

class ArchivoCategorias:
    categorias = []
    categoriasInvalidos = []

    def cargar(self, rutaArchivo):
        self.categorias = []
        self.categoriasInvalidos = []

        archivo = open(rutaArchivo)
        while True:
            lines = archivo.readline()
            '''
            LEE LA SIGUIENTE LINEA, ESTA FORMA PERMITE UN PROCESAMIENTO MAS RAPIDO
            NO HAY QUE LEER TODO EL ARCHIVO DE UNA
            '''
            if not lines:
                break

            atributo,valorAsociado,keys = lines.split('..') #separa por los distintos campos de cada linea con ..
            keys = keys.replace('\n', '') #para eliminar los saltos de linea
            claves = keys.split(',') #las claves de cada categoria se separan por ,

            if (valorAsociado == 'invalid'):
                categoriaInvalida = cat.Categoria(atributo, 'nan', claves) #si es invalid, se le pone 'nan' de valor asociado
                self.categoriasInvalidos.append(categoriaInvalida)
            else:
                categoriaNueva = cat.Categoria(atributo, valorAsociado, claves)
                self.categorias.append(categoriaNueva)

        archivo.close()

        return self.categorias, self.categoriasInvalidos
