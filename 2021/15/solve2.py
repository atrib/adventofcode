
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
  
  minrisks = [[None] * cols for _ in range(rows)]
  minrisks[rows - 1][cols - 1] = 0
  # print(minrisks)
  
  countchanged = 1
  while countchanged > 0:
    countchanged = 0
    for row in range(rows):
      for col in range(cols):
        neighbours = [(x, y)  for (x, y) in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
                              if (0 <= x) and (x < rows) and (0 <= y) and (y < cols)]
        # print('{},{}: {}'.format(row, col, neighbours))
        
        # print([minrisks[x][y] for (x, y) in neighbours if minrisks[x][y] is not None])
        neighbourcosts = [minrisks[x][y] + inp[x][y] 
                              for (x, y) in neighbours 
                              if minrisks[x][y] is not None]
        # print('{},{}: {}'.format(row, col, neighbourcosts))
        if neighbourcosts != []:
          curcost = minrisks[row][col]
          minrisks[row][col] = min(min(neighbourcosts), curcost) if curcost is not None else min(neighbourcosts)
          countchanged += 1 if (curcost != minrisks[row][col]) else 0
    print(countchanged)
          
  print('Minimum risk to traverse path = {}'.format(minrisks[0][0]))

  
# solve('input.simp')
solve('input')
