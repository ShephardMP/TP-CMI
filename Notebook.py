# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 17:20:16 2018

@author: Mauro
"""
try:
    import Tkinter as Tk
except ImportError:
    import tkinter as tk
try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

BLACK = 'black'
WHITE = 'white'
RED = 'red'
GREY='#d9d9d9'
GREYSUAVE='#e8e8e8'
COLOR_1 = '#2E2E2E'
COLOR_2 = '#8A4B08'
COLOR_3 = '#DF7401'
HIGHLIGHT='#E0EAED'

class Notebook():
    note=None
    current=None
    refVentana=None
    stringTabs=None
    def __init__(self,top,ventana=None,X=10,Y=126,WIDTH=960,HEIGHT=444):
        #SE CREA UN NUEVO ESTILO PARA LA NOTEBOOK
        self.refVentana=ventana
        self.stringTabs=[]
        noteStyler = ttk.Style()
        noteStyler.configure('TNotebook', background=GREY, borderwidth=0)
        noteStyler.configure('TNotebook.Tab', background=GREYSUAVE, foreground=BLACK, lightcolor=BLACK, borderwidth=1)
        noteStyler.configure('TFrame', background=WHITE, foreground=WHITE, borderwidth=0)
        
        
        self.note = ttk.Notebook(top,style='TNotebook') #se utiliza el estilo
        self.note.place(x=X,y=Y , width=WIDTH, height=HEIGHT)
        self.note.configure(width=300)
        self.note.configure(takefocus="")
        
        
        
        self.note.bind("<<NotebookTabChanged>>", self.setearYmostrar)
    
        
        #  self.Notebook.bind("<<NotebookTabChanged>>", adminInterfaz.buscarDataset(self.current))
                
    def mostrarTabActiva(self): #sin este metodo no puedo mandar parametros a la ventana
        if(len(self.note.tabs())>1): #si hay mas de una tab
            self.refVentana.mostrarTablaPorTab(self.get_tab_activa())
        
    def getNotebook(self):
        return self.note #de tipo ttk.Notebook
    
    def addTab(self,texto='',pad=3):
        new_tab=ttk.Frame(self.note)
        self.note.add(new_tab,text=texto, padding=pad)
        self.stringTabs.append(texto)
        self.set_tab_activa()
        self.seleccionarTab(texto)
       # print ("activa notebook",self.get_tab_activa())
        
  
        
    def set_tab_activa(self):
        self.current=self.note.tab(tk.CURRENT)['text'] #obtiene la tab actual mediante la variable CURRENT
        
    def get_tab_activa(self):
        return self.current
    
    def seleccionarTab(self,tab):
        
        self.note.select(self.stringTabs.index(tab)) 
        #es esperado que tab sea el id de la tab, es decir
        #si la tab dice 1, para seleccionarla mediante este metodo debo invocar con un 1
        
    def setearYmostrar(self,event):
        self.set_tab_activa()
        self.mostrarTabActiva()