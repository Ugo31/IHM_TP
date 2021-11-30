#!/usr/bin/env python3
import math
from tkinter import Tk, Canvas, Frame, BOTH
from  collections import deque
import random

class Forme:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.shape = None
        self.type  = None

    def move(self, x, y):
        self.x = x
        self.y = y

    def get_dist(self,forme):
        if(not forme):
            return -1
        return math.sqrt(pow(self.x-forme.x,2)+pow(self.y-forme.y,2))

    def is_same_color(self,color):
        return color.lower() in self.color.lower() or self.color.lower() in color.lower()

    def is_same_shape(self,ptype):
        return ptype.lower() in self.type.lower() or self.type.lower() in ptype.lower()

    def get_dist(self,_x,_y):
        return math.sqrt(pow(self.x-_x,2)+pow(self.y-_y,2))

    def is_in(self,x,y):
        raise NotImplementedError("Please Implement this method")

class Cercle(Forme):
    def __init__(self, x, y, r, color):
        super().__init__(x, y, color)
        self.r = r
        self.type ="CIRCLE"

    def draw(self, canvas):
        self.shape = canvas.create_oval(
            self.x, self.y, self.x + self.r, self.y + self.r, fill=self.color
        )

    def is_in(self,x,y):
        return (x-self.x)**2 + (y - self.y)**2 < self.r**2



class Rectangle(Forme):
    def __init__(self, x, y, s, color):
        super().__init__(x, y, color)
        self.s = s
        self.type ="RECTANGLE"

    def draw(self, canvas):
        self.shape =  canvas.create_rectangle(self.x, self.y, self.x+self.s, self.y+self.s, fill=self.color)

    def is_in(self,x,y):
        return self.x<x<self.x+self.s and self.y<y<self.y+self.s


class Triangle(Forme):
    def __init__(self, x, y, s, color):
        super().__init__(x, y, color)
        self.s = s
        self.x1 = self.x - self.s
        self.y1 = self.y + self.s

        self.x2 = self.x + self.s
        self.y2 = self.y

        self.x3 = self.x - self.s
        self.y3 = self.y - self.s
        self.type ="TRIANGLE"

    def draw(self, canvas):
        points = [
            self.x1,
            self.y1,
            self.x2,
            self.y2,
            self.x3,
            self.y3
        ]
        self.shape =  canvas.create_polygon(points, fill=self.color)

    def area(self,_x1, _y1, _x2, _y2, _x3, _y3):
        return abs((_x1 * (_y2 - _y3) + _x2 * (_y3 - _y1)
                    + _x3 * (_y1 - _y2)) / 2.0)
    
    def is_in(self,x, y):
        A  = self.area(self.x1, self.y1, self.x2, self.y2, self.x3, self.y3)
        A1 = self.area(x, y, self.x2, self.y2, self.x3, self.y3)
        A2 = self.area(self.x1, self.y1, x, y, self.x3, self.y3)
        A3 = self.area(self.x1, self.y1, self.x2, self.y2, x, y)
        if(A == A1 + A2 + A3):
            return True
        else:
            return False

class Interface(Frame):
    def __init__(self):
        super().__init__()

        self.root = Tk()
        self.root.geometry("400x250+300+300")
        self.root.withdraw()

        self.MODE = None
        self.canvas = Canvas(self)
        self.initUI()

        self.shape_list = []

        self.lastclicks = None
        self.selected_form = None
        self.hyp_form = [None,None,None]
        self.is_destroyed = False

    def destroyINT(self):
        self.root.destroy()
        self.destroy()
        self.is_destroyed = True
        exit(0)

    def changemode(self,mode):
        self.MODE = mode

    def select_shape(self,pshape):
        self.selected_form = pshape

    def is_shape_selected(self):
        return self.selected_form!=None

    def get_selected(self):
        return self.selected_form

    def delete_selected(self):
        self.shape_list.remove(self.selected_form)

    def get_3_closest(self,x,y):
        dq = [None,None,None]
        
        for s in self.shape_list:
            dist = s.get_dist(x,y)
            dist1 = 99999999999999999
            dist2= 99999999999999999
            dist3 = 99999999999999999
            if(dq[0]):
                dist1 = dq[0].get_dist(x,y)
            if(dq[1]):
                dist2 = dq[1].get_dist(x,y)
            if(dq[2]):
                dist3 = dq[2].get_dist(x,y)
            if(dist<50):

                if(dist1>dist):
                    dq[2] =dq[1]
                    dq[1] =dq[0]
                    dq[0] = s

                elif(dist2>dist):
                    dq[2] =dq[1]
                    dq[1] =s

                elif(dist3>dist):
                    dq[2] =s
        return dq






    def initUI(self):
        self.master.title("Lines")
        self.pack(fill=BOTH, expand=1)
        self.canvas.pack(fill=BOTH, expand=1)
        self.canvas.bind("<ButtonRelease-1>", self.callback)
        self.root.protocol("WM_DELETE_WINDOW", self.destroyINT)

    def clear_all(self):
        self.lastclicks = None
        self.selected_form = None
        self.hyp_form = [None,None,None]

    def callback(self, args):
        print(args.x, " | ", args.y)
        self.lastclicks = [args.x, args.y]
        self.hyp_form = self.get_3_closest(args.x, args.y)
        print(self.hyp_form)

    def get_last_click(self):
        return self.lastclicks

    def clear_last_click(self):
        self.lastclicks = None

    def refresh(self):
        if(not self.is_destroyed):
            self.canvas.delete("all")
            for s in self.shape_list:
                s.draw(self.canvas)
            self.root.update_idletasks()
            self.root.update()

    def get_all_type(self,ptype=None):
        if(ptype):
            index = 0
            returned = []
            for s in self.shape_list:
                if(s.is_same_shape(ptype)):
                    returned.append(s)
                    index+=1
            if(index):
                return returned
            else:
                return None
            
        else:
            return self.shape_list


    def create(self,shape,x=None,y=None,color=None):

        appliedcolor = None
        if(not color):
            appliedcolor = "blue"
        elif("red" in color.lower()):
            appliedcolor = 'red'
        elif("blue" in color.lower()):
            appliedcolor = 'blue'
        elif("orange" in color.lower()):
            appliedcolor = 'orange'
        elif("yellow" in color.lower()):
            appliedcolor = 'yellow'
        elif("green" in color.lower()):
            appliedcolor = 'green'
        elif("purple" in color.lower()):
            appliedcolor = 'purple'
        elif("dark" in color.lower()):
            appliedcolor = 'black'
        else:
            print('err, Unknow color. COLOR IS =',color)


        if(not x):
            x = random.randint(0, self.canvas.winfo_reqwidth()-30)
        if(not y):
            y = random.randint(0, self.canvas.winfo_reqheight()-30)
        if("triangle" in shape.lower()):
            s = Triangle( x, y, 20, appliedcolor)
            self.shape_list.append(s)
        elif("rectangle" in shape.lower()):
            s = Rectangle( x, y, 30, appliedcolor)
            self.shape_list.append(s)

        elif("circle" in shape.lower()):
            s = Cercle( x, y, 30, appliedcolor)
            self.shape_list.append(s)
        else:
            print('err, Unknow shape. SHAPE IS =',shape.lower())
            exit(1)



def main():

    ex = Interface()
    ex.changemode("move")
    ex.create("triangle")
    ex.create("triangle",20,20)
    ex.create("triangle",40,40)
    ex.refresh()

if __name__ == "__main__":
    main()
