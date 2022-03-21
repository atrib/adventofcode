import re

def solve(filename):
    line_re = re.compile('(on|off) x=(\-?[0-9]+)\.\.(\-?[0-9]+),y=(\-?[0-9]+)\.\.(\-?[0-9]+),z=(\-?[0-9]+)\.\.(\-?[0-9]+)')
    lines = [line_re.match(line.strip()).groups() for line in open(filename, 'r')]

    points = {
        'on': set(),
        'off': set()
    }

    # [print(line) for line in lines]

    upperlim = 50
    lowerlim = -50
    for line in lines:
        minx = max(int(line[1]), lowerlim)
        maxx = min(int(line[2]), upperlim)
        miny = max(int(line[3]), lowerlim)
        maxy = min(int(line[4]), upperlim)
        minz = max(int(line[5]), lowerlim)
        maxz = min(int(line[6]), upperlim)

        ison = line[0] == 'on'
        other = 'on' if line[0] == 'off' else 'off'
        added = 0
        for x in range(minx, maxx + 1, 1):
            for y in range(miny, maxy + 1, 1):
                for z in range(minz, maxz + 1, 1):
                    if (x, y, z) not in points[line[0]]:
                        added += 1
                    points[line[0]].add((x, y, z))
                    points[other].discard((x, y, z))

                # print(points)

        # print(added)

    print('{} has {} points on'.format(filename, len(points['on'])))
    # print(len(points['off']))




    # print(lines)

solve('input.simp')
solve('input.simp2')
solve('input.simp3')
solve('input')
