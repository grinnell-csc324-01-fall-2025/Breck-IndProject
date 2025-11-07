import chess
from chess import pgn
import os
from tqdm import tqdm

files =["lichess_elite_2020-12.pgn"]#file for file in os.listdir("Data") if file.endswith(".pgn")]

print(len(files))

# Load_pgn takes a pgn file_path and returns an array of the files as now readable games
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
for file in tqdm(files):
  games.extend(load_pgn(f"Data/{file}"))
  if i >= 2:
    break
  i += 1

print(len(games))