from copy import deepcopy
from math import exp, floor, ceil

class snailfishnumber():
    left = None
    right = None

    def __repr__(self):
        return '[{},{}]'.format(self.left, self.right)

    def __eq__(self, __o):
        if type(__o) != snailfishnumber:
            return False
        return (self.left == __o.left) and (self.right == __o.right)

def tosnailfishnum(line):
    stack = []
    commastack = []
    tmpnum = None
    for c in line:
        # print(c)
        if c == '[':
            stack.append(snailfishnumber())
            commastack.append(False)
        elif c == ']':
            # Finish completed number
            assert commastack[-1]
            assert stack[-1].left is not None
            assert len(stack) > 0
            stack[-1].right = tmpnum
            # Pop number for use in parent
            tmpnum = stack.pop()
            assert commastack.pop() == True
        elif c == ',':
            assert not commastack[-1]
            assert stack[-1].left is None
            assert len(stack) > 0
            commastack[-1] = True
            stack[-1].left = tmpnum
            tmpnum = None
        else:
            assert c in [str(x) for x in range(0,10)]
            if tmpnum is None:
                tmpnum = 0
            tmpnum = (10*tmpnum) + int(c)
    
    return tmpnum

def addleft(number, inc):
    if type(number.left) == int:
        number.left += inc
    else:
        addleft(number.left, inc)

def addright(number, inc):
    if type(number.right) == int:
        number.right += inc
    else:
        addright(number.right, inc)

def explode_helper(depth, number):
    if depth < 4:
        leftincl = None
        rightincr = None
        # Either child which is a snailfishnumber might kaboom, or have children who do
        if type(number.left) == snailfishnumber:
            (leftincl, ownval, rightincl) = explode_helper(depth + 1, number.left)
            number.left = ownval
            if rightincl is not None:
                if type(number.right) == int:
                    number.right += rightincl
                else:
                    addleft(number.right, rightincl)
        if type(number.right) == snailfishnumber:
            (leftincr, ownval, rightincr) = explode_helper(depth + 1, number.right)
            number.right = ownval
            if leftincr is not None:
                if type(number.left) == int:
                    number.left += leftincr
                else:
                    addright(number.left, leftincr)
        # print((leftincl, number, rightincr))
        return (leftincl, number, rightincr)
    else:
        # Kaboom
        assert depth == 4
        assert type(number.left) == int
        assert type(number.right) == int
        # print( (number.left, 0, number.right))
        return (number.left, 0, number.right)

def explode(number):
    # print('explode({}) = '.format(number), end = '')
    (l, number, r) = explode_helper(0, number)
    # print(number)
    return number

assert explode(tosnailfishnum('[[[[[9,8],1],2],3],4]')) == tosnailfishnum('[[[[0,9],2],3],4]')
assert explode(tosnailfishnum('[7,[6,[5,[4,[3,2]]]]]')) == tosnailfishnum('[7,[6,[5,[7,0]]]]')
assert explode(tosnailfishnum('[[6,[5,[4,[3,2]]]],1]')) == tosnailfishnum('[[6,[5,[7,0]]],3]')
assert explode(tosnailfishnum('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]')) == tosnailfishnum('[[3,[2,[8,0]]],[9,[5,[7,0]]]]')

def split_helper(splitonce, number): 
    if splitonce:
        return (splitonce, number)

    if type(number) == int:
        if number > 9:
            newnum = snailfishnumber()
            newnum.left = int(floor(number / 2))
            newnum.right = int(ceil(number / 2))
            
            number = newnum
            splitonce = True
    else:
        (splitl, number.left) = split_helper(splitonce, number.left)
        splitonce = splitonce or splitl
        (splitr, number.right) = split_helper(splitonce, number.right)
        splitonce = splitonce or splitr

    return (splitonce, number)

def split(number):
    (splitonce, number) = split_helper(False, number)
    return number

def reduce(number):
    while True:
        numbercpy = deepcopy(number)
        number = explode(number)
        if numbercpy != number:
            # print('{} to {}'.format(numbercpy, number))
            continue

        number = split(number)
        # print('{} to {}'.format(numbercpy, number))
        if number == numbercpy:
            break

    return number

