from Game.chess_engine import ChessEngine
from Game.bots import RandomBot

print("Testing basic bot movement...")

# Create engine and bot
engine = ChessEngine()
bot = RandomBot('w')

print("\nInitial board:")
engine.print_board()

print(f"\nCurrent turn: {'White' if engine.current_turn == 'w' else 'Black'}")

# Bot gets a move
move = bot.get_move(engine)
print(f"\nBot suggests: {move}")

if move:
    from_sq, to_sq = move
    
    # Check if squares are different
    if from_sq != to_sq:
        print(f"Moving {from_sq} -> {to_sq}")
        
        # Get piece info
        from_coords = engine.square_to_coords(from_sq)
        piece = engine.board[from_coords[0]][from_coords[1]]
        print(f"Piece: {piece} at {from_sq}")
        
        # Make the move
        success = engine.make_move(from_sq, to_sq)
        
        if success:
            print("Move successful!")
            print("\nBoard after move:")
            engine.print_board()
        else:
            print("Move failed - might be illegal")
    else:
        print("ERROR: Bot suggested moving to same square!")
else:
    print("Bot couldn't find a move")

print("\n=== Test complete ===")