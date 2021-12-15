
def solve(filename):
  inp = [[int(x) for x in line.strip()] for line in open(filename, 'r')]
  rows = len(inp)
  cols = len(inp[0])
  
  minrisks = [[None] * cols for _ in range(rows)]
  minrisks[rows - 1][cols - 1] = 0
  # print(minrisks)
  
  changed = True
  while changed:
    changed = False
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
          changed = (curcost != minrisks[row][col]) or changed
          
  print('Minimum risk to traverse path = {}'.format(minrisks[0][0]))

  
solve('input.simp')
solve('input')
