# -*- coding: utf-8 -*-
import io
import Categoria as cat

class ArchivoCategorias:
    categorias = []
    categoriasInvalidos = []

    def cargar(self, rutaArchivo):
        self.categorias = []
        self.categoriasInvalidos = []


        with io.open(rutaArchivo, "r") as archivo:
            lines = archivo.readlines()
            print(lines)


            for line in lines:
                atributo,valorAsociado,keys = line.split('..') #separa por los distintos campos de cada linea con ..
                keys = keys.replace('\n', '') #para eliminar los saltos de linea
                claves = keys.split(',') #las claves de cada categoria se separan por ,

                if (valorAsociado == 'invalid'):
                    categoriaInvalida = cat.Categoria(atributo, 'NAN', claves) #si es invalid, se le pone 'nan' de valor asociado
                    self.categoriasInvalidos.append(categoriaInvalida)
                else:
                    categoriaNueva = cat.Categoria(atributo, valorAsociado, claves)
                    self.categorias.append(categoriaNueva)


        return self.categorias, self.categoriasInvalidos
