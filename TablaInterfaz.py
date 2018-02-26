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
    
    def __init__(self,topLevel, columnas, cantidadFilasVisibles = 10):
                     #aca en columns hay que poner ids de la cantidad de columnas que queramos -1
        self.tree = ttk.Treeview(topLevel, columns=(columnas), height = cantidadFilasVisibles)
                                        
    def place(self, x=0, y=0, anchoPix = 600):
        self.tree.place(x = x, y = y, width = anchoPix)
        
    def nombrarColumnas(self, nombres):
        for x in range(0, len(nombres)):
            numCol = '#' + str(x)
            self.tree.heading(numCol, text= nombres[x])
            
    def insertarFila(self, valores):
        v0 = valores.pop(0)
        self.tree.insert("", tk.END, text = v0, values = valores)
        valores.insert(0, v0)
        
    def cargarDataset(self, dataset):
        self.nombrarColumnas(dataset.nombresColumnas())
        for i in range(0, dataset.cantidadFilas() - 1):
            self.insertarFila(dataset.getFila(i))