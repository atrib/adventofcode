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
        if not caveto == 'start':
            if not cavefrom in links:
                links[cavefrom] = set([caveto])
            else:
                links[cavefrom].add(caveto)
        if not cavefrom == 'start':
            if not caveto in links:
                links[caveto] = set([cavefrom])
            else:
                links[caveto].add(cavefrom)

        assert not (cavemajor[cavefrom] and cavemajor[caveto])

    # print(caves)
    # print(cavemajor)
    # print(links)

    paths_start_to_end = [','.join(path) for path in find_paths('start', 'end', [])]
    # paths_start_to_end.sort()
    # [print(path) for path in paths_start_to_end]
    print('{} has {} paths visiting a small cave at most once'.format(filename, len(set(paths_start_to_end))))

def path_has_double_minor(path):
    minor_caves_on_path = set()

    for cave in path:
        if cavemajor[cave]:
            continue
        
        if cave in minor_caves_on_path:
            return True
        minor_caves_on_path.add(cave)

    return False

def find_paths(cavefrom, caveto, prev_path):
    # print('findpath {} to {}'.format(cavefrom, caveto))
    assert cavefrom in caves
    assert caveto   in caves
    if cavefrom == caveto:
        return [[cavefrom]]

    prev_path = prev_path + [cavefrom]
    paths = [[cavefrom] + path  for nexthop in links[cavefrom] 
                                    if cavemajor[nexthop] or (nexthop not in prev_path) or not path_has_double_minor(prev_path)
                                        for path in find_paths(nexthop, caveto, prev_path)]
    
    # print(paths)
    return paths

solve_input('input.simp')
solve_input('input.simp2')
solve_input('input.simp3')
solve_input('input')
