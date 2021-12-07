import re

# Check if val is within limits
def within(lim1, lim2, val):
  minlim = min(lim1, lim2)
  maxlim = max(lim1, lim2)
  return (val >= minlim) and (val <= maxlim)

def main():
  lines = []
  line_re = re.compile('([0-9]+),([0-9]+) -> ([0-9]+),([0-9]+)')
  with open('input', 'r') as fd:
    for line in fd:
      m = line_re.match(line)
      assert m
      lines.append(((int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4)))))
      
  # Discard non-horizontal/vertical/diagonal lines
  lines = [((x1,y1), (x2,y2)) for ((x1,y1), (x2,y2)) in lines 
              if (x1 == x2) 
                  or (y1 == y2)
                  or ((x1 - x2) == (y1 - y2))
                  or ((x1 - x2) == (y2 - y1))]
  print(len(lines))
  
  maxx = max([max(x1, x2) for ((x1,y1), (x2,y2)) in lines])
  maxy = max([max(y1, y2) for ((x1,y1), (x2,y2)) in lines])
  print('{} {} {}'.format(maxx, maxy, maxx*maxy))
  oceanfloor = [[0] * (maxx + 1) for _ in range(maxy + 1)]
  
  # Brute force, oh yeah
  count_danger = 0
  for x in range(maxx + 1):
    for y in range(maxy + 1):
      num = 0
      for ((x1,y1), (x2,y2)) in lines:
        if (x1 == x2) and (x == x1) and within(y1, y2, y):
          num += 1
        elif (y1 == y2) and (y == y1) and within(x1, x2, x):
          num += 1
        elif within(x1, x2, x) and within(y1, y2, y):
          diffx = x - x1
          diffy = y - y1
          if (diffx == diffy) or (diffx == -diffy):
            num += 1
        
      if num >= 2:
        count_danger += 1
  
  print(count_danger)

    
if __name__ == '__main__':
  main()
  
  # # [print(row) for row in oceanfloor]
  # # print()
  # # Mark lines
  # for ((x1,y1), (x2,y2)) in lines:
  #   print(str(((x1,y1), (x2,y2))))
  #   if x1 == x2: # Vertical
  #     for y_idx in range(min(y1, y2), max(y1, y2) + 1):
  #       oceanfloor[y_idx][x1] += 1
  #   elif y1 == y2: # Horizontal
  #     for x_idx in range(min(x1, x2), max(x1, x2) + 1):
  #       oceanfloor[y1][x_idx] += 1
  #   else: # Diagonal
  #     incx = +1 if (x1 < x2) else -1
  #     incy = +1 if (y1 < y2) else -1
  #     iterator = 1 if (x1 - x2) == (y1 - y2) else -1
  #     for x_idx in range(x1, x2 + incx, incx):
  #       y_idx = y1 + ((x_idx - x1) * incx * incy)
  #       # print('{}, {}'.format(x_idx, y_idx))
  #       oceanfloor[x_idx][y_idx] += 1
      
  #     assert x_idx == x2
  #     assert y_idx == y2
        
  #   # [print(row) for row in oceanfloor]
  #   # print()
    
  # # Count dangerous points
  # print(sum([1 for row in oceanfloor for val in row if val >= 2]))
