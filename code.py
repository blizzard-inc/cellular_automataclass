class Board:
  def __init__(self,rows:list):
    if len(rows)==0 or any([len(rows[i])==0 for i in range(len(rows))]):
      raise TypeError
    self.rows=rows
    self.nrows=len(rows)
    self.ncols=len(rows[0])
  
  def __getitem__(self,key)
    return self.rows[key]
  def advance(self,rule:Rules)

class Neighbourhood:
  def __init__(self,neighbours:list):
    if any([len(neighbours[i]!=2 or any([type(neigbours[i][j])!=int for j in range(len(neighbours[i])) ]) for i in range(len(neigbours)) )])
    neighbours.sort()
    self.neighbours=neighbours

class Rules:
  def __init__(self,neigbours:Neighbourhood,livecases,deathcases)
      self.livecases,
