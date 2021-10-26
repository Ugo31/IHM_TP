#!/usr/bin/env/python
# coding: utf-8
# Mon agent ivy en python

from ivy.ivy import IvyServer
from tkinter import *
import time

class MyAgentParole(IvyServer):
    def __init__(self, name):
        self.init_vars()
        IvyServer.__init__(self,'MonAgentParole')
        self.name = name
        self.start('127.255.255.255:2010')
        self.bind_msg(self.handle_speak, '^speak (.*)')
        self.bind_msg(self.handle_sra, '^sra5 Parsed=action=(.*)where=(.*)form=(.*)color=(.*)localisation=(.*)Confidence=(.*)NP=(.*)Num_A=(.*)')
        self.bind_msg(self.handle_dolar, '^OneDolarIvy (.*)')
        print("python started")
        self.loop()

    def init_vars(self):
        #SRA5
        self.action = None
        self.where = None
        self.form = None
        self.color = None
        self.localisation = None
        #Pointage
        self.click = [0,0]#None
        #Formes
        self.forme = "Triangle"#None





    def loop(self):
        while(1):            
            
            if(self.action and "CREATE" in self.action): #and self.forme
                print("1")
                #Si on a ICI
                if(self.localisation and "THERE" in self.localisation):
                    print("2")
                    #On attend le click
                    if(self.click):
                        print("3")
                        #Si couleur
                        if(self.color):
                            print("4")
                            print("CREER + FORME + CLICK + COULEUR")
                            break
                        #Si pas couleur
                        else:
                            print("5")
                            print("CREER + FORME + CLICK + PAS COULEUR")            
                            break
                        
                #Si on a pas ICI
                else:
                    print("6")
                    #Si couleur
                    if(self.color):
                        print("7")
                        print("CREER + FORME + PAS CLICK + COULEUR")
                        break
                    #Si pas couleur
                    else:
                        print("8")
                        print("CREER + FORME + PAS CLICK + PAS COULEUR")
                        break


            elif(self.action == "DELETE"):
                pass
            elif(self.action == "MOVE"):
                pass
            elif(self.action == "QUIT"):
                pass
            else:
                print("action non impllementee")

            time.sleep(1)


            if(True):
                print("DLLs============================")
                print("action : %s"%self.action)
                print("where : %s"%self.where)
                print("form : %s"%self.form)
                print("color : %s"%self.color)
                print("localisation : %s"%self.localisation)


            

    #reco parole
    def handle_sra(self,*args):

        action=args[1]
        where=args[2]
        form=args[3]
        color=args[4]
        localisation=args[5]
        Confidence=float(args[6].replace(',','.'))
        NP=args[7]

##        
##        print("_______________handle_sra__________________")
##        print("action : %s"%action)
##        print("where : %s"%where)
##        print("form : %s"%form)
##        print("color : %s"%color)
##        print("localisation : %s"%localisation)
##        print("Confidence : %s"%Confidence)
##        print("NP : %s"%NP)

        if(Confidence>=0.6): 

            self.action = self.undef_to_None(action)
            self.where = self.undef_to_None(where)
            self.form = self.undef_to_None(form)
            self.color = self.undef_to_None(color)
            self.localisation = self.undef_to_None(localisation)

        else:
            print("repetez")
            a_dire = "parle mieux frere"
            self.send_msg('ppilot5 SaySSML=%s' %a_dire)




    def undef_to_None(self,x):
        if("undefined" in x):
            return None
        return x
        





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


