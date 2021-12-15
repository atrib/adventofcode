inp = [line.strip() for line in open('input', 'r').readlines()]

total_corrupt_point = 0
corrupted_costs = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
for line in inp:
    stack = []
    corrupted = False
    for c in line:
        if c in ['(', '[', '{', '<']:
            stack.append(c)
        else:
            opener = stack.pop()
            # print('{} {}'.format(opener, c))
            if (opener == '(' and c != ')') or (opener == '[' and c != ']') or (opener == '{' and c != '}') or (opener == '<' and c != '>'):
                corrupted = True
                total_corrupt_point += corrupted_costs[c]
        if corrupted:
            break

print(total_corrupt_point)
