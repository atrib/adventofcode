import re

def solve(filename):
    startpos_re = re.compile('Player ([0-9]+) starting position: ([0-9]+)')
    lines = [line.strip() for line in open(filename, 'r')]
    playerpos = {}
    for line in lines:
        startpos_m = startpos_re.match(line)
        assert startpos_m is not None
        playerpos[int(startpos_m.group(1))] = int(startpos_m.group(2))

    nspaces = 10
    maxscore = 21
    # universe_summary = {(p1pos, p2pos, p1score, p2score, turn) = nuniverses}
    universe_summary = {((p1pos, p2pos), (p1score, p2score), turn): 0 
                            for p1pos in range(1, nspaces + 1) 
                            for p2pos in range(1, nspaces + 1) 
                            for p1score in range(maxscore) 
                            for p2score in range(maxscore)
                            for turn in playerpos.keys()
                        }
    universe_summary[((playerpos[1], playerpos[2]), (0, 0), 1)] = 1
    # print(len(universe_summary))
    # [print('{}: {}'.format(key, val)) for key, val in universe_summary.items() if val > 0]

    nwins = {player: 0 for player in playerpos.keys()}
    dicefaces = 3
    rolls = [(r1 + 1, r2 + 1, r3 + 1) for r1 in range(dicefaces) for r2 in range(dicefaces) for r3 in range(dicefaces)]
    while sum(universe_summary.values()) != 0:
        new_universe_summary = {((p1pos, p2pos), (p1score, p2score), turn): 0 
                                    for p1pos in range(1, nspaces + 1) 
                                    for p2pos in range(1, nspaces + 1) 
                                    for p1score in range(maxscore) 
                                    for p2score in range(maxscore)
                                    for turn in playerpos.keys()
                                }
        
        for (poss, scores, turn), nuniverses in universe_summary.items():
            if nuniverses == 0:
                continue

            for roll in rolls:
                newpos = (((poss[turn - 1] - 1) + sum(roll)) % nspaces) + 1
                newscore = scores[turn - 1] + newpos

                if newscore >= maxscore:
                    nwins[turn] += nuniverses
                else:
                    newposs = (newpos, poss[1]) if turn == 1 else (poss[0], newpos)
                    newscores = (newscore, scores[1]) if turn == 1 else (scores[0], newscore)
                    # print('{} {} {} {} '.format(newpos, newscore, newposs, newscores))
                    new_universe_summary[(newposs, newscores, 2 if turn == 1 else 1)] += nuniverses

        universe_summary = new_universe_summary
    
    winning_universes = max(nwins.values())
    winner = {val: key for key, val in nwins.items()}[winning_universes]
    print('Player {} wins {} times'.format(winner, winning_universes))

solve('input.simp')
solve('input')
