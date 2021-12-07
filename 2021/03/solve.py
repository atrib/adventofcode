
def count_ones(nums):
  count1s = None
  
  for num in nums:
    if not count1s:
      count1s = [int(bit) for bit in num]
    else:
      assert len(num) == len(count1s)
      ones = [int(bit) for bit in num]
      count1s = [sum(val) for val in zip(ones, count1s)]
  
  return count1s

data = []
with open('input', 'r') as fd:
  for line in fd:
    data.append(line[:-1])
    
count1s = count_ones(data)

gamma = int(''.join(['1' if count > len(data)/2 else '0' for count in count1s]), 2)
epsln = int(''.join(['0' if count > len(data)/2 else '1' for count in count1s]), 2)

print('gamma = {}'.format(gamma))
print('epsilon = {}'.format(epsln))
print('gamma * epsilon = {}'.format(str(gamma * epsln)))
