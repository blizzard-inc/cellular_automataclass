class bord:
  def __init__(self,rows:list):
    if len(rows)==0 or any(len(rows[i])==0 for i in range(len(rows))):
      raise TypeError
    self.rows=rows
    self.nrows=len(rows)
    self.ncols=len(rows[0])
  
    
