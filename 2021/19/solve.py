from math import sqrt
from matplotlib import pyplot as plt
import re

def get_sensor_data(filename):
    scanner_re = re.compile('\-\-\- scanner ([0-9]+) \-\-\-')
    beacon_re  = re.compile('(\-?[0-9]+),(\-?[0-9]+),(\-?[0-9]+)')
    scanners = []
    beacons = []
    for line in open(filename, 'r'):
        scanner_m = scanner_re.match(line)
        if line == '\n':
            scanners.append(beacons)
        elif scanner_m is not None:
            beacons = []
        else:
            beacon_m = beacon_re.match(line)
            assert beacon_m is not None
            beacons.append((int(beacon_m.group(1)), int(beacon_m.group(2)), int(beacon_m.group(3))))

    return scanners

def dist(p1, p2):
    # print('{}     {}'.format(p1, p2))
    return sqrt((p1[0] - p2[0])*(p1[0] - p2[0]) + (p1[1] - p2[1])*(p1[1] - p2[1]) + (p1[2] - p2[2])*(p1[2] - p2[2]))
def firstelem(tuple):
    return tuple[0]
def choose(a, b):
    assert b == 2
    return (a* (a - 1))/2

def calculate_similarity(distances_sensor1, distances_sensor2):
    i = 0
    j = 0
    common_pts = []
    prev_dist = 0
    while (i < len(distances_sensor1)) and (j < len(distances_sensor2)):
        (d1, p11, p12) = distances_sensor1[i]
        (d2, p21, p22) = distances_sensor2[j]
        if d1 == d2:
            common_pts.append((d1, p11, p12, p21, p22))
            i += 1
            j += 2
            # Matching becomes harder if more than two pairs of points have the same distance,
            # so we ignore them for now and keep a check instead
            assert prev_dist != d1
            prev_dist = d1
        elif d1 < d2:
            i += 1
        else:
            j+= 1

    # print(len(common_pts))
    # [print(x) for x in common_pts]
    return common_pts


# Generate rotation
def find_rotation(known_delta, unknown_delta): 
    (kx_delta,ky_delta,kz_delta) = known_delta
    (ux_delta,uy_delta,uz_delta) = unknown_delta
    xrot = None
    yrot = None
    zrot = None

    maps = {
        ux_delta: +1,
        -ux_delta: -1,
        uy_delta: 2,
        -uy_delta: -2,
        uz_delta: 3,
        -uz_delta: -3
    }
    xrot = maps[kx_delta]
    yrot = maps[ky_delta]
    zrot = maps[kz_delta]
    return (xrot, yrot, zrot)

def apply_rotation(rotation, point):
    (rotx, roty, rotz) = rotation
    (x_delta, y_delta, z_delta) = point
    maps = {
        1: x_delta,
        -1: -x_delta,
        2: y_delta,
        -2: -y_delta,
        3: z_delta,
        -3: -z_delta
    }

    return (maps[rotx], maps[roty], maps[rotz])

def add_points(p1, p2):
    assert len(p1) == 3
    assert len(p2) == 3
    return (p1[0] + p2[0], p1[1] + p2[1], p1[2] + p2[2])
def neg(p):
    assert len(p) == 3
    return(-p[0], -p[1], -p[2])
    
def solve(filename):
    sensor_data = get_sensor_data(filename)
    num_sensors = len(sensor_data)
    pairwise_distances = [sorted([(dist(p1, p2), p1, p2) for p1 in sensor for p2 in sensor if p1 != p2], key = firstelem) for sensor in sensor_data]

    # Initial known sensor is sensor 0. All other positions are relative to this
    # Therefore, all beacons from sensor 0 can be directly added
    known_sensors = set([0])
    unknown_sensors = set(range(1, num_sensors))
    similarity_scores = {}
    rot_map   = {0: (1, 2, 3)}
    trans_map = {0: (0, 0, 0)}
    beacon_positions = set([beacon for beacon in sensor_data[0]])

