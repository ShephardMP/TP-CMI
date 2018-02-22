# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 23:50:49 2018

@author: tomy-
"""

class Categoria:
    keys = []
    nombreAtributo = None
    valorAsociado = None

    def __init__(self, nombreAtributo, valorAsociado = 0, claves=[]):
        self.nombreAtributo = nombreAtributo
        self.valorAsociado = valorAsociado
        self.keys=[] #sin esto ES RE FLASHERO LO QUE PASA, se van concatenando las keys. Es como si la estructura esta fuera compartida y a la vez no.
        self.agregarKeys(claves)

    def getValorAsociado(self):
        return self.valorAsociado

    def getNombreAtributo(self):
        return self.nombreAtributo

    def getKeys(self):
        return self.keys

    def setValorAsociado(self, valor):
        self.valorAsociado = valor

    def setNombreAtributo(self, nombre):
        self.nombreAtributo = nombre

    def agregarKeys(self, nuevasKeys):
        self.keys[0:0] = nuevasKeys #Se insertan las nuevas keys al principio