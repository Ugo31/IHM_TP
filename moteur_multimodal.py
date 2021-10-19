#!/usr/bin/env/python
# coding: utf-8
# Mon agent ivy en python

from ivy.ivy import IvyServer
from tkinter import *

class MyAgentParole(IvyServer):
    def __init__(self, name):
        IvyServer.__init__(self,'MonAgentParole')
        self.name = name
        self.start('127.255.255.255:2010')
        self.bind_msg(self.handle_speak, '^speak (.*)')
        self.bind_msg(self.handle_sra, '^sra5 Parsed=(.*) Confidence=(.*) NP=.*')
        self.bind_msg(self.handle_dolar, '^OneDolarIvy (.*)')


    #reco parole
    def handle_sra(self, agent, arg):
        #arg=arg.replace('�','c') #car utf8 pose pbm
        print("_______________handle_sra__________________")
        print("test : %s"%arg)
        if(arg.find("Event")==-1): 
            print("OK")
            liste = arg.split("Text=")
            if(len(liste)>1): # le if est la pour enlever le is ready
                test = liste[1].split("Confidence=")
                mots = test[0]
                confiance = float(test[1].replace(',','.'))
                print("======")
                print(mots)
                print(confiance)
        else:
            print("repetez")
            a_dire = "parler mieux frere"
            self.send_msg('ppilot5 SaySSML=%s' %a_dire)


    #synth parole
    def handle_speak(self, agent, arg):
        self.send_msg('test = %s' %arg)
        self.send_msg('ppilot5 SaySSML=%s' %arg)
        
    #reco formes
    def handle_dolar(self, agent, arg):
        print("onedolar : %s"%arg)
        liste = arg.split()
        template = liste[0].split('=')[1]
        confidence = float(liste[1].split('=')[1])
        print("======")
        print(template)
        print(confidence)

    

a=MyAgentParole('HelloBack')


