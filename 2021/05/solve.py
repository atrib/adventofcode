import re

def main():
  lines = []
  line_re = re.compile('([0-9]+),([0-9]+) -> ([0-9]+),([0-9]+)')
  with open('input', 'r') as fd:
    for line in fd:
      m = line_re.match(line)
      assert m
      lines.append(((int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4)))))
      
  # Discard non-horizontal/vertical lines
  lines = [((x1,y1), (x2,y2)) for ((x1,y1), (x2,y2)) in lines if (x1 == x2) or (y1 == y2)]
  
  maxx = max([max(x1, x2) for ((x1,y1), (x2,y2)) in lines])
  maxy = max([max(y1, y2) for ((x1,y1), (x2,y2)) in lines])
  oceanfloor = [[0] * (maxx + 1) for _ in range(maxy + 1)]

  # [print(row) for row in oceanfloor]
  # print()
  # Mark lines
  for ((x1,y1), (x2,y2)) in lines:
    if x1 == x2:
      for y_idx in range(min(y1, y2), max(y1, y2) + 1):
        oceanfloor[y_idx][x1] += 1
    elif y1 == y2:
      for x_idx in range(min(x1, x2), max(x1, x2) + 1):
        oceanfloor[y1][x_idx] += 1
        
    # [print(row) for row in oceanfloor]
    # print()
    
  # Count dangerous points
  print(sum([1 for row in oceanfloor for val in row if val >= 2]))
    
if __name__ == '__main__':
  main()