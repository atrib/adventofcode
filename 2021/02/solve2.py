
depth = 0
pos = 0
aim = 0

def forward(val):
  global pos
  global depth
  global aim
  pos += val
  depth += aim * val
  
def up(val):
  global aim
  aim -= val

def down(val):
  global aim
  aim += val

data = []
with open('input', 'r') as fd:
  for line in fd:
    data.append(line)
    
for cmd in data:
  (op, arg) = cmd.split(' ')
  val = int(arg)
  if op == 'forward':
    forward(val)
  elif op == 'up':
    up(val)
  elif op == 'down':
    # TODO: remove arbitrary depth limit
    down(val)
  else:
    assert False, 'Unknown opcode {}'.format(op)
  
print('depth = {}'.format(depth))
print('pos = {}'.format(pos))
print(str(depth * pos))
