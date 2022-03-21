import re

class deterministic_dice():
    nextcount = None
    maxcount = None
    nrolls = None

    def __init__(self, maxcount):
        self.nextcount = 1
        self.maxcount = maxcount
        self.nrolls = 0

    def roll(self):
        self.nrolls += 1
        ret = self.nextcount
        self.nextcount += 1
        if self.nextcount > self.maxcount:
            self.nextcount = 1

        return ret

def solve(filename):
    startpos_re = re.compile('Player ([0-9]+) starting position: ([0-9]+)')
    lines = [line.strip() for line in open(filename, 'r')]
    playerpos = {}
    for line in lines:
        startpos_m = startpos_re.match(line)
        assert startpos_m is not None
        playerpos[int(startpos_m.group(1))] = int(startpos_m.group(2))
    playerscore = {player: 0 for player in playerpos.keys()}

    dice = deterministic_dice(100)
    nrolls = 3
    maxscore = 1000
    nspaces = 10
    winner = None
    while winner is None:
        for player, pos in playerpos.items():
            rolls = [dice.roll() for _ in range(nrolls)]

            assert pos >= 1 and pos <= nspaces
            newpos = (((pos - 1) + sum(rolls)) % nspaces) + 1
            playerpos[player] = newpos

            score = playerscore[player]
            score += newpos
            playerscore[player] = score
            if score >= maxscore:
                winner = player
                break
                
        # print(playerpos)
        # print(playerscore)

    # print(playerpos)
    # print(playerscore)
    losingscore = playerscore[2 if winner == 1 else 1]
    print('{}: (losingscore = {}) * (nrolls = {}) = {}'.format(filename, losingscore, dice.nrolls, losingscore * dice.nrolls))

solve('input.simp')
solve('input')
