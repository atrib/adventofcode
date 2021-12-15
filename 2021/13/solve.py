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
    
    dots = apply_fold(dots, folds[0])
    print('{} dots after one fold'.format(len(dots)))

def main():
    solve('input.simp')
    solve('input')

if __name__ == '__main__':
    main()