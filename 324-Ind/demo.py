"""Demo of Chess Engine with Three Bots"""
from Game.game import ChessGame
from Game.bots import RandomBot, CaptureBot, CenterControlBot

print("=== Chess Engine with Three Bots ===")
print("Testing different bot strategies against each other")

print("\n" + "="*60)
print("GAME 1: Random Bot vs Capture Bot")
print("="*60)
game1 = ChessGame(RandomBot('w'), CaptureBot('b'))
game1.run(max_turns=6)

print("\n" + "="*60)
print("GAME 2: Capture Bot vs Center Control Bot")
print("="*60)
game2 = ChessGame(CaptureBot('w'), CenterControlBot('b'))
game2.run(max_turns=6)

print("\n" + "="*60)
print("GAME 3: Center Control Bot vs Random Bot")
print("="*60)
game3 = ChessGame(CenterControlBot('w'), RandomBot('b'))
game3.run(max_turns=6)

print("\n" + "="*60)
print("ALL TESTS COMPLETED!")
print("="*60)