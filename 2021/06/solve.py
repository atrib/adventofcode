
def main():
    with open('input', 'r') as fd:
        inp = [int(x) for x in fd.readline().split(',')]

    max_days_to_reproduce = 8
    # Create initial count of fish
    count_age = {i: 0 for i in range(max_days_to_reproduce + 1)}
    for age in inp:
        count_age[age] += 1

    for i in range(256):
        reproducing = count_age[0]
        # Reduce age to reproduction for non-reproducing lanternfish
        for j in range(1, max_days_to_reproduce + 1):
            count_age[j - 1] = count_age[j]
        # Reproducing lanternfish create one each with 6 and 8 days
        count_age[6] += reproducing
        count_age[8] = reproducing

        # print(count_age)
    print(sum(count_age.values()))

if __name__ == '__main__':
    main()