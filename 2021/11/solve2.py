def print_octopi(octopi):
    for row in octopi:
        for (octopus, flashed) in row:
            print('{}'.format(octopus), end='')
        print()
    print()

def step(octopi):
    def increment(i, j):
        if (i < 0) or (j < 0) or (i >= len(octopi)) or (j >= len(octopi[0])):
            return

        (energy, flashed) = octopi[i][j]
        if energy != 9:
            octopi[i][j] = (energy + 1, flashed)
        else:
            octopi[i][j] = (energy + 1, True)
            [increment(i_dash, j_dash)  for i_dash in range(i - 1, i + 2) 
                                        for j_dash in range(j - 1, j + 2) 
                                            if (i_dash, j_dash) != (i, j)
                                                and i_dash >= 0 and i_dash < len(octopi)
                                                and j_dash >= 0 and j_dash < len(octopi[0])
                                            ]

    for i in range(len(octopi)):
        for j in range(len(octopi[0])):
            increment(i, j)

    num_flashes = 0
    for i in range(len(octopi)):
        for j in range(len(octopi[0])):
            (energy, flashed) = octopi[i][j]
            if flashed:
                assert energy > 9
                num_flashes += 1
                octopi[i][j] = (0, False)
            else:
                assert energy <= 9

    return (octopi, num_flashes)

octopi = [[int(octopus) for octopus in line.strip()] for line in open('input', 'r')]

# Add tag for whether an octopus has flashed
octopi = [[(octopus, False) for octopus in row] for row in octopi]

step_count = 0
while True:
    # Step
    (octopi, num_flashes) = step(octopi)
    step_count += 1
    if num_flashes == len(octopi) * len(octopi[0]):
        print(step_count)
        break
