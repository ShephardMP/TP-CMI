# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 19:44:12 2018
ToolTip class proporcionado por http://www.voidspace.org.uk/python/weblog/arch_d7_2006_07_01.shtml
con modificaciones de @Mauro
"""

from tkinter import *

class ToolTip(object):

    def __init__(self, widget,text):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.delay=1200
        self.x = self.y = 0
        self.text=text
        

    def showtip(self):
        "muestra el tip"
    
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 75
        y = y + cy + self.widget.winfo_rooty() +75
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle",
                       "style", tw._w,
                       "help", "noActivates")
        except TclError:
            pass
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#FFFFFF", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"),
                      wraplength=200)
        label.pack(ipadx=1)
        self.id = self.widget.after(500, self.showtip)


    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

    def enter(self,event=None):
        if(self.id is None):
            self.id = self.widget.after(self.delay, self.showtip)
            
    def leave(self,event=None):
        if (self.id is not None):
            id=self.id
            self.id=None
            self.widget.after_cancel(id)
        self.hidetip()
            
def createToolTip(widget, text):
    toolTip = ToolTip(widget,text)
    def enter(event):
        toolTip.enter(event)
        
    def leave(event):
        toolTip.leave(event)
    widget.bind('<Enter>',enter)
    widget.bind('<Leave>',leave)
