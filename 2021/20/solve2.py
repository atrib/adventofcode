def grow_canvas(canvas, whattodo = 9):
    if whattodo == 9: # 9x growth
        (outside, image) = canvas
        nrows = len(image)
        ncols = len(image[0]) 
        newimage = [(outside * ncols * 3) for _ in range(0, 3 * nrows)]
        for nrow in range(nrows):
            newimage[nrow + nrows] = (outside * ncols) + image[nrow] + (outside * ncols)

        # [print(row) for row in image]
        # print()
        # [print(row) for row in newimage]

        return (outside, newimage)
    elif whattodo == 1: # +1 growth
        (outside, image) = canvas
        nrows = len(image)
        ncols = len(image[0]) 
        newimage = [[outside for _ in range(ncols + 2)]] + \
                    [[outside] + row + [outside] for row in image] + \
                    [[outside for _ in range(ncols + 2)]]

        # [print(row) for row in image]
        # print()
        # [print(row) for row in newimage]

        return (outside, newimage)
    
    assert False

def to_bin(num):
    ret = 0
    for n in num:
        assert n in [0,1]
        ret *= 2
        ret += n
    return ret

def enhance(canvas, algomap):
    # Grow without any changes, after which all non-canvas chars will be same
    canvas = grow_canvas(canvas, 1)
    (outside, image) = canvas
    nrows = len(image)
    ncols = len(image[0]) 
    
    # [print(row) for row in image]
    # print()
    newimg = []
    for i in range(nrows):
        newrow = []
        for j in range(ncols):
            # print('{} {}'.format(i, j))
            idx = to_bin([image[x][y] if ((x >= 0 and x < nrows) and (y >= 0 and y < ncols)) else outside
                                        for x in [i-1, i, i+1] for y in [j-1, j, j+1]])
            newrow.append(algomap[idx])
        newimg.append(newrow)

    outside_idx = to_bin([outside for _ in range(9)])
    outside = algomap[outside_idx]

    canvas = (outside, newimg)
    # [print(row) for row in newimg]
    return canvas

def solve(filename):
    lines = [line.strip() for line in open(filename, 'r')]
    algomap = lines[0]
    assert len(algomap) == 512
    assert len(lines[1]) == 0
    canvas = ('.', lines[2:])
    # canvas = grow_canvas(canvas, 9)
    # canvas = grow_canvas(canvas, 1)

    # Replace '.' with 0 and '#' with 1
    algomap = [1 if c == '#' else 0 for c in algomap]
    (outside, image) = canvas
    canvas = (1 if outside == '#' else 0, [[1 if c == '#' else 0 for c in row] for row in image])

    count_reps = 50
    for rep in range(count_reps):
        canvas = enhance(canvas, algomap)

    (outside, image) = canvas

    # Outside pixels must be off for count to make sense
    assert outside == 0
    print('{} has {} lit pixels'.format(filename, sum([sum(row) for row in image])))


solve('input.simp')
solve('input')
