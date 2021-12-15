
def solve(filename):
    lines = [line.strip() for line in open(filename, 'r')]

    # Enumerate initial pairs
    paircounts = {}
    template = lines[0]
    for i in range(len(template) - 1):
        pair = template[i:i+2]
        if not pair in paircounts:
            paircounts[pair] = 1
        else:
            paircounts[pair] += 1
    # print(paircounts)

    # Read out rules and make pairs
    insertionpairs = {}
    for line in lines[2:]:
        sourcepair = line[0:2]
        extrachar = line[6]
        assert sourcepair not in insertionpairs
        insertionpairs[sourcepair] = [sourcepair[0] + extrachar, extrachar + sourcepair[1]]
    # print(insertionpairs)

    # Expand protein for n steps
    nsteps = 40
    for i in range(nsteps):
        newpaircounts = {}

        for pair in paircounts.keys():
            outpairs = insertionpairs[pair]
            ntimes = paircounts[pair]
            for px in outpairs:
                if px in newpaircounts:
                    newpaircounts[px] += ntimes
                else:
                    newpaircounts[px] = ntimes

        paircounts = newpaircounts
    # print('step {} has len {}'.format(i, int(sum(paircounts.values())/2) + 1))

    # Count individual protiens
    protcounts = {}
    for protpair, ntimes in paircounts.items():
        for prot in protpair:
            if prot in protcounts:
                protcounts[prot] += ntimes / 2
            else:
                protcounts[prot] = ntimes / 2
    protcounts[template[0]] += 1/2
    protcounts[template[-1]] += 1/2
    # print(protcounts)

    maxcount = max(protcounts.values())
    mincount = min(protcounts.values())
    print('{} has difference {}'.format(filename, int(maxcount - mincount)))
    
solve('input.simp')
solve('input')
