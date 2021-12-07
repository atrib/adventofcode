
depth = 0
pos = 0

def forward(val):
  global pos
  pos += val
  
def up(val, bound = 0):
  global depth
  depth -= val
  if depth < bound:
    depth = bound

def down(val, bound):
  global depth
  depth += val
  if depth > bound:
    depth = bound

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
    down(val, 10000)
  else:
    assert False, 'Unknown opcode {}'.format(op)
  
print('depth = {}'.format(depth))
print('pos = {}'.format(pos))
print(str(depth * pos))
