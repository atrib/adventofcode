# Solves the problem using djikstra's which is much faster than the prev. attempt

def solve(filename):
  inp = [[int(x) for x in line.strip()] for line in open(filename, 'r')]
  rows = len(inp)
  cols = len(inp[0])
  
  # Generate 5x board as per rules
  inp5x = [[x for _ in range(5) for x in row ] for _ in range(5) for row in inp]
  for xtile in range(5):
    for ytile in range(5):
      inc = xtile + ytile
      for x in range(rows):
        for y in range(cols):
          xpos = (rows * xtile) + x
          ypos = (cols * ytile) + y
          # Risk values follow a circular 1-9 scale
          oldval = inp5x[xpos][ypos] - 1
          newval = ((oldval + inc) % 9) + 1
          inp5x[xpos][ypos] = newval
  inp = inp5x
  rows *= 5
  cols *= 5      
  
  def getrisk(point):
    return point[0]
  
  minrisks = [[None] * cols for _ in range(rows)]
  minrisks[rows - 1][cols - 1] = 0
  considering = set([(0, (rows - 1, cols - 1))])
  done = set()
  while len(considering) != 0:
    # Find lowest risk point and put it in done set
    (risk, minpoint) = sorted(list(considering), key = getrisk)[0]
    considering.remove((risk, minpoint))
    done.add(minpoint)
    
    # Find unvisited neighbours
    row = minpoint[0]
    col = minpoint[1]
    neighbours = [(x, y)  for (x, y) in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
                          if (0 <= x) and (x < rows) and (0 <= y) and (y < cols) and (x, y) not in done]
    
    # Update their risk as per current known risk
    for (x, y) in neighbours:
      risk_via_rowcol = inp[row][col] + minrisks[row][col]
      oldrisk = minrisks[x][y]
      if oldrisk:
        if oldrisk > risk_via_rowcol:
          considering.remove((oldrisk, (x, y)))
          considering.add((risk_via_rowcol, (x, y)))
          minrisks[x][y] = risk_via_rowcol
      else:
        considering.add((risk_via_rowcol, (x, y)))
        minrisks[x][y] = risk_via_rowcol
        
  print('Minimum risk to traverse path = {}'.format(minrisks[0][0]))

  
solve('input.simp')
solve('input')
