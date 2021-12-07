
def xor(x, y):
  return bool((x and not y) or (not x and y))
  
def count_ones(nums):
  count1s = None
  
  for num in nums:
    if not count1s:
      count1s = [int(bit) for bit in num]
    else:
      assert len(num) == len(count1s), 'num is {}  and count1s is {}'.format(num, count1s)
      ones = [int(bit) for bit in num]
      count1s = [sum(val) for val in zip(ones, count1s)]
  
  return count1s

def filter_nums(nums, pos, majority = True):
  count1s = count_ones(nums)
  filterval = '1' if xor(not majority, count1s[pos] >= len(nums)/2) else '0'
  return [num  for num in nums if num[pos] == filterval]

def main():
  data = []
  with open('input', 'r') as fd:
    for line in fd:
      data.append(line[:-1])
      
  width = len(data[0])
  oxygen_lines = data
  for i in range(width):
    # print(oxygen_lines)
    oxygen_lines = filter_nums(oxygen_lines, i, majority = True)
    if(len(oxygen_lines) == 1):
      break
  assert(len(oxygen_lines) == 1)

  co2_lines = data
  for i in range(width):
    # print(co2_lines)
    co2_lines = filter_nums(co2_lines, i, majority = False)
    if(len(co2_lines) == 1):
      break
  assert(len(co2_lines) == 1)
  
  o2 = int(oxygen_lines[0], 2)
  co2 = int(co2_lines[0], 2)
    
  print('o2 = {}'.format(o2))
  print('co2 = {}'.format(co2))
  print('o2 * co2 = {}'.format(str(o2 * co2)))

if __name__ == '__main__':
  main()