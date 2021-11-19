from ivy.ivy import IvyServer
import time
from interface import Interface

class MyAgentParole(IvyServer):
    def __init__(self, name):

        self.interface = Interface()
        #self.interface.create("triangle")
        #self.interface.create("rectangle",20,20)
        #self.interface.create("triangle",40,40)

        self.init_vars()
        IvyServer.__init__(self,'MonAgentParole')
        self.name = name
        self.start('127.255.255.255:2010')
        self.bind_msg(self.handle_speak, '^speak (.*)')
        self.bind_msg(self.handle_sra, '^sra5 Parsed=action=(.*)where=(.*)form=(.*)color=(.*)localisation=(.*)Confidence=(.*)NP=(.*)Num_A=(.*)')
        self.bind_msg(self.handle_dolar, '^OneDolarIvy Template=(.*)Confidence=(.*)')
        print("python started")
        self.loop()

    def init_vars(self):
        #SRA5
        self.action = "MOVE"
        self.color = None
        #Pointage
        self.click = None#None
        #Formes
        self.form = None
        





    def loop(self):
        while(1):
            self.click = self.interface.get_last_click()

            if(self.action and self.form and "CREATE" in self.action): #and self.forme
                print("1")
                #Si on a a click
                if(self.click):
                    print("3")
                    #Si couleur
                    if(self.color):
                        print("4")
                        print("CREER + FORME + CLICK + COULEUR")
                        self.interface.create(self.form,self.click[0],self.click[1],self.color)
                    #Si pas couleur
                    else:
                        print("5")
                        print("CREER + FORME + CLICK + PAS COULEUR")            
                        self.interface.create(self.form,x=self.click[0],y=self.click[1])
    
                #Si on a pas click
                else:
                    print("6")
                    #Si couleur
                    if(self.color):
                        print("7")
                        print("CREER + FORME + PAS CLICK + COULEUR")
                        self.interface.create(self.form,color=self.click[1])

                    #Si pas couleur
                    else:
                        print("8")
                        print("CREER + FORME + PAS CLICK + PAS COULEUR")
                        self.interface.create(self.form)



            elif(self.action == "DELETE"):
                pass
            elif(self.action == "MOVE"):
                # Tant que la position n'a pas été definie, ne rien faire.
                if(self.undef_to_None(self.click) != None):

                    #Cas où la forme est précisée 
                    if(self.undef_to_None(self.form) != None):
                        find = self.inspect_object_list()
                        
                    #Cas où on precise juste forme à deplacer ou "ça" avec un click
                    if(self.interface.selected_form != None):
                        self.interface.selected_form.move_form(self.click)
                        break
                    else :
                        print("SVP Indiquez une couleur pour que l'on puisse choisir la forme")
                        while(self.color == None):
                            time.sleep(0.1)
                        self.interface.selected_form = self.color_filter(self.interface.hyp_form,self.color)
            elif(self.action == "QUIT"):
                pass
            else:
                pass
                #print("action non impllementee")

            self.interface.refresh()

            if(True):
                print("DLLs============================")
                print("action : %s"%self.action)
                print("form : %s"%self.form)
                print("color : %s"%self.color)
                print("localisation : %s"%self.click)


            
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
