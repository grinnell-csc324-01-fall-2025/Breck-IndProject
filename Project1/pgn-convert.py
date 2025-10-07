import chess
from chess import pgn
import os

files =[file for file in os.listdir("Data") if file.endswith(".pgn")]

print(len(files))

def load_pgn(file_path):
  games = []
  with open(file_path, 'r') as pgn_file:
    while True:
      game = pgn.read_game(pgn_file)
      if game is None:
        break
      games.append(game)
  return games

games = []
i = 1
for file in files:
  games.extend(load_pgn(f"Data/{file}"))
  print(len(games))
  if (i >= len(files)):
    break
  i += 1

print(len(games))