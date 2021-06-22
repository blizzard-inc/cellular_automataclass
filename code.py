import numpy

class cell:
    def __init__(self,state:):
        self.state=state

class board(numpy.array):
    def __init__(self,border,*args,**kwargs):
        self.border=border
        super().__init__(self,*args,**kwargs)
        
    def advance(self,rule: rule)
        

class rule:
    def __init__(self,death,live,border :borderrules):
        self.birth=birth
        self.death=death
        self.live=live
class sumrule(rule):
    def __init__(self,live,death,birth,neighbours,border):
      #neem live=[2,3]
      #death=[0,1,4,5,6,7,8]
      #birth=[3]
      super().__init__(self,deaths,lives,border)
    
class borderrules:
    def __init__(self,):

((0,0),(0,1),(-1,0),)
list(1,2,2,3)
zeros(3)
list(0,0,0)
