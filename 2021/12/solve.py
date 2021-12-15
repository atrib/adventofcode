caves = set()
links = {}
cavemajor = {}

def solve_input(filename):
    global caves
    global links
    global cavemajor
    caves = set()
    links = {}
    cavemajor = {}
    
    for line in open(filename, 'r'):
        [cavefrom, caveto] = line.strip().split('-')

        # Add to set of caves
        caves.add(cavefrom)
        caves.add(caveto)
        # Track if caves are major or minor (small or large)
        if not cavefrom in cavemajor:
            major = True if cavefrom.upper() == cavefrom else False
            cavemajor[cavefrom] = major
        if not caveto in cavemajor:
            major = True if caveto.upper() == caveto else False
            cavemajor[caveto] = major
        # Track links
        if not cavefrom in links:
            links[cavefrom] = set([caveto])
        else:
            links[cavefrom].add(caveto)
        if not caveto in links:
            links[caveto] = set([cavefrom])
        else:
            links[caveto].add(cavefrom)

        assert not (cavemajor[cavefrom] and cavemajor[caveto])

    # print(caves)
    # print(cavemajor)
    # print(links)

    paths_start_to_end = find_paths('start', 'end', [])
    print('{} has {} paths visiting a small cave at most once'.format(filename, len(paths_start_to_end)))

def find_paths(cavefrom, caveto, prev_path):
    # print('findpath {} to {}'.format(cavefrom, caveto))
    assert cavefrom in caves
    assert caveto   in caves
    if cavefrom == caveto:
        return [[cavefrom]]

    prev_path = prev_path + [cavefrom]
    paths = [[cavefrom] + path  for nexthop in links[cavefrom] if (not(nexthop) in prev_path) or cavemajor[nexthop]
                                for path in find_paths(nexthop, caveto, prev_path)]
    
    # print(paths)
    return paths

solve_input('input.simp')
solve_input('input.simp2')
solve_input('input')
