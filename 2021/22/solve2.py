import re

def insideoutside(oldmin, oldmax, newmin, newmax):
    inside = []
    outside = []
    assert oldmin <= oldmax
    assert newmin <= newmax

    if oldmin == oldmax:
        # Full overlap
        if (newmin <= oldmin) and (oldmin <= newmax):
            inside.append((oldmin, oldmax))
        else:
            outside.append((oldmin, oldmax))

        return (inside, outside)

    if newmin < oldmin:
        if newmax < oldmin:
            outside.append((oldmin, oldmax))
        elif newmax < oldmax:
            outside.append((newmax + 1, oldmax))
            inside.append((oldmin, newmax))
        else:
            inside.append((oldmin, oldmax))
    elif newmin == oldmin:
        if newmax < oldmax:
            outside.append((newmax + 1, oldmax))
            inside.append((oldmin, newmax))
        else:
            inside.append((oldmin, oldmax))
    elif (newmin > oldmin) and (newmin < oldmax): 
        outside.append((oldmin, newmin - 1))
        if newmax < oldmax:
            outside.append((newmax + 1, oldmax))
            inside.append((newmin, newmax))
        else:
            inside.append((newmin, oldmax))
    elif newmin == oldmax:
        outside.append((oldmin, newmin - 1))
        inside.append((newmin, oldmax))
    else: # newmin > oldmax:
        outside.append((oldmin, oldmax))

    return (inside, outside)

# Assuming that oldcubes are non-overlapping
def cutout(oldcubes, newcube):
    oldcubescutout = []
    (newminx,newmaxx,newminy,newmaxy,newminz,newmaxz) = newcube

    for oldcube in oldcubes:
        (oldminx,oldmaxx,oldminy,oldmaxy,oldminz,oldmaxz) = oldcube

        (insidex, outsidex) = insideoutside(oldminx, oldmaxx, newminx, newmaxx)
        (insidey, outsidey) = insideoutside(oldminy, oldmaxy, newminy, newmaxy)
        (insidez, outsidez) = insideoutside(oldminz, oldmaxz, newminz, newmaxz)

        # All parts with at-least one dimension outside newcube survive
        # All subparts of non-overlapping oldcubes are also assured to be non-overlapping
        [oldcubescutout.append((minx, maxx, miny, maxy, minz, maxz)) 
                                for (minx, maxx) in outsidex
                                for (miny, maxy) in outsidey + insidey
                                for (minz, maxz) in outsidez + insidez]

        [oldcubescutout.append((minx, maxx, miny, maxy, minz, maxz)) 
                                for (minx, maxx) in insidex
                                for (miny, maxy) in outsidey
                                for (minz, maxz) in outsidez + insidez]

        [oldcubescutout.append((minx, maxx, miny, maxy, minz, maxz)) 
                                for (minx, maxx) in insidex
                                for (miny, maxy) in insidey
                                for (minz, maxz) in outsidez]

    return oldcubescutout


def solve(filename):
    line_re = re.compile('(on|off) x=(\-?[0-9]+)\.\.(\-?[0-9]+),y=(\-?[0-9]+)\.\.(\-?[0-9]+),z=(\-?[0-9]+)\.\.(\-?[0-9]+)')
    lines = [line_re.match(line.strip()).groups() for line in open(filename, 'r')]

    cubesets = {
        'on': [],
        'off': []
    }

    countlines = 0
    for line in lines:
        newcubetype = line[0]
        minx = int(line[1])
        maxx = int(line[2])
        miny = int(line[3])
        maxy = int(line[4])
        minz = int(line[5])
        maxz = int(line[6])
        newcube = (minx, maxx, miny, maxy, minz, maxz)

        # Cut out new cube out of ALL existing cubes. 
        # All cells in new cube now have newcubetype
        cubesets = {cubetype: cutout(oldcubes, newcube) for cubetype, oldcubes in cubesets.items()}
        cubesets[newcubetype].append(newcube)
            
        countlines += 1
        print('Processed lines {}/{}. Cubes `on`: {} `off`: {} '.format(countlines, len(lines), len(cubesets['on']), len(cubesets['off'])))
    print('Number of `on` cells for {} is {}'.format(
            filename,
            sum([(maxx - minx + 1) * (maxy - miny + 1) * (maxz - minz + 1) 
                for (minx, maxx, miny, maxy, minz, maxz) in cubesets['on']])
                                )
        )

solve('input.simp')
solve('input.simp2')
solve('input.simp3')
solve('input')
