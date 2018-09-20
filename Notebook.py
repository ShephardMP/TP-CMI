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

import os #para arreglar los problemas de path

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
    stringTabs=None #es una lista con las tabs en string
    top=None
    noteStyler=None
    
    
    
    def __init__(self,top,ventana=None,X=10,Y=126,WIDTH=960,HEIGHT=444):
        #SE CREA UN NUEVO ESTILO PARA LA NOTEBOOK
        self.refVentana=ventana
        self.stringTabs=[]
        
        self.__initCustomStyle__()
       
        
        
        self.note = ttk.Notebook(top,style='TNotebook') #se utiliza el estilo
        self.note.place(x=X,y=Y , width=WIDTH, height=HEIGHT)
        self.note.configure(width=300)
        self.note.configure(takefocus="")
        
        
        
        self.note.bind("<<NotebookTabChanged>>", self.setearYmostrar)
        self.note.bind("<ButtonPress-1>", self.botonCerrarPressed, True)
        self.note.bind("<ButtonRelease-1>", self.botonCerrarReleased, True)
        
    
        self.top=top
        #  self.Notebook.bind("<<NotebookTabChanged>>", adminInterfaz.buscarDataset(self.current))
                
    
    def mostrarTabActiva(self): #sin este metodo no puedo mandar parametros a la ventana
        if(self.current is not None): #si hay mas de una tab
            self.refVentana.mostrarTablaPorTab(self.get_tab_activa())
        else:
            self.refVentana.limpiarNotebook()
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
        if(len(self.note.tabs())>0):
            self.current=self.note.tab(tk.CURRENT)['text'] #obtiene la tab actual mediante la variable CURRENT
        else:
            self.current=None
    def get_tab_activa(self):
        return self.current
    
    def seleccionarTab(self,tab):
        
        self.note.select(self.stringTabs.index(tab)) 
        #es esperado que tab sea el id de la tab, es decir
        #si la tab dice 1, para seleccionarla mediante este metodo debo invocar con un 1
        
    def setearYmostrar(self,event):
        
        self.set_tab_activa()
        self.mostrarTabActiva()
        
    
        
        
    def borrarTab(self,tab):
        
        
        nombreTab=self.getTabText(tab)
        self.stringTabs.remove(nombreTab)
        
        self.note.forget(tab) #cuidado con esta linea, aparentemente genera un event NotebookTabChanged
        self.top.update() 
        #lo anterior es una estupidez que este aca, pero tras tiempo de debug se vio que el self.note.forget
        #genera un event pero solo al final del metodo a menos que se llame a top.update(). De esta
        #manera primero muestro y luego reparo las referencias en mainwindow
        #si no, primero se borrarn las referencias y luego se muestra y a veces puede ocasionar problemas
        
        self.refVentana.eliminarDataset(nombreTab)
       
        
        
    def getTabText(self,tabID):
        return self.note.tab(tabID)['text']
    
    def __initCustomStyle__(self):
        noteStyler = ttk.Style()
        noteStyler.configure('TNotebook', background=GREY, borderwidth=0)
       
        noteStyler.configure('TFrame', background=WHITE, foreground=WHITE, borderwidth=0)
        
        self.images = (
            tk.PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            tk.PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            tk.PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )
        
        noteStyler.element_create("close", "image", "img_close",("active", "pressed", "!disabled", "img_closepressed"),
                            ("active", "!disabled", "img_closeactive"),border=8, sticky='')
        noteStyler.layout("TNotebook.Tab", [
            ("TNotebook.tab", {
                "sticky": "nswe", 
                "children": [
                    ("TNotebook.padding", {
                        "side": "top", 
                        "sticky": "nswe",
                        "children": [
                                ("TNotebook.label", {"side": "left", "sticky": ''}),
                                ("TNotebook.close", {"side": "left", "sticky": ''}),
                                
                        
                    ]
                })
            ]
        })
    ])
        noteStyler.configure('TNotebook.Tab', background=GREYSUAVE, foreground=BLACK, lightcolor=BLACK, borderwidth=1)
        
    def botonCerrarPressed(self,event):
        element = self.note.identify(event.x, event.y)

        if "close" in element: #este close es el elemento creado en el styler Custom
            self.note.state(['pressed'])
           
            
    def botonCerrarReleased(self,event):
        if not self.note.instate(['pressed']):
            return

        element =  self.note.identify(event.x, event.y)
        index = self.note.index("@%d,%d" % (event.x, event.y))

       
        if "close" in element:
            self.borrarTab(index)

        self.note.state(["!pressed"])
       
        
        