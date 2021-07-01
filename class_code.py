import numpy as np
#import time

class Neighbourhood:
    def __init__(self, reladresses : list) -> None:
        '''
        creates an instance of the class

        Parameters
        ----------
        reladresses : list
            relative coordinates of the neighbours of the cell.

        Returns
        -------
        None.

        '''
        dimension = len(reladresses[0])
        if any([len(reladress) != dimension for reladress in reladresses]):
            raise ValueError('The relative coordinates aren\'t all of the same dimension')
        self.neighbours = reladresses

    def __getitem__(self, index : tuple) -> tuple:
        '''
        gives the relative adress of a neighbour

        Parameters
        ----------
        index : tuple
            the number of the neighbour.

        Returns
        -------
        tuple
            the adress of the neighbour.

        '''
        return self.neighbours[index]

    def __setitem__(self, index : tuple, val : int) -> None:
        '''
        sets the relative adress of a neighbour

        Parameters
        ----------
        index : tuple
            the number of the neighbour.
        val : int
            the new adress of the neighbour.

        Returns
        -------
        None

        '''
        self.neighbours[index] = val

    def __str__(self) -> str:
        '''
        returns a readable description of the instance

        Returns
        -------
        str
            the readable description.

        '''
        return str(self.neighbours)

    def __repr__(self) -> str:
        '''
        returns a complete representation of the instance

        Returns
        -------
        str
            the complete representation.

        '''
        return self.__str__()