#     actual_beacon_positions = [
# '-892,524,684',
# '-876,649,763',
# '-838,591,734',
# '-789,900,-551',
# '-739,-1745,668',
# '-706,-3180,-659',
# '-697,-3072,-689',
# '-689,845,-530',
# '-687,-1600,576',
# '-661,-816,-575',
# '-654,-3158,-753',
# '-635,-1737,486',
# '-631,-672,1502',
# '-624,-1620,1868',
# '-620,-3212,371',
# '-618,-824,-621',
# '-612,-1695,1788',
# '-601,-1648,-643',
# '-584,868,-557',
# '-537,-823,-458',
# '-532,-1715,1894',
# '-518,-1681,-600',
# '-499,-1607,-770',
# '-485,-357,347',
# '-470,-3283,303',
# '-456,-621,1527',
# '-447,-329,318',
# '-430,-3130,366',
# '-413,-627,1469',
# '-345,-311,381',
# '-36,-1284,1171',
# '-27,-1108,-65',
# '7,-33,-71',
# '12,-2351,-103',
# '26,-1119,1091',
# '346,-2985,342',
# '366,-3059,397',
# '377,-2827,367',
# '390,-675,-793',
# '396,-1931,-563',
# '404,-588,-901',
# '408,-1815,803',
# '423,-701,434',
# '432,-2009,850',
# '443,580,662',
# '455,729,728',
# '456,-540,1869',
# '459,-707,401',
# '465,-695,1988',
# '474,580,667',
# '496,-1584,1900',
# '497,-1838,-617',
# '527,-524,1933',
# '528,-643,409',
# '534,-1912,768',
# '544,-627,-890',
# '553,345,-567',
# '564,392,-477',
# '568,-2007,-577',
# '605,-1665,1952',
# '612,-1593,1893',
# '630,319,-379',
# '686,-3108,-505',
# '776,-3184,-501',
# '846,-3110,-434',
# '1135,-1161,1235',
# '1243,-1093,1063',
# '1660,-552,429',
# '1693,-557,386',
# '1735,-437,1738',
# '1749,-1800,1813',
# '1772,-405,1572',
# '1776,-675,371',
# '1779,-442,1789',
# '1780,-1548,337',
# '1786,-1538,337',
# '1847,-1591,415',
# '1889,-1729,1762',
# '1994,-1805,1792'
#     ]
    
    while len(known_sensors) != num_sensors:
        # Add one more sensor by correlating it to unknown sensors
        for (known, unknown) in [(k, u) for k in known_sensors for u in unknown_sensors]:
            if (known, unknown) not in similarity_scores:
                # print('{} {}'.format(known, unknown), end = '-')
                common_distances = calculate_similarity(pairwise_distances[known], pairwise_distances[unknown])
                similarity_scores[(known, unknown)] = len(common_distances)
                if len(common_distances) >= choose(12, 2):
                    break
        known_sensors.add(unknown)
        unknown_sensors.remove(unknown)
        # print('Learning sensor {} from sensor {}'.format(unknown, known))
        # [print(x) for x in common_distances]

        # Match unknown sensor to known (rot = rotation, trans = translation)
        trans_guesses = None
        for common_dst in common_distances:
            (d, p1k, p2k, p1u, p2u) = common_dst
            # The delta of the known sensor must match the delta of the unknown sensor
            # albeit, with a rotation. 
            # Note: known delta already has a rotation, which we account for
            # Of course, we do not know which among (p1u, p2u) is p1k and which is p2k
            # Therefore, known_delta can be +- unknown delta

            # Assume (p1u, p2u) == (p1k, p2k)
            known_delta = (p1k[0] - p2k[0], p1k[1] - p2k[1], p1k[2] - p2k[2])
            known_delta = apply_rotation(rot_map[known], known_delta)
            unknown_delta = (p1u[0] - p2u[0], p1u[1] - p2u[1], p1u[2] - p2u[2])
            if len(set(list([abs(x) for x in known_delta]))) != 3:
                continue

            # print('known {} unknown {} '.format(known_delta, unknown_delta))
            rot = find_rotation(known_delta, unknown_delta)
            # print('{} has rotation {}'.format(unknown, rot))

            if trans_guesses is None:
                # Find actual co-ordinates of beacon p1, by adding the relative distance from the known sensor, 
                # then subtracting relative distance from the unknown sensor.
                trans_guesses = set()
                trans_guesses.add(add_points(add_points(trans_map[known], apply_rotation(rot_map[known], p1k)), neg(apply_rotation(rot, p1u))))
                trans_guesses.add(add_points(add_points(trans_map[known], apply_rotation(rot_map[known], p1k)), neg(apply_rotation(neg(rot), p2u))))
                # print(trans_guesses)
                continue
            else:
                newguesses0 = add_points(add_points(trans_map[known], apply_rotation(rot_map[known], p1k)), neg(apply_rotation(rot, p1u)))
                newguesses1 = add_points(add_points(trans_map[known], apply_rotation(rot_map[known], p1k)), neg(apply_rotation(neg(rot), p2u)))
                newguesses = set([newguesses0, newguesses1])
                # print(newguesses)
                trans = trans_guesses.intersection(newguesses)
                if len(trans) != 1:
                    print(len(trans))
                assert len(trans) == 1
                trans = trans.pop()
                    
                # print('{} has position {}'.format(unknown, trans))

                rot_map[unknown] = rot if trans == newguesses0 else neg(rot)
                trans_map[unknown] = trans
                # print(rot_map)
                # print(trans_map)
                break

        for p in sensor_data[unknown]:
            beacon = add_points(trans_map[unknown], apply_rotation(rot_map[unknown], p))
            beacon_positions.add(beacon)
            # if beacon not in actual_beacon_positions:
            #     print('Error: beacon {} scanner {} original data {}'.format(beacon, unknown, p))

    # print()
    # [print(x) for x in beacon_positions]
    # print()

    print('{} has {} unique beacons'.format(filename, len(beacon_positions)))

solve('input.simp')
solve('input')
