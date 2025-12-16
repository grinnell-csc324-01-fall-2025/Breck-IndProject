from Game.chess_engine import ChessEngine
from Game.bots import RandomBot, CaptureBot, CenterControlBot

class ChessGame:
    def __init__(self, white_bot=None, black_bot=None):
        self.engine = ChessEngine()
        self.white_bot = white_bot or RandomBot('w')
        self.black_bot = black_bot or RandomBot('b')
    
    def play_turn(self):
        current_color = self.engine.current_turn
        
        if current_color == 'w':
            bot = self.white_bot
        else:
            bot = self.black_bot
        
        # Get move from bot
        move = bot.get_move(self.engine)
        
        if not move:
            return None, None
        
        from_sq, to_sq = move
        
        # Make the move
        success = self.engine.make_move(from_sq, to_sq)
        
        return from_sq, to_sq if success else (None, None)
    
    def run(self, max_turns=10):
        """Run a demo game"""
        print(f"\n=== {type(self.white_bot).__name__} (White) vs {type(self.black_bot).__name__} (Black) ===")
        
        for turn in range(max_turns):
            print(f"\n--- Turn {turn + 1} ---")
            print(f"Current player: {'White' if self.engine.current_turn == 'w' else 'Black'}")
            
            # Show board
            self.engine.print_board()
            
            # Play the turn
            from_sq, to_sq = self.play_turn()
            
            if not from_sq or not to_sq:
                print("No valid move, ending game")
                break
            
            print(f"Move: {from_sq} -> {to_sq}")
            
            # Check game over
            if self.engine.is_game_over():
                result = self.engine.get_game_result()
                print(f"\nGame Over: {result}")
                break
        
        print(f"\n=== Game ended after {min(turn + 1, max_turns)} turns ===")
        self.engine.print_board()