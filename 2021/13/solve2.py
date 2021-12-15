import re

def apply_fold(dots, fold):
    (dim, val) = fold
    dots_folded = set()
    for dot in dots:
        (x, y) = dot
        if dim == 'x':
            assert x != val
            dots_folded.add((val - (x - val) if x > val else x, y))
        else:
            assert dim == 'y'
            assert y != val
            dots_folded.add((x, val - (y - val) if y > val else y))
    
    return list(dots_folded)

def print_code(dots):
    maxx = maxy = 0
    for (x,y) in dots:
        maxx = max(maxx, x)
        maxy = max(maxy, y)
    dots = set(dots)
    for j in range(maxy + 1):
        for i in range(maxx + 1):
            if (i, j) in dots:
                print('#', end = '')
            else:
                print('.', end = '')
        print()

fold_re = re.compile('fold along (x|y)=([0-9]+)')
def solve(inp_filename):
    lines = [line.strip() for line in open(inp_filename, 'r')]
    # Get dots and folds
    dots = [(int(x), int(y)) for [x,y] in [line.split(',') for line in lines if ',' in line]]
    folds = []
    for line in lines[len(dots) + 1:]:
        m = fold_re.match(line)
        assert m
        folds.append((m.group(1), int(m.group(2))))
    
    for fold in folds:
        dots = apply_fold(dots, fold)
    print_code(dots)

def main():
    solve('input.simp')
    solve('input')

if __name__ == '__main__':
    main()