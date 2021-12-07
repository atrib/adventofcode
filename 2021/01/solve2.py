
data = []
with open('input', 'r') as fd:
  for line in fd:
    data.append(int(line))

zipped_data3 = zip(data[:-2], data[1:-1], data[2:])
summed_data3 = [sum(x) for x in zipped_data3]

inc = 0
prev = None
for cur in summed_data3:
  if prev and (cur > prev):
    inc+=1
  prev = cur

print(inc)