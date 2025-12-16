from Chess_Ind.Game.chess_engine import ChessEngine
from Chess_Ind.Game.bots import RandomBot, CaptureBot, CenterControlBot

def test_bot_colors():
    """Verify bots move correct color pieces"""
    print("=== Testing Bot Colors ===")
    
    engine = ChessEngine()
    
    # Test white bots
    white_bots = [RandomBot('w'), CaptureBot('w'), CenterControlBot('w')]
    
    for bot in white_bots:
        print(f"\nTesting {type(bot).__name__} (White):")
        move = bot.get_move(engine)
        if move:
            from_sq, to_sq = move
            from_coords = engine.square_to_coords(from_sq)
            piece = engine.board[from_coords[0]][from_coords[1]]
            print(f"  Move: {from_sq}->{to_sq}, Piece: {piece}")
            
            if piece[0] == 'w':
                print("  ✓ Correct: Moving white piece")
            else:
                print("  ✗ ERROR: Moving wrong color!")
        else:
            print("  No move returned")
    
    # Test black bots
    print("\n\nTesting Black bots (need to switch turn first):")
    engine.make_move("e2", "e4")  # White moves first
    
    black_bots = [RandomBot('b'), CaptureBot('b'), CenterControlBot('b')]
    
    for bot in black_bots:
        print(f"\nTesting {type(bot).__name__} (Black):")
        move = bot.get_move(engine)
        if move:
            from_sq, to_sq = move
            from_coords = engine.square_to_coords(from_sq)
            piece = engine.board[from_coords[0]][from_coords[1]]
            print(f"  Move: {from_sq}->{to_sq}, Piece: {piece}")
            
            if piece[0] == 'b':
                print("  ✓ Correct: Moving black piece")
            else:
                print("  ✗ ERROR: Moving wrong color!")
        else:
            print("  No move returned")
    
    print("\n" + "="*60)
    print("Bot color test completed!")

def test_no_same_square_moves():
    """Verify bots don't move to same square"""
    print("\n=== Testing No Same-Square Moves ===")
    
    engine = ChessEngine()
    bots = [RandomBot('w'), CaptureBot('w'), CenterControlBot('w')]
    
    all_good = True
    for bot in bots:
        print(f"\nTesting {type(bot).__name__}:")
        
        # Test 10 times to be sure
        for i in range(10):
            move = bot.get_move(engine)
            if move:
                from_sq, to_sq = move
                if from_sq == to_sq:
                    print(f"  ✗ Failed test {i+1}: {from_sq}->{to_sq} (SAME SQUARE!)")
                    all_good = False
                else:
                    print(f"  ✓ Test {i+1}: {from_sq}->{to_sq}")
            else:
                print(f"  No move on test {i+1}")
    
    if all_good:
        print("\n✓ All bots passed: No same-square moves!")
    else:
        print("\n✗ Some bots failed: Moving to same square!")
    
    print("\n" + "="*60)
    print("Same-square test completed!")

if __name__ == "__main__":
    test_bot_colors()
    test_no_same_square_moves()