inp = [[int(c) for c in line.strip()] for line in open('input', 'r').readlines()]

lenx = len(inp[0])
leny = len(inp)

# Check if a point is a lowpoint
def lowpoint(x, y):
    neighbours = [inp[y_dash][x_dash] 
                    for (x_dash, y_dash) in [(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)]                    
                        if (x_dash >= 0) and (x_dash < lenx) and (y_dash >= 0) and (y_dash < leny)]
    return inp[y][x] < min(neighbours)

# Find all points in a basin, starting at a lowpoint
def basin(lowpoint):
    basinpoints = []
    toprocess = [lowpoint]

    while len(toprocess) > 0:
        newtoprocess = []
        for x, y in toprocess:
            basinpoints.append((x,y))
            # print(basinpoints)
            neighbours = [(x_dash, y_dash) 
                            for (x_dash, y_dash) in [(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)]
                                if (x_dash >= 0) and (x_dash < lenx) and (y_dash >= 0) and (y_dash < leny) # Within bounds
                                    and inp[y_dash][x_dash] != 9                                           # Basins bounded by 9
                                    and (x_dash, y_dash) not in basinpoints                                # Already seen, is in basinpoints
                                    and (x_dash, y_dash) not in newtoprocess                               # Already seen, waiting to be processed 
                            ]
            # print(neighbours)
            [newtoprocess.append(neighbour) for neighbour in neighbours]
        toprocess = newtoprocess
    
    return basinpoints

lowpoints = [(i, j) for i in range(0, lenx) for j in range(0, leny) if lowpoint(i, j)]
basins = [basin(lowpoint) for lowpoint in lowpoints]
basins.sort(key = len, reverse = True)

print([len(basin) for basin in basins])
assert len(basins) >= 3

print('Product of three biggest basins {} * {} * {} = {}'.format(
    len(basins[0]),
    len(basins[1]),
    len(basins[2]),
    len(basins[0]) * len(basins[1]) * len(basins[2])
))
