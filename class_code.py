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
   
        Raises
        ----------
        ValueError
            Te coordinates need to be of the same dimension.
        
        TypeError
            The adresses need to be tuples and the coordinates of the adress need to be integers
        
        Returns
        -------
        None.

        '''
        dimension = len(reladresses[0])
        if any([len(reladress) != dimension for reladress in reladresses]):
            raise ValueError('The relative coordinates aren\'t all of the same dimension')
        if any([type(reladress) != tuple for reladress in reladresses]):
            raise TypeError('All adresses must be tuples')
        if any([any([type(coordinate)!= int for coordinate in reladress])for reladress in reladresses]):
            raise TypeError('All coordinates in adresses should be integers')
        self.neighbours = reladresses

    def __getitem__(self, index : int) -> tuple:
        '''
        gives the relative adress of a neighbour

        Parameters
        ----------
        index : int
            the number of the neighbour.

        Returns
        -------
        tuple
            the adress of the neighbour.

        '''
        return self.neighbours[index]

    def __setitem__(self, index : int, val : tuple) -> None:
        '''
        sets the relative adress of a neighbour

        Parameters
        ----------
        index : int
            the number of the neighbour.
        val : tuple
            the new adress of the neighbour.
   
        Raises
        ----------
        ValueError
            The dimension of the old and new adress need to be the same.
        
        Returns
        -------
        None

        '''
        if len(val) != len(self.neighbours[index]):
            raise ValueError('the dimension of the new adress doesn\'t match the old one')
        self.neighbours[index] = val
        
    def __len__(self) -> int:
        '''
        returns the number of neighbours
        
        Returns
        -------
        int
            the number of neighbours
        
        '''
        return len(self.neighbours)
        
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
    def __init__(self, kind : str = None, offset : tuple = None, const : int = None) -> None:
        '''
        creates an instance of the class

        Parameters
        ----------
        kind : str, optional
            determines wether dirichlet, neumann or wrapping boundry conditions are used.
                The default is 'wrap'.
        offset : tuple, optional
            determines what offset is used in each direction. The default is (0,).
        const : int, optional
            the value it returns when type = 'D'. The default is 0.
   
        Raises
        ----------
        TypeError
            The offsets need to be integers
        
        Returns
        ----------
        None.
        '''
        if not kind in ['D','N']:
            kind = 'wrap'
            const = 0    
            if not offset :
                offset = (0, )
            if any([type(change) != int for change in offset]):
                raise TypeError('the offsets must be integers')
        else:
            offset = (0, )    
            if not const:
                const = 0
        self.kind = kind
        self.offset = offset
        self.const = const
        
    def __call__(self, adress : tuple, shape : tuple) -> tuple:
        '''
        determines what to do when the instance is called with arguments.

        Parameters
        ----------
        adress : tuple
            the adress of a cell.
        shape : tuple
            shape of the board.
   
        Raises
        ----------
        ValueError
            The dimension of adress and board need to match, the shape of the board needs to have positive length 
                and there needs to be a 0 in the offsets
        
        TypeError
            The coordinates of the cell need to be integers 
                and the amount of cells in each direction of the board must be an integer.
        
        Returns
        -------
        tuple
            
        first element = boolean, determines whether to use the second element 
            as constant or as adress.
        second element = either the value of the cell, or the 'real' adress of the cell

        '''
        if len(adress) != len(shape):
            raise ValueError('the adress doesn\'t have as many dimensions as the board')
        if any([type(coordinate)!=int for coordinate in adress]):
            raise TypeError('the coordinates of a cell must be integers')
        if any([length<=0 for length in shape]):
            raise ValueError('the shape of the board doesn\'t support negative lengths')
        if any([type(length)!=int for length in shape]):
            raise TypeError('the board must have an integer amount of cells in any direction')
        offsetcomp = list(self.offset)
        if len(adress) > len(self.offset):
            offsetcomp += [0] * (len(adress) - len(self.offset))
        else:
            offsetcomp = offsetcomp[:len(adress)]
        if 0 not in offsetcomp[:len(adress)]:
            raise ValueError('there is no 0 in the relevant offsets')
        offsetcomp = tuple(offsetcomp)
        zeroindex=offsetcomp.index(0)
        if all([ (0 <= adress[i] < shape[i]) for i in range(len(adress)) ]):
            return False, tuple(adress)
        elif self.kind == 'D':
            return True, self.const
        elif self.kind == 'N':
            forwardadress = [( 0 if adress[i] < 0 else shape[i] - 1 if adress[i] >= shape[i] else adress[i]) for i in range(len(adress))]
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
        if self.kind == 'N':
            return f'von Neumann boundary, offsets are {self.offset}'
        elif self.kind == 'D':
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
   
        Raises
        ----------
        ValueError
            The number of neighbours needs to match with the neighbourhood of the rule 
                and the next state function must be defined.
        
        TypeError
            The state of a neighbours must be an integer.
        
        Returns
        -------
        int
            next state of the cell.
        '''
        if len(neighbours) != len(self.neighbourhood):
            raise ValueError('The number of neighbours doesn\'t match with the neighbourhood of the rule')
        if any([type(neighbour) != np.int32 for neighbour in neighbours]):
            raise TypeError('The state of any neighbour is always an numpy.int32')
        if self.f == None:
            raise ValueError('the next state function has not been defined')
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
   
        Raises
        ----------
        TypeError
            All cells of the matrix need to be integers.
        
        Returns
        -------
        None.

        '''
        if matrix.dtype != np.int32:
            raise TypeError('all cells must have integer type')
        
        self.edgerules = edgerules
        self.cells = matrix

    def neighbourhood(self, index : tuple, reladresses : Neighbourhood) -> list:
        '''
        function for determining the states of the neighbours

        Parameters
        ----------
        index : tuple
            the adress of the cell.
        adresses : Neighbourhood
            the 'list' of relative adresses.
   
        Raises
        ----------
        ValueError
            The dimension of adress and the board need to match.
        
        TypeError
           The value of the cells needs to be an integer and the dimension of neighbours adress 
                and the board need to match.
        
        Returns
        -------
        neighbours : list
            a list of states of the neighbours.

        '''
        if len(index) != self.cells.ndim:
            raise ValueError('the number of dimensions of the adress don\'t match up with that of the board')
        if any([type(coordinate)!=int for coordinate in index]):
            raise TypeError('the value of the cells must all be of type integer')
        if len(reladresses[0]) != self.cells.ndim:

            raise TypeError('the number of dimensions of the neighbours adresses don\'t match up with that of the board')
        neighbours = []
        for reladress in reladresses:
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
        
        Raises
        ----------
        ValueError
            nextstatefunc needs to be specified
        
        Returns 
        -------
        None

        '''
        if not nextstatefunc:
            raise ValueError('a rule must be specified. Are you missing an argument?')
        nextboard = np.zeros(self.cells.shape,np.int32)
        adressbook = nextstatefunc.neighbourhood
        for index in np.ndenumerate(self.cells):
            neighbours = tuple(self.neighbourhood(index[0], adressbook))
            nextboard[index[0]] = nextstatefunc(neighbours)
            
        self.cells = nextboard
        
    def advance(self, rule : Rule = None, steps : int = None) -> None:
        '''
        takes multiple steps at once

        Parameters
        ----------
        rule : Rule
            the rule with which the next states of the board are to be determined.
        steps : int, optional
            the number of steps to be taken. The default is 1
        
        Raises
        ----------
        ValueError
            rule must be specified and steps cannot be lower than 1.

        Returns
        -------
        None.

        '''
        if not rule:
            raise ValueError('a rule must be specified. Are you missing an argument?')
        if not steps:
            steps = 1
        if steps < 1:
            raise ValueError('You cannot make me go backwards, that goes against the second law of thermodynamics')
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
        
        Raises
        ----------
        ValueError
            The length of the dimensions need to be positive.
        
        TypeError
           The dimensions need to be integers
           
        Returns
        -------
        None.

        '''
        if any([length<= 0  for length in dimensions]):
            raise ValueError('you cannot use non-positive lengths for any dimensions')
        if any([type(length)!= int for length in dimensions]):
            raise TypeError('all dimensions for a board must be integers')
        cells = np.zeros(dimensions, np.int32)
        super().__init__(cells, edgerules)

class Totalistic(Rule):
    def __init__(self, neighbourhood : Neighbourhood, birth : set, live : set) -> None:
        '''
        creates an instance of this class

        Parameters
        ----------
        neighbourhood : Neighbourhood
            the relative adresses of the neighbours of a generic cell.
        birth : set
            list of number of live neighbours for which the current cell will turn alive.
        live : set
            list of number of live neighbours for which the current cell will stay alive.
        
        Raises
        ----------
        ValueError
            The amount of living neighbours needs to be positive 
                and the amount of living neighbours cannot proceed the amount of neighbours
        
        TypeError
            The amount of living neighbours needs to be an integer.
           
        Returns
        -------
        None.

        '''
        if any([total < 0 for total in birth]):
            raise ValueError('you cannot have a negative amount of living neighbours')
        if any([total > len(neighbourhood) for total in birth]):
            raise ValueError('you cannot have more living neighbours than you have neighbours')
        if any([type(total) != int for total in birth]):
            raise TypeError('you cannot have a non-integer amount of living neighbours')
        if any([total < 0 for total in live]):
            raise ValueError('you cannot have a negative amount of living neighbours')
        if any([total > len(neighbourhood) for total in live]):
            raise ValueError('you cannot have more living neighbours than you have neighbours')
        if any([type(total) != int for total in live]):
            raise TypeError('you cannot have a non-integer amount of living neighbours')
        self.birth = birth
        self.live = live
        def f(neighbours : list)->int:
            '''
            returns the next state of a cell based on a list of states of the neighbours
            
            Parameters
            ----------
            
            neighbours : list
                list of states of the neighbours of a cell
        
            Raises
            ----------
            ValueError
                The number of neighbours needs to match the size of the neighbourhood.
        
            TypeError
                The state of a cell needs to be a 0 or 1.
           
            Returns
            -------
                int
                    next state of the cell
            '''
            if len(neighbours) != len(neighbourhood):
                raise ValueError('the number of neighbours doesn\'t match with the size of the neighbourhood')
            if any([neighbour not in [0,1] for neighbour in neighbours]):
                raise TypeError('the state of any cell can only be 0 or 1 with a totalistic rule')
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
        if length == None:
            length = 1
        if length < 0:
            raise ValueError
        self.dim = dim
        self.length = length
        neighbours = [[]]
        for _ in range(dim):
            for number in range(len(neighbours)):
                current_house = neighbours[number]
                neighbours[number] = current_house + [0]
                for d in range(1, length + 1):
                    neighbours += [current_house + [d], current_house + [-d]]
        for number in range(len(neighbours)):
            neighbours[number] = tuple(neighbours[number])
        
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
        if length == None:
            length = 1
        if length < 0:
            raise ValueError
        self.dim = dim
        self.length = length
        neighbours = [[]]
        for _ in range(dim):
            for number in range(len(neighbours)):
                current_house = neighbours[number]
                neighbours[number] = current_house + [0]
                distance = sum([abs(coord) for coord in current_house])
                for d in range(1, length - distance + 1):
                    neighbours += [current_house + [d], current_house + [-d]]
        for number in range(len(neighbours)):
            neighbours[number] = tuple(neighbours[number])
        
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
        super().__init__(matrix, edgerules)
    
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
