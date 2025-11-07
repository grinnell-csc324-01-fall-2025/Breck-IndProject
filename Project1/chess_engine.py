import chess

def Board():
  board = [0] * 8
  for i in range(len(board)):
      board[i] = ["  "] * 8 # type: ignore
  return board

def Print_Board(board):
  for i, row in enumerate(board):
    print(8 - i, end = ": ")
    for j, col in enumerate(row):
      print(col, end = " ")
    print("\n")
  print(" " * 3 + "a" + " " * 2 + "b" + " " * 2 + "c" + " " * 2 + "d" + " " * 2 + "e" + " " * 2 + "f" + " " * 2 + "g" + " " * 2 + "h")

White_pieces_map = {
    "wP": [(6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7)],
    "wN": [(7, 1), (7, 6)],
    "wB": [(7, 2), (7, 5)],
    "wR": [(7, 0), (7, 7)],
    "wQ": [(7, 3)],
    "wK": [(7, 4)],
  }

Black_pieces_map = {
    "bP": [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],
    "bN": [(0, 1), (0, 6)],
    "bB": [(0, 2), (0, 5)],
    "bR": [(0, 0), (0, 7)],
    "bQ": [(0, 3)],
    "bK": [(0, 4)],
  }

letter_map = {
  "a": 0,
  "b": 1,
  "c": 2,
  "d": 3,
  "e": 4,
  "f": 5,
  "g": 6,
  "h": 7,
}

def place_pieces(board):
  # White pieces
  for piece, squares in White_pieces_map.items():
    for square in squares:
      x, y = square[0], square[1]
      board[x][y] = piece
  
  # Black pieces
  for piece, squares in Black_pieces_map.items():
    for square in squares:
      x, y = square[0], square[1]
      board[x][y] = piece
  return board


board = Board()
place_pieces(board)
curr_turn = 1


while(True):
  Print_Board(board)
  print("")

  curr_player = ""
  if curr_turn % 2 == 1:
    curr_player = "White"
  else:
    curr_player = "Black"
  curr_turn += 1

  print(curr_player + "'s current turn!\n")
  
  start_sq = input("Enter the square of the piece you want to move: ")
  starty, startx = start_sq[0], start_sq[1]
  starty = letter_map[starty]
  startx = 8 - int(startx)

  end_sq = input("Enter the square where you want to move the piece to: ")
  endy, endx = end_sq[0], end_sq[1]
  endy = letter_map[endy]
  endx = 8 - int(endx)

  temp = board[startx][starty]
  board[startx][starty] = "  "
  board[endx][endy] = temp
