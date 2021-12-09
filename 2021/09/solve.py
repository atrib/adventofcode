inp = [[int(c) for c in line.strip()] for line in open('input', 'r').readlines()]

lenx = len(inp[0])
leny = len(inp)

def lowpoint(x, y):
    neighbours = [inp[y_dash][x_dash] 
                    for (x_dash, y_dash) in [(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y
                    
                    )]
                        if (x_dash >= 0) and (x_dash < lenx) and (y_dash >= 0) and (y_dash < leny)]

    # print(neighbours)
    return inp[y][x] < min(neighbours)

risksum = 0
for i in range(0, lenx):
    for j in range(0, leny):
        if lowpoint(i, j):
            risk = 1 + inp[j][i]
            risksum += risk

print(risksum)
