from ivy.ivy import IvyServer
import time
from interface import Interface
import sys
class MyAgentParole(IvyServer):
    def __init__(self, name):

        self.interface = Interface()
        self.interface.create("triangle",200,200,'orange')
        self.interface.create("rectangle",200,210,'red')

        self.interface.create("rectangle",20,20,'red')
        self.interface.create("circle",100,100,'green')
        self.interface.create("circle",120,100,'dark')

        self.init_vars()
        IvyServer.__init__(self,'MonAgentParole')
        self.name = name
        self.start('127.255.255.255:2010')
        self.bind_msg(self.handle_speak, '^speak (.*)')
        self.bind_msg(self.handle_sra, '^sra5 Parsed=action=(.*)where=(.*)form=(.*)color=(.*)localisation=(.*)Confidence=(.*)NP=(.*)Num_A=(.*)')
        self.bind_msg(self.handle_dolar, '^OneDolarIvy Template=(.*)Confidence=(.*)')
        print("python started")
        self.actionDelay = 4000
        self.programspeed = 300

        self.loop()

    def init_vars(self):
        #SRA5
        self.action = None
        self.color = None
        #Pointage
        self.click = None#None
        #Formes
        self.form = None
        self.tickswaited = 0
        self.interface.clear_all()
        self.err = None
        

    def isReady(self):
        return self.tickswaited*self.programspeed > self.actionDelay



    def loop(self):
        while(1):
            self.click = self.interface.get_last_click()



            #//////////////////////////////////////////////////////////////////////////////////////////
            # SELECTION DE FORME POUR DELETE OU MOVE
            # Cas ou le click est defini 
            if(not self.interface.is_shape_selected()):
                if(self.click):
                    # Cas ou au moins une forme est non nulle
                    if(self.interface.hyp_form and self.interface.hyp_form[0]):
                        # compte combien de formes potentielles sont selectionees
                        l=0
                        if(self.interface.hyp_form[0]):
                            l+=1
                        if(self.interface.hyp_form[1]):
                            l+=1
                        if(self.interface.hyp_form[2]):
                            l+=1
                        #si une seule forme
                        if(l==1):
                            #on la selectionne
                            print("SELECTED",self.interface.hyp_form[0])
                            self.interface.select_shape(self.interface.hyp_form[0])
                            self.click = None
                            self.interface.clear_last_click()
                            self.err = "NO ERRORS"
                        elif(self.color):
                        #si plusieures formes, on doit faire avec la couleur pour discrimier
                            #on check celles de la meme couleur
                            all_same_colors = []
                            for s in self.interface.hyp_form:
                                if(s and s.is_same_color(self.color)):
                                    all_same_colors.append(s)
                            #si il y en a que une on la select
                            if(len(all_same_colors)==1):
                                print("SELECTED",all_same_colors[0])
                                self.interface.select_shape(all_same_colors[0])
                                self.click = None
                                self.interface.clear_last_click()
                                self.err = "NO ERRORS"
                            #si il y en a que plusieures de la meme couleur mais on precise la forme
                            elif(len(all_same_colors)>1 and self.form):
                                all_same_shape = []
                                for s in self.interface.hyp_form:
                                    if(s and s.is_same_shape(self.form)):
                                        all_same_shape.append(s)
                                if(len(all_same_shape)==1):
                                    print("SELECTED",all_same_shape[0])
                                    self.interface.select_shape(all_same_shape[0])
                                    self.click = None
                                    self.interface.clear_last_click()
                                    self.err = "NO ERRORS"
                                elif(len(all_same_shape)==0):
                                    self.err = "ERR no candidates with this SHAPE and COLOR"
                                else:
                                    self.err = "ERR cant discrimiate enought with CLICK even with the SHAPE and COLOR"

                            elif(len(all_same_colors)==0):
                                self.err = "ERR no candidates with this COLOR"
                            else:
                                self.err = "ERR cant discrimiate enought with CLICK even with the color,try adding shape too"


                        elif(self.form):
                            all_same_shape = []
                            for s in self.interface.hyp_form:
                                if(s and s.is_same_shape(self.form)):
                                    all_same_shape.append(s)
                            if(len(all_same_shape)==1):
                                print("SELECTED",all_same_shape[0])
                                self.interface.select_shape(all_same_shape[0])
                                self.click = None
                                self.interface.clear_last_click()
                                self.err = "NO ERRORS"
                            elif(len(all_same_shape)==0):
                                self.err = "ERR no candidates with this SHAPE"
                            else:
                                self.err = "ERR cant discrimiate enought with CLICK even with the shape,try adding color too"


                        else:
                            self.err = "ERR cant discrimiate enought with CLICK, try adding color OR/and shape"
                    else:
                        self.err="ERR click on a shape to select it"
                #Cas où le type de  forme est précisée par la parole mais pas de click
                elif(self.form):
                    allype = self.interface.get_all_type(self.form)
                    if(allype):
                        if(len(allype)>1):
                            #Cas où multiples formes de  ce type
                            if(self.color):
                                #on check celles de la meme couleur
                                all_same_colors = []
                                for s in allype:
                                    if(s and s.is_same_color(self.color)):
                                        all_same_colors.append(s)
                                #si il y en a que une on la select
                                if(len(all_same_colors)==1):
                                    print("SELECTED",all_same_colors[0])
                                    self.interface.select_shape(all_same_colors[0])
                                    self.click = None
                                    self.interface.clear_last_click()
                                    self.err = "NO ERRORS"
                                else:
                                    self.err="ERR cant discrimiate enought even with the color"
                            else:
                                self.err="ERR cant discrimiate enought, try adding color"


                        elif(len(allype)==1):
                            #Cas où la forme est la seule de  ce type 
                            self.interface.select_shape(allype[0])
                            print("SELECTED",allype[0])
                            self.click = None
                            self.interface.clear_last_click()
                            self.err = "NO ERRORS"
                        else:
                            self.err="ERR no selected shapes match the form len="
                    else:
                        self.err="ERR no shapes like that detected bro"













            if(self.action and self.form and "create" in self.action.lower()): #and self.forme
                #Si on a a click
                if(self.click):
                    #Si couleur
                    if(self.color):
                        self.err = "CREER + FORME + CLICK + COULEUR"
                        self.interface.create(self.form,x=self.click[0],y=self.click[1],color=self.color)
                        self.init_vars()
                    #Si pas couleur
                    else:
                        self.err = "CREER + FORME + CLICK + PAS COULEUR"
                        self.tickswaited+=1       
                        if(self.isReady()):
                            self.interface.create(self.form,x=self.click[0],y=self.click[1])
                            self.init_vars()
    
                #Si on a pas click
                else:
                    #Si couleur
                    if(self.color):
                        self.err = "CREER + FORME + PAS CLICK + COULEUR"
                        self.tickswaited+=1
                        if(self.isReady()):
                            self.interface.create(self.form,color=self.color)
                            self.init_vars()
                    #Si pas couleur
                    else:
                        self.err = "CREER + FORME + PAS CLICK + PAS COULEUR"
                        self.tickswaited+=1
                        if(self.isReady()):
                            self.interface.create(self.form)
                            self.init_vars()

            elif(self.action and "delete" in self.action.lower() and self.interface.is_shape_selected()):
                self.interface.delete_selected()
                self.init_vars()

            elif(self.action and "move" in self.action.lower() and self.interface.is_shape_selected() and self.click):
                self.interface.get_selected().move(x=self.click[0],y=self.click[1])
                self.init_vars()
            
            elif(self.action and "quit" in self.action.lower()):
                sys.exit()         
            else:
                pass





            self.interface.refresh()

            if(True):
                print("DLLs============================")
                print("action : %s"%self.action)
                print("form : %s"%self.form)
                print("color : %s"%self.color)
                print("localisation : %s"%self.click)
                print("waiting : ",self.isReady())
                print("selected shape : ",self.interface.get_selected())
                print("LOG : ",self.err)

                

            
            time.sleep(self.programspeed/1000)

            
    # Check dans la liste des formes possibles celle qui a cette couleur
    def color_filter(self,hypothetic_form, color):
        for form in hypothetic_form :
            if form.color == color:
                return form
    
    def inspect_object_list(self):
        i = 0
        form_correspond = []
        for object in self.interface.shape_list:
            if object.type == self.form : 
                form_correspond.append(object)
        if len(form_correspond) == 0:
            time.sleep(1)
            print( "Aucun(e) " + str(self.form) + " dans l'interface.")
        if len(form_correspond) == 1:
            self.interface.selected_form = form_correspond[0]
            # Si on en a trouvé qu'un seul, on le valide en renvoyant True
            return True
        else :
            return False
                
    #reco parole
    def handle_sra(self,*args):
        action=args[1]
        color=args[4]
        Confidence=float(args[6].replace(',','.'))
        NP=args[7]

        if(Confidence>=0.6): 
            self.action = self.undef_to_None(action)
            self.color = self.undef_to_None(color)
            print("action : %s"%self.action)
            print("color : %s"%self.color)


        else:
            print("repetez")
            a_dire = "parle mieux frere"
            self.send_msg('ppilot5 SaySSML=%s' %a_dire)




    def undef_to_None(self,x):
        if(not x):
            return None
        if("undefined" in x):
            return None
        return x
        





    #synth parole
    def handle_speak(self, agent, arg):
        self.send_msg('test = %s' %arg)
        self.send_msg('ppilot5 SaySSML=%s' %arg)
        
    #reco formes
    def handle_dolar(self, *args):
        print("onedolar : %s",args)
        #liste = args.split()
        #self.form = liste[0].split('=')[1]
        #self.confidence = float(liste[1].split('=')[1])
        self.form = str(args[1])
        self.confidence = float(args[2])
        print("======")
        print(self.form)
        print(self.confidence)
        

    



def main():

    a=MyAgentParole('HelloBack')

if __name__ == "__main__":
    main()
