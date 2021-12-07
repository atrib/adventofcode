prev = None
cur = None

inc = 0
with open('input', 'r') as fd:
  for line in fd:
    cur = int(line)
    if prev and (cur > prev):
      inc += 1
      
    prev = cur

print(inc)