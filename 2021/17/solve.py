from math import floor, ceil, sqrt
import re

def solve(tarxmin, tarxmax, tarymin, tarymax):
  minvelx = int(ceil((sqrt(8 * tarxmin) - 1) / 2))
  maxvely = 0
  
  for velx in range(minvelx, tarxmax + 1): # Increase x velocity from velxmin onwards
    # Find number of steps when x is in target range
    posx = 0
    step = 0
    steps = []
    for cur_velx in range(velx, 0, -1):
      # print(posx)
      step += 1
      posx += cur_velx
      if posx >= tarxmin and posx <= tarxmax:
        steps.append(step)
    if posx >= tarxmin and posx <= tarxmax:
      steps.append(-1)
    # print('vel = {}: {}'.format(velx, steps))
    
    # Find the range of y velocity  
    for step in steps:
      if step == -1:
        # We can go even higher steps
        newstep = max(steps) + 1
        while True:
          velyrangebot = (float(tarymin)/newstep) + ((float(newstep) - 1) / 2)
          velyrangetop = (float(tarymax)/newstep) + ((float(newstep) - 1) / 2)
          if floor(velyrangetop) >= velyrangebot:
            # Max y velocity causes highest y position
            maxvely = max(maxvely, floor(velyrangetop))
          # print('{}: {} to {}, max {}'.format(newstep, velyrangebot, velyrangetop, maxvely))
          newstep += 1
          if newstep > 1000:
            break
      else:
        velyrangebot = (float(tarymin)/step) + ((float(step) - 1) / 2)
        velyrangetop = (float(tarymax)/step) + ((float(step) - 1) / 2)
        if floor(velyrangetop) >= velyrangebot:
          # Max y velocity causes highest y position
          maxvely = max(maxvely, floor(velyrangetop))
        # print('{}: {} to {}, max {}'.format(step, velyrangebot, velyrangetop, maxvely))

  print(maxvely * (maxvely + 1) / 2)

inputs = [
  'target area: x=20..30, y=-10..-5',
  'target area: x=138..184, y=-125..-71'
]

input_re = re.compile('target area: x=([0-9]+)\.\.([0-9]+), y=(\-[0-9]+)\.\.(\-[0-9]+)')
for inp in inputs:
  m = input_re.match(inp)
  x1 = int(m.group(1))
  x2 = int(m.group(2))
  y1 = int(m.group(3))
  y2 = int(m.group(4))
  
  solve(x1, x2, y1, y2)
  