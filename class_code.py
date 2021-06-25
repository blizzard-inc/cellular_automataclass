import numpy as np
import time

class neighbourhoodcl:
    def __init__(self,reladresses:list):
        self.neighbours=reladresses
    def __getitem__(self,index):
        return self.neighbours[index]
    def __setitem__(self,index,val):
        self.neighbours[index]=val

class edgerule:
    """
    klasse voor de randvoorwaarden.
    """
    def __init__(self,type:str=None,const=None,offset:tuple=None):
        if not const:
            const=0
        if not offset:
            offset=(0,)
        if not type:
            type="wrap"
        self.type=type
        self.offset=offset
    def __call__(self,adress,shape):
        offsetcomp=list(self.offset)
        if len(adress)>len(self.offset):
            offsetcomp+=[0]*(len(adress)-len(self.offset))
        offsetcomp=tuple(offsetcomp)
        if all([0<=adress[i]+offsetcomp[i]<shape[i] for i in range(len(adress))]):
            return False, tuple(adress)
        elif type=='D':
            return True, const
        elif type=='N':
            forwardadress=[(0 if adress[i]+offsetcomp[i]<0 else shape[i]-1) for i in range(len(adress))]
            return False, tuple(forwardadress)
        else:
            forwardadress=[(adress[i]+offsetcomp[i])%shape[i] for i in range(len(adress))]
            return False, tuple(forwardadress)

class rule:
    def __init__(self,neighbourhood:neighbourhoodcl):
        self.neighbourhood=neighbourhood
    def __call__(self,neighbours):
        raise NotImplementedError

class board:
    """
        dit is de klasse van een bord, met regels voor hoe tegels verbinden
        (dus met regels voor randvoorwaarden).
    
        matrix:array van alle cellen, met als waarden integers.
        edgerules
        een functie die bepaalt hoe de randen zich gedragen.
        api: returnt een 2-tupel
        eerste component is boolean:
            als true: waarde is tweede component.
                anders: waarde is waarde van cel met als adres tweede component.
    """
    def __init__(self,matrix :np.array, edgerules):
        self.edgerules=edgerules
        self.cells=matrix
    def neighbourhood(self,index,adresses):
        neighbours=[]
        for reladress in adresses:
            absadress = [index[i]+reladress[i] for i in range(len(index))]
            constant, val= self.edgerules(absadress,self.cells.shape)
            if constant:
                neighbour= val
            else:
                neighbour=self.cells[val]
            neighbours+=[neighbour]
        return neighbours
        
    def nextstate(self,nextstatefunc:rule):
        nextboard=emptyboard(self.cells.shape,self.edgerules)
        adressbook=nextstatefunc.neighbourhood
        for index in np.ndenumerate(self.cells):
            neighbours=self.neighbourhood(index[0],adressbook)
            nextboard.cells[index[0]]=nextstatefunc(neighbours)
            
        self.cells=nextboard.cells
        return nextboard.cells
        
    def advance(self,steps:int,nextstatefunc:rule):
        pass
class emptyboard(board):
    def __init__(self,dimensions,edgerules):
        cells=np.zeros(dimensions,int)
        super().__init__(cells,edgerules)

class totalistic(rule):
    """class die specifieke regels makkelijker creëert.
        deze class maakt regels waar de positie van de buren niet uit maakt
        adresses: lijst relatieve coordinaten waarover de som genomen wordt
        birth: lijst van sommen waarbij de cel levend word
        live: lijst van sommen waarbij de cel levend blijft.
        !! bij deze sommen wordt de centrale cel niet meegerekend
    """
    def __init__(self,neighbourhood:neighbourhoodcl,birth:list,live:list):
        self.birth=birth
        self.live=live
        super().__init__(neighbourhood)
    def __call__(self, neighbours:list):
        birth = neighbours[0]==0 and sum(neighbours) in self.birth
        live = neighbours[0]==1 and sum(neighbours)-1 in self.live
        if birth or live:
            return 1
        return 0

class moorehood(neighbourhoodcl):
    def __init__(self,dim:int=None,length:int=None):
        if not dim:
            dim=2
        if dim<1:
            raise ValueError
        if not length:
            length=1
        if length<0:
            raise ValueError
        
        if length==0:
            neighbours=[[0]*dim]
        else:
            neighbours=[[]]
            for _ in range(dim):
                for number in range(len(neighbours)):
                    current_house=neighbours[number]
                    neighbours[number]=current_house+[0]
                    for d in range(1,length+1):
                        neighbours+=[current_house+[d],current_house+[-d]]
        super().__init__(neighbours)

class neumannhood(neighbourhoodcl):
    def __init__(self,dim,length):
        if length==0:
            neighbours=[[0]*dim]
        else:
            neighbours=[[]]
            for _ in range(dim):
                for number in range(len(neighbours)):
                    current_house=neighbours[number]
                    neighbours[number]=current_house+[0]
                    distance=sum([abs(coord) for coord in current_house])
                    for d in range(1,length-distance+1):
                        neighbours+=[current_house+[d],current_house+[-d]]
        super().__init__(neighbours)
'''   
life=totalistic([(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)],[3],[2,3])
torus=edgerule()
testboard=emptyboard((5,5),torus)
testboard.cells[1,1]=1
testboard.cells[1,2]=1
testboard.cells[2,2]=1
testboard.cells[2,3]=1
testboard.cells[3,1]=1
#print(testboard.cells)
#print(testboard.nextstate(life))
'''
'''
if __name__=='__main__':
    print('starting program\n')
    time.sleep(4)
    if input('do you want to build a cellular automata?\n y/n  ')=='y':
        print('for game of life, type 1')
        print('for a custom cellular automata, press 2')
        if choice:=input('1/2  ')=='1'
        elif choice=='2'
        print('\n first of all, let\'s choose a neighbourhood.')
        time.sleep(1)
        print('for ')
        neighbourhood
        while input()=='':
            pass    
    print('goodbye')
'''