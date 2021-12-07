
def update_board(board, inp):
  board = [[(num, True) if seen or (inp == num) else (num, False) 
            for (num, seen) in row] 
            for row in board]
  
  return board

def is_complete(board):
  rowscomplete = [True] * len(board)
  colscomplete = [True] * len(board[0])
  # Check rows
  for i in range(len(board)):
    for j in range(len(board[0])):
      rowscomplete[i] &= board[i][j][1]
      colscomplete[j] &= board[i][j][1]
      
  return (True in rowscomplete) or (True in colscomplete)

def main():  
  lines = []
  with open('input', 'r') as fd:
    for line in fd:
      lines.append(line[:-1])
  
  inputs = [int(val) for val in lines[0].split(',')]
  
  num_boards = int((len(lines) - 1) / 6)
  boards = []
  for i in range(num_boards):
    board = []
    for j in range(5):
      row = [(int(x), False)  for x in lines[2 + (i * 6) + j].split()]
      board.append(row)
    boards.append(board)
    
  for inp in inputs:
    # print(inp)
    boards = [update_board(board, inp) for board in boards]
    # Remove completed boards
    lastboard = boards[0]
    boards = [board for board in boards if not is_complete(board)]

    if(len(boards) == 0):
      # Calculate output and end
      unmarked = [val for row in lastboard for (val, seen) in row if not seen]
      print(sum(unmarked))
      print(sum(unmarked) * inp)     
      return 
  
if __name__ == '__main__':
  main()