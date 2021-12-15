def median(lst):
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // 2
   
    if (lstLen % 2):
        return sortedLst[index]
    else:
        return (sortedLst[index] + sortedLst[index + 1])/2.0

inp = [line.strip() for line in open('input', 'r').readlines()]

completion_scores = []
completion_score = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}
for line in inp:
    stack = []
    corrupted = False
    for c in line:
        if c in ['(', '[', '{', '<']:
            stack.append(c)
        else:
            opener = stack.pop()
            if (opener == '(' and c != ')') or (opener == '[' and c != ']') or (opener == '{' and c != '}') or (opener == '<' and c != '>'):
                corrupted = True
        if corrupted:
            break
    
    incomplete_score = 0
    if not corrupted and len(stack) > 0:
        # Calculate cost of completion
        for c in stack[::-1]:
            incomplete_score = (5 * incomplete_score) + completion_score[c]
        completion_scores.append(incomplete_score)

assert len(completion_scores) % 2 == 1
print(median(completion_scores))

# {([(<[ }>{[]{[(<()>