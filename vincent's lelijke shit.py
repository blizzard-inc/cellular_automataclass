  
class cellulaire_automata:
    def __init__(self, hoogte, breedte, begin):
        self.hoogte = hoogte
        self.breedte = breedte
        self.begin = begin
    
    def __str__(self):
        return str(self.maak_rooster(self.begin))
    
    def maak_rooster(self, begin):
        import math
        rooster = [[0]*self.breedte]*self.hoogte
        lijst1 = [0 for i in range(math.floor((self.breedte-3)/2))] 
        lijst2 = [0 for i in range(math.ceil((self.breedte-3)/2))]
        rooster[0] = lijst1+begin+lijst2
        return rooster
    
    def evolueer():
        pass
    
    def __repr__(self):
        return f'CA: hoogte ={self.hoogte}, breedte = {self.breedte}, begin = {self.begin}'

class een_dimensionaal(cellulaire_automata):
    
    def __init__(self, hoogte, breedte, begin, lijst0, lijst1):
        self.hoogte = hoogte
        self.breedte = breedte
        self.begin = begin
        self.lijst0 = lijst0
        self.lijst1 = lijst1
        
    def buren(self, begin):
        burenlijst = []
        lijsta= [self.begin]
        rooster = super().maak_rooster(begin)
        for i in range(1, self.hoogte):
            if i == 1:
                self.breedte = 3
            else:
                self.breedte +=  2
            rooster[i-1]=[0]+rooster[i-1]+[0]
            for j in range(0,self.breedte+2):
                burenlijst.append([rooster[i-1][(j-1)%self.breedte], rooster[i-1][j%self.breedte], rooster[i-1][(j+1)%self.breedte]])
            rooster[i] = self.evolueren(burenlijst)
            length = self.breedte + 2
            rooster[i] = rooster[i][:length]
            lijsta.append(rooster[i])
            for i in range(len(lijsta)):
                while len(lijsta[i]) < len(lijsta[-1]):
                    lijsta[i].insert(0,0)
                    lijsta[i].append(0)
            burenlijst.clear()
        return lijsta

    def evolueren(self, burenlijst):
        regel = []
        lijst_0 = [i for i in self.lijst0]
        lijst_1 = [i for i in self.lijst1]
        for lijst in burenlijst:
            if lijst in lijst_0:
                regel.append(0)
            elif lijst in lijst_1:
                regel.append(1)
        return regel
    
    def grafisch(self):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10,6))
        plt.imshow(self.buren(self.begin), cmap='hot')
    def __str__(self):
        return '\n'.join([str(stuff) for stuff in self.buren(self.begin)])
    
    def __repr__(self):
        return f'1d: lijst0={self.lijst0}, lijst1={self.lijst1}, {super().__repr__()}'
    
class twee_dimensionaal(cellulaire_automata):
    
    def __init__(self, hoogte, breedte):
        self.hoogte = hoogte
        self.breedte = breedte
    
    
a = een_dimensionaal(9, 3, [1,1,1], [[1, 1, 1], [1, 1, 0], [1, 0, 1], [0, 0, 0]], [[1, 0, 0], [0, 1, 1], [0, 1, 0], [0, 0, 1]])
print(a)
