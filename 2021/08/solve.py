import re

#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....

#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg

sevensegmentmaps = {
    0 : ['a', 'b', 'c', 'e', 'f', 'g'],
    1 : ['c', 'f'],
    2 : ['a', 'c', 'd', 'e', 'g'],
    3 : ['a', 'c', 'd', 'f', 'g'],
    4 : ['b', 'c', 'd', 'f'],
    5 : ['a', 'b', 'd', 'f', 'g'],
    6 : ['a', 'b', 'd', 'e', 'f', 'g'],
    7 : ['a', 'c', 'f'],
    8 : ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
    9 : ['a', 'b', 'c', 'd', 'f', 'g']
}

possible_maps = {
    i: set(['a', 'b', 'c', 'd', 'e', 'f', 'g']) for i in ['a', 'b', 'c', 'd', 'e', 'f', 'g']
}

# Refine the set of possible mappings
def refine_map(num):
    print(num)
    # Use the set of possible actual numbers to refine the possible mapping
    possible_nums = [key for key, value in sevensegmentmaps.items() if len(value) == len(num)]
    actual_segments = set()
    [actual_segments.add(segment) for possible_num in possible_nums for segment in sevensegmentmaps[possible_num]]
    print(actual_segments)
    for c in num:
        possible_maps[c] = possible_maps[c].intersection(actual_segments)
    pass
    print(possible_maps)

def identify_unique(num):
    possible_nums = [key for key, value in sevensegmentmaps.items() if len(value) == len(num)]
    if len(possible_nums) == 1:
        return possible_nums[0]
    else:
        return None

io_re = re.compile('(([a-g]+ ){10})\|(( [a-g]+){4})')
inputs = []
outputs = []
with open('input', 'r') as fd:
    for line in fd:
        m = io_re.match(line)
        inputs.append(m.group(1).strip().split())
        outputs.append(m.group(3).strip().split())

# for inps, outs in zip(inputs, outputs):
#     [refine_map(inp) for inp in inps]
#     [refine_map(out) for out in outs]

# print(possible_maps)

sum = 0
for outs in outputs:
    for out in outs:
        n = identify_unique(out)
        if n:
            sum += 1

print(sum)
