# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 15:19:38 2018

@author: tomy-
"""

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

import tkinter as tk

class TablaInterfaz:
    tree = None
    scrollbarX = None
    scrollbarY = None
    alturaPix = None

    def __init__(self,topLevel, columnas, cantidadFilasVisibles = 10, scrollbarHorizontal = True, scrollbarVertical = True):
                     #aca en columns hay que poner ids de la cantidad de columnas que queramos -1
        self.tree = ttk.Treeview(topLevel, columns=(columnas), height = cantidadFilasVisibles)
        self.alturaPix = 25 + cantidadFilasVisibles * 20;
        for c in columnas:
            self.tree.column(c, width = 100)
        if (scrollbarHorizontal):
            self.scrollbarX = ttk.Scrollbar(topLevel, orient="horizontal", command=self.tree.xview)
            self.tree.configure(xscrollcommand=self.scrollbarX.set)
        if (scrollbarVertical):
            self.scrollbarY = ttk.Scrollbar(topLevel, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscrollcommand=self.scrollbarY.set)

    def place(self, x=0, y=0, anchoPix = 600):
        self.tree.place(x = x, y = y, width = anchoPix)
        if (self.scrollbarX != None):
            self.scrollbarX.place(x=x, y = self.alturaPix + y, width = anchoPix);
        if (self.scrollbarY != None):
            self.scrollbarY.place(x = x+anchoPix, y = y, height = self.alturaPix);

    def nombrarColumnas(self, nombres):
        for x in range(0, len(nombres)):
            numCol = '#' + str(x)
            self.tree.heading(numCol, text= nombres[x])

    def insertarFila(self, valores):
        self.tree.insert("", tk.END, text = valores[0], values = valores[1:len(valores)])

    def cargarDataset(self, dataset):
        self.nombrarColumnas(dataset.nombresColumnas())
        dataframe = dataset.datos()
        counter = 0
        for fila in dataframe.itertuples():
            if counter > 15000:
                break
            self.insertarFila(fila[1:len(fila)])
            counter += 1
