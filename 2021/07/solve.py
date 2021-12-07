def median(lst):
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // 2
   
    if (lstLen % 2):
        return sortedLst[index]
    else:
        return (sortedLst[index] + sortedLst[index + 1])/2.0

inp = [int(x) for x in open('input', 'r').readline().split(',')]

target = median(inp)

fuel = sum([abs(x - target) for x in inp])

print(str(fuel))