def add(num1, num2):
    if num1 == None:
        return num2

    num = snailfishnumber()
    num.left = num1
    num.right = num2
    ret = reduce(num)
    # print('{} + {} = '.format(num1, num2), end = '')
    # print(ret)
    return ret

assert add(tosnailfishnum('[[[[4,3],4],4],[7,[[8,4],9]]]'), tosnailfishnum('[1,1]')) == tosnailfishnum('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')
print()
assert add(tosnailfishnum('[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]'), tosnailfishnum('[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]')) == tosnailfishnum('[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]')

def foldleft(objects, operation):
    assert len(objects) > 0
    
    finalobj = objects[0]
    for obj in objects[1:]:
        finalobj = operation(finalobj, obj)
    #     print(finalobj)
    # print()
    return finalobj

assert foldleft([tosnailfishnum(x) for x in ['[1,1]','[2,2]','[3,3]','[4,4]']], add) == tosnailfishnum('[[[[1,1],[2,2]],[3,3]],[4,4]]')
assert foldleft([tosnailfishnum(x) for x in ['[1,1]','[2,2]','[3,3]','[4,4]','[5,5]']], add) == tosnailfishnum('[[[[3,0],[5,3]],[4,4]],[5,5]]')
assert foldleft([tosnailfishnum(x) for x in ['[1,1]','[2,2]','[3,3]','[4,4]','[5,5]','[6,6]']], add) == tosnailfishnum('[[[[5,0],[7,4]],[5,5]],[6,6]]')
_ns = ['[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
        '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]',
        '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]',
        '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]',
        '[7,[5,[[3,8],[1,4]]]]',
        '[[2,[2,2]],[8,[8,1]]]',
        '[2,9]',
        '[1,[[[9,3],9],[[9,0],[0,7]]]]',
        '[[[5,[7,4]],7],1]',
        '[[[[4,2],2],6],[8,7]]'
        ]
assert foldleft([tosnailfishnum(x) for x in _ns], add) == tosnailfishnum('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]')

def magnitude(number):
    if type(number) == int:
        return number
    else:
        return (3 * magnitude(number.left)) + (2 * magnitude(number.right))

assert magnitude(tosnailfishnum('[9,1]')) == 29
assert magnitude(tosnailfishnum('[1,9]')) == 21
assert magnitude(tosnailfishnum('[[9,1],[1,9]]')) == 129
assert magnitude(tosnailfishnum('[[1,2],[[3,4],5]]')) == 143
assert magnitude(tosnailfishnum('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')) == 1384
assert magnitude(tosnailfishnum('[[[[1,1],[2,2]],[3,3]],[4,4]]')) == 445
assert magnitude(tosnailfishnum('[[[[3,0],[5,3]],[4,4]],[5,5]]')) == 791
assert magnitude(tosnailfishnum('[[[[5,0],[7,4]],[5,5]],[6,6]]')) == 1137
assert magnitude(tosnailfishnum('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]')) == 3488
_ns = ['[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]',
        '[[[5,[2,8]],4],[5,[[9,9],0]]]',
        '[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]',
        '[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]',
        '[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]',
        '[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]',
        '[[[[5,4],[7,7]],8],[[8,3],8]]',
        '[[9,3],[[9,9],[6,[4,9]]]]',
        '[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]',
        '[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'
        ]
assert foldleft([tosnailfishnum(x) for x in _ns], add) == tosnailfishnum('[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]')
assert magnitude(foldleft([tosnailfishnum(x) for x in _ns], add)) == 4140
assert max([magnitude(add(tosnailfishnum(x), tosnailfishnum(y))) if x != y else 0 for x in _ns for y in _ns]) == 3993

inputs = [tosnailfishnum(line.strip()) for line in open('input', 'r')]
mags = [magnitude(add(deepcopy(x), deepcopy(y))) if x != y else 0 for x in inputs for y in inputs]
print(max(mags))
