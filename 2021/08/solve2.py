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
    0 : ['a', 'b', 'c',      'e', 'f', 'g'],
    1 : [          'c',           'f'],
    2 : ['a',      'c', 'd', 'e',      'g'],
    3 : ['a',      'c', 'd',      'f', 'g'],
    4 : ['b',      'c', 'd',      'f'],
    5 : ['a', 'b',      'd',      'f', 'g'],
    6 : ['a', 'b',      'd', 'e', 'f', 'g'],
    7 : ['a',      'c',           'f'],
    8 : ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
    9 : ['a', 'b', 'c', 'd',      'f', 'g']
}
sevensegmentoccurences = {
    c: len([1 for value in sevensegmentmaps.values() if c in value]) for c in ['a', 'b', 'c', 'd', 'e', 'f', 'g']
}

# Codes contains the number 0-9 as per sevensegmentmaps along with a replacement cipher
def determine_map(codes):
    codemap = {}
    codes.sort(key = len)

    for segs in codes:
        # print(segs)
        unknownsegs = [c for c in segs if c not in codemap]
        knownsegs   = [codemap[c] for c in segs if c in codemap]

        candidatenum = [(key, value)
                            for key, value in sevensegmentmaps.items()   # Candidate numbers must:
                            if len(value) == len(segs)                   # have same length as the current code
                            and set(knownsegs).issubset(set(value))]     # must contain all known segments

        # print('unknownsegs {}'.format(unknownsegs))
        # print(candidatenum)
        # Try to match against each candidate
        for candidate in candidatenum:
            unknownsegsreal = list(set(candidate[1]) - set(knownsegs))
            assert len(unknownsegsreal) == len(unknownsegs)
            # print(unknownsegsreal)

            tempcodemap = {}
            # Try to use occurence information to map unknownsegs to unknownsegsreal
            matching = True
            for seg in unknownsegs:
                countseg = len([x for x in codes if seg in x])
                candidatesegs = [segreal for segreal in unknownsegsreal if sevensegmentoccurences[segreal] == countseg]
                
                assert len(candidatesegs) <= 1
                if len(candidatesegs) == 0:
                    matching = False
                    break
                tempcodemap[seg] = candidatesegs[0]
            # If matching was successful, copy tempcodemap to codemap
            for k, v in tempcodemap.items():
                codemap[k] = v

        # print(codemap)
        # We can find the last map by elimination
        if len(codemap.keys()) == 6:
            knownsegs = codemap.keys()
            knownsegsreal = codemap.values()

            lastseg = [c for c in ['a', 'b', 'c', 'd', 'e', 'f', 'g'] if c not in knownsegs]
            lastsegreal = [c for c in ['a', 'b', 'c', 'd', 'e', 'f', 'g'] if c not in knownsegsreal]

            assert len(lastseg) == 1
            assert len(lastsegreal) == 1

            codemap[lastseg[0]] = lastsegreal[0]
            break

    assert len(codemap.keys()) == 7
    return codemap


def decipher_num(codemap, outs):
    num = 0

    for out in outs:
        realout = [codemap[c] for c in out]

        for i in range(10):
            if set(sevensegmentmaps[i]) == set(realout):
                num = 10 * num + i

    return num

io_re = re.compile('(([a-g]+ ){10})\|(( [a-g]+){4})')
inputs = []
outputs = []
with open('input', 'r') as fd:
    for line in fd:
        m = io_re.match(line)
        # if not m:
        #     print(line)
        inputs.append(m.group(1).strip().split())
        outputs.append(m.group(3).strip().split())

totalout = 0
for inps, outs in zip(inputs, outputs):
    codemap = determine_map(inps)
    outsnum = decipher_num(codemap, outs)
    totalout += outsnum
    # print(outsnum)

print(totalout)

