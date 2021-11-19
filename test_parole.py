#!/usr/bin/env/python
# coding: utf-8
# Mon agent ivy en python

from ivy.ivy import IvyServer
from tkinter import *
from PIL import Image, ImageTk

class MyAgent(IvyServer):
    def __init__(self, name):
        IvyServer.__init__(self,'MonAgentPython')
        self.name = name
        self.start('127.255.255.255:2010')
        self.bind_msg(self.handle_hello, '^speak (.*)')
        self.bind_msg(self.handle_sra, '^sra5 (.*)')

    def handle_sra(self, agent, arg):
        arg2 = arg.decode("utf-8")
        print("test : %s"%arg2)
        
    def handle_hello(self, agent, arg):
        self.send_msg('test = %s' %arg)
        self.send_msg('ppilot5 SaySSML=%s' %arg)
	
a=MyAgent('HelloBack')



#root = Tk()      
#canvas = Canvas(root, width = 300, height = 300)      
#canvas.pack()      
#img = PhotoImage(Image.open("cafe.png"))
#canvas.create_image(20,20, anchor=NW, image=img)      
#mainloop()   