class Edgerule:
    def __init__(self, type : str = None, offset : tuple = None, const : int = None) -> None:
        '''
        creates an instance of the class

        Parameters
        ----------
        type : str, optional
            determines wether dirichlet, neumann or wrapping boundry conditions are used.
                The default is 'wrap'.
        offset : tuple, optional
            determines what offset is used in each direction. The default is (0,).
        const : int, optional
            the value it returns when type = 'D'. The default is 0.
        Returns
        ----------
        None.
        '''
        if not const:
            const = 0
        if not offset or type in ['D','N']:
            offset = (0, )
        if not type in ['D','N']:
            type = 'wrap'
            const = 0
        self.type = type
        self.offset = offset
        self.const= const
        
    def __call__(self, adress : tuple, shape : tuple) -> tuple:
        '''
        determines what to do when the instance is called with arguments.

        Parameters
        ----------
        adress : tuple
            the adress of a cell.
        shape : tuple
            shape of the board.

        Returns
        -------
        tuple
            
        first element = boolean, determines whether to use the second element 
            as constant or as adress.
        second element = either the value of the cell, or the 'real' adress of the cell

        '''
        if len(adress) != len(shape):
            raise ValueError('the adress doesn\'t have as many dimensions as the board')
        offsetcomp = list(self.offset)
        if len(adress) > len(self.offset):
            offsetcomp += [0] * (len(adress) - len(self.offset))
        elif 0 not in offsetcomp[:len(adress)]:
            raise ValueError('there is no 0 in the relevant offsets')
        offsetcomp = tuple(offsetcomp)
        zeroindex=offsetcomp.index(0)
        if all([ (0 <= adress[i] + offsetcomp[i] < shape[i]) for i in range(len(adress)) ]):
            return False, tuple(adress)
        elif self.type == 'D':
            return True, self.const
        elif self.type == 'N':
            forwardadress = [( 0 if adress[i] < 0 else shape[i] - 1) for i in range(len(adress))]
            return False, tuple(forwardadress)
        else:
            forwardadress = [(adress[i] + offsetcomp[i]*(adress[zeroindex]//shape[zeroindex])) % shape[i] for i in range(len(adress))]
            return False, tuple(forwardadress)

    def __str__(self) -> str:
        '''
        returns a readable description of the instance

        Returns
        -------
        str
            the readable description.

        '''
        if self.type == 'N':
            return f'von Neumann boundary, offsets are {self.offset}'
        elif self.type == 'D':
            return f'Dirichlet boundary, constant = {self.const}'
        else:            
            return f'wrapping boundary, offsets are {self.offset}'

    def __repr__(self) -> str:
        '''
        returns a complete representation of the instance

        Returns
        -------
        str
            the complete representation.

        '''
        return f'edgerule({self.type}, {self.constant}, {self.offset}'

class Rule:
    def __init__(self, neighbourhood : Neighbourhood, f = None) -> None:
        '''
        creates a new instance of this class

        Parameters
        ----------

        neighbourhood : Neighbourhood
            the neighbourhood of a generic cell.
        f : any type
            function which takes a list of states of the neighbours,
                and returns the next state. (nextstatefunction)
        
        Returns
        -------
        None.

        '''
        self.neighbourhood = neighbourhood
        self.f = f

    def __call__(self, neighbours:tuple) -> int:
        '''
        determines what to do when an instance is called

        Parameters
        ----------
        neighbours : tuple
            list of states of the neighbours.

        Returns
        -------
        int
            next state of the cell.
        '''
        if not self.f:
            raise ValueError
        return self.f(neighbours)

    def __str__(self) -> str:
        '''
        returns a readable description of the instance

        Returns
        -------
        str
            the readable description.

        '''
        return f'rule using function {self.f} and neighbourhood {self.neighbourhood}'

    def __repr__(self) -> str:
        '''
        returns a complete representation of the instance

        Returns
        -------
        str
            the complete representation.

        '''
        return f'rule({self.f},{self.neighbourhood})'

class Board:
    def __init__(self, matrix : np.array, edgerules : Edgerule) -> None:
        '''
        creates an instance of this class

        Parameters
        ----------
        matrix : np.array
            array which contains the states of the cells.
        edgerules : Edgerule
            the boundary condition for this instance.

        Returns
        -------
        None.

        '''
        self.edgerules = edgerules
        self.cells = matrix

    def neighbourhood(self, index : tuple, adresses : Neighbourhood) -> list:
        '''
        function for determining the states of the neighbours

        Parameters
        ----------
        index : tuple
            the adress of the cell.
        adresses : Neighbourhood
            the 'list' of relative adresses.

        Returns
        -------
        neighbours : list
            a list of states of the neighbours.

        '''
        neighbours = []
        for reladress in adresses:
            absadress = [index[i] + reladress[i] for i in range(len(index))]
            constant, val = self.edgerules(absadress, self.cells.shape)
            if constant:
                neighbour = val
            else:
                neighbour = self.cells[val]
            neighbours += [neighbour]
        return neighbours
        
    def nextstate(self, nextstatefunc : Rule = None) -> None:
        '''
        determines the next state of the board using the nextstatefunction,
            and changes the board to that state

        Parameters
        ----------
        nextstatefunc : Rule
            the rule with which the next states of the board are to be determined.

        Returns 
        -------
        None

        '''
        if not nextstatefunc:
            raise ValueError
        nextboard = Emptyboard(self.cells.shape, self.edgerules)
        adressbook = nextstatefunc.neighbourhood
        for index in np.ndenumerate(self.cells):
            neighbours = tuple(self.neighbourhood(index[0], adressbook))
            nextboard.cells[index[0]] = nextstatefunc(neighbours)
            
        self.cells = nextboard.cells
        
    def advance(self, rule : Rule = None, steps : int = None) -> None:
        '''
        takes multiple steps at once

        Parameters
        ----------
        rule : Rule
            the rule with which the next states of the board are to be determined.
        steps : int, optional
            the number of steps to be taken. The default is 1

        Returns
        -------
        None.

        '''
        if not rule:
            raise ValueError
        if not steps:
            steps = 1

        for _ in range(steps):
            self.nextstate(rule)
    
    def __getitem__(self, index :tuple ) -> int:
        '''
        gives the state of a cell

        Parameters
        ----------
        index : tuple
            the adress of the cell.

        Returns
        -------
        int
            the state of the cell.

        '''
        return self.cells[index]
    
    def __setitem__(self, index: tuple, val: int) -> None:
        '''
        sets the value of a cell

        Parameters
        ----------
        index : tuple
            the adress of the cell.
        val : int
            the new state of the cell.

        Returns
        -------
        None

        '''
        self.cells[index]=val
        
    def __str__(self) -> str:
        '''
        returns a readable description of the instance

        Returns
        -------
        str
            the readable description.

        '''
        return str(self.cells)

    def __repr__(self) -> str:
        '''
        returns a complete representation of the instance

        Returns
        -------
        str
            the complete representation.

        '''
        return f'{self.edgerules},\n board({self.cells})'

class Emptyboard(Board):
    def __init__(self, dimensions : tuple, edgerules: Edgerule) -> None:
        '''
        creates an instance of this class

        Parameters
        ----------
        dimensions : tuple
            the dimensions of the new board.
        edgerules : Edgerule
            the boundary conditions for this new board.

        Returns
        -------
        None.

        '''
        cells = np.zeros(dimensions, int)
        super().__init__(cells, edgerules)

class Totalistic(Rule):
    def __init__(self, neighbourhood : Neighbourhood, birth : list, live : list) -> None:
        '''
        creates an instance of this class

        Parameters
        ----------
        neighbourhood : Neighbourhood
            the relative adresses of the neighbours of a generic cell.
        birth : list
            list of number of live neighbours for which the current cell will turn alive.
        live : list
            list of number of live neighbours for which the current cell will stay alive.

        Returns
        -------
        None.

        '''
        self.birth = birth
        self.live = live
        def f(neighbours):
            birth = neighbours[0] == 0 and sum(neighbours) in self.birth
            live = neighbours[0] == 1 and sum(neighbours) - 1 in self.live
            if birth or live:
                return 1
            return 0
        super().__init__(neighbourhood,f)
        

    def __str__(self) -> str:
        '''
        returns a readable description of the instance

        Returns
        -------
        str
            the readable description.

        '''
        return f"totalistic rule B{','.join([str(i) for i in self.birth])}/S{','.join([str(i) for i in self.live])} with neighbourhood {self.neighbourhood}"

    def __repr__(self) -> str:
        '''
        returns a complete representation of the instance

        Returns
        -------
        str
            the complete representation.

        '''
        return f"totalistic(B{','.join([str(i) for i in self.birth])}/S{','.join([str(i) for i in self.live])}, {self.neighbourhood})"

class Moorehood(Neighbourhood):
    def __init__(self, dim : int = None, length : int = None) -> None:
        '''
        creates an instance of this class

        Parameters
        ----------
        dim : int, optional
            The number of dimensions of the neighbourhood. The default is 2.
        length : int, optional
            The maximum Chebyshev distance for cells in the neighbourhood.
                The default is 1.

        Raises
        ------
        ValueError
            dim cannot be lower than 1, and length cannot be lower than 0.

        Returns
        -------
        None

        '''
        if not dim:
            dim = 2
        if dim < 1:
            raise ValueError
        if not length:
            length = 1
        if length < 0:
            raise ValueError
        self.dim = dim
        self.length = length
        if length == 0:
            neighbours = [[0] * dim]
        else:
            neighbours=[[]]
            for _ in range(dim):
                for number in range(len(neighbours)):
                    current_house = neighbours[number]
                    neighbours[number] = current_house + [0]
                    for d in range(1, length + 1):
                        neighbours += [current_house + [d], current_house + [-d]]
        super().__init__(neighbours)

    def __str__(self) -> str:
        '''
        returns a readable description of the instance

        Returns
        -------
        str
            the readable description.

        '''
        return f'moore({self.dim},{self.length})'

class Neumannhood(Neighbourhood):
    def __init__(self, dim : int = None, length : int = None) -> None:
        '''
        creates an instance of this class

        Parameters
        ----------
        dim : int, optional
            The number of dimensions of the neighbourhood. The default is 2.
        length : int, optional
            The maximum Manhattan distance of cells in the neighbourhood.
            The default is 1.

        Raises
        ------
        ValueError
            dim cannot be lower than 1, and length cannot be lower than 0.


        Returns
        -------
        None.

        '''
        if not dim:
            dim = 2
        if dim < 1:
            raise ValueError
        if not length:
            length = 1
        if length < 0:
            raise ValueError
        self.dim = dim
        self.length = length
        if length == 0:
            neighbours = [[0] * dim]
        else:
            neighbours = [[]]
            for _ in range(dim):
                for number in range(len(neighbours)):
                    current_house = neighbours[number]
                    neighbours[number] = current_house + [0]
                    distance = sum([abs(coord) for coord in current_house])
                    for d in range(1, length - distance + 1):
                        neighbours += [current_house + [d], current_house + [-d]]
        super().__init__(neighbours)

    def __str__(self) -> str:
        '''
        returns a readable description of the instance

        Returns
        -------
        str
            the readable description.

        '''
        return f'Neumann({self.dim},{self.length})'


class Automata(Board):
    def __init__(self, matrix : np.array, edgerules: Edgerule, rules : Rule) -> None:
        '''
        Creates an instance of this class

        Parameters
        ----------
        matrix : np.array
            array which contains the states of the cells.
        edgerules : Edgerule
            the boundary condition for this instance.
        rules : Rule
            the rule with which the next states of the board are to be determined.

        Returns
        -------
        None

        '''
        self.rules=rules
        super().__init__(self, matrix, edgerules)
    
    def nextstate(self, rules : Rule = None) -> None:
        '''
        determines the next state of the board using the rule,
            and changes the board to that state


        Parameters
        ----------
        rules : Rule, optional
            the rule with which the next state of the board are to be determined.
                The default is self.rule .

        Returns
        -------
        None

        '''
        if not rules:
            rules = self.rules
        super().nextstate(rules)
    
    def advance(self, rules : Rule = None,  steps : int = None) -> None:
        '''
        takes multiple steps at once

        Parameters
        ----------
        rules : Rule, optional
            the rule with which the next states of the board are to be determined.
                The default is self.rule 
        steps : int, optional
            the number of steps to be taken. The default is 1

        Returns
        -------
        None

        '''
        if not rules:
            rules = self.rules
        super().advance(steps, rules)
        if not steps:
            steps = 1
    def __repr__(self) -> str:
        '''
        returns a complete representation of the instance

        Returns
        -------
        str
            the complete representation.

        '''
        return f'{self.rules}\n {self.edgerules} \n {self.cells}'
    
    
'''
life = Totalistic([(0,0),(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)], [3], [2, 3])
torus = Edgerule()
testboard = Emptyboard((5, 5), torus)
testboard.cells[1, 1] = 1
testboard.cells[1, 2] = 1
testboard.cells[2, 2] = 1
testboard.cells[2, 3] = 1
testboard.cells[3, 1] = 1
print(testboard.cells)
testboard.advance(6,life)
print(testboard.cells)
'''
'''
def r30(neighbourhood):
    key={(0,0,0):0,
     (0,0,1):1,
     (0,1,0):1,
     (0,1,1):1,
     (1,0,0):1,
     (1,0,1):0,
     (1,1,0):0,
     (1,1,1):0,
     }
    return key[neighbourhood]

rule30 = Rule([(-1,),(0,),(1,)],r30)
same = Edgerule('N')
testboard = Emptyboard((8,),same)
testboard[1-1]=1
testboard[4-1]=1
testboard[5-1]=1
testboard[7-1]=1
print(testboard)

while input('')!='exit':
    testboard.nextstate(rule30)
    print(testboard)
'''
'''
if __name__ == '__main__':
    print('starting program\n')
    time.sleep(4)
    if input('do you want to build a cellular automata?\n y/n  ') == 'y':
        print('for game of life, type 1')
        print('for a custom cellular automata, press 2')
        if choice:=input('1/2  ') == '1'
            pass
        elif choice=='2'
            pass
        else:
            pass
        print('\n first of all, let\'s choose a neighbourhood.')
        time.sleep(1)
        print('for ')
        neighbourhood
        while input() == '':
            pass    
    print('goodbye')
'''
