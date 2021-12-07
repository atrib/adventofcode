def fuelcalc(distance):
    return (distance * (distance + 1)) / 2

inp = [int(x) for x in open('input', 'r').readline().split(',')]

minfuel = None
for i in range(min(inp), max(inp) + 1):
    fuel = sum([fuelcalc(abs(x - i))  for x in inp])
    if not minfuel or (fuel < minfuel):
        minfuel = fuel

print(str(minfuel))