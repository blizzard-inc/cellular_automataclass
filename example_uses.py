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
