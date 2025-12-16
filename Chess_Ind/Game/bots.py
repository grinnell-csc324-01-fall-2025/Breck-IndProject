import random
from typing import Tuple, Optional
from Chess_Ind.Game.chess_engine import ChessEngine

class RandomBot:
    """Bot 1: Makes random legal moves"""
    def __init__(self, color: str):
        self.color = color  # 'w' or 'b'
    
    def get_move(self, engine: ChessEngine) -> Optional[Tuple[str, str]]:
        # Get all legal moves for this bot's color
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = engine.board[row][col]
                # Check if piece belongs to this bot
                if piece != "  " and piece[0] == self.color:
                    moves = engine.get_legal_moves_for_piece((row, col))
                    for move in moves:
                        all_moves.append(((row, col), move))
        
        if not all_moves:
            return None
        
        # Choose a random move
        from_pos, to_pos = random.choice(all_moves)
        
        # Convert coordinates to algebraic notation
        from_sq = engine.coords_to_square(from_pos)
        to_sq = engine.coords_to_square(to_pos)
        
        # IMPORTANT: Debug output
        piece = engine.board[from_pos[0]][from_pos[1]]
        print(f"DEBUG RandomBot({self.color}): Moving {piece} from {from_sq} to {to_sq}")
        
        # Verify we're not moving to same square
        if from_sq == to_sq:
            # Find any valid move
            for from_pos2, to_pos2 in all_moves:
                from_sq2 = engine.coords_to_square(from_pos2)
                to_sq2 = engine.coords_to_square(to_pos2)
                if from_sq2 != to_sq2:
                    return from_sq2, to_sq2
            return None
        
        return from_sq, to_sq

class CaptureBot(RandomBot):
    """Bot 2: Prefers capturing moves"""
    def get_move(self, engine: ChessEngine) -> Optional[Tuple[str, str]]:
        # Get all legal moves for this bot's color
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = engine.board[row][col]
                if piece != "  " and piece[0] == self.color:
                    moves = engine.get_legal_moves_for_piece((row, col))
                    for move in moves:
                        all_moves.append(((row, col), move))
        
        if not all_moves:
            return None
        
        # Look for capturing moves
        capture_moves = []
        non_capture_moves = []
        
        for from_pos, to_pos in all_moves:
            # Check if this move captures a piece
            target_piece = engine.board[to_pos[0]][to_pos[1]]
            if target_piece != "  " and target_piece[0] != self.color:
                capture_moves.append((from_pos, to_pos))
            else:
                non_capture_moves.append((from_pos, to_pos))
        
        # Choose move
        if capture_moves:
            from_pos, to_pos = random.choice(capture_moves)
            move_type = "capture"
        else:
            from_pos, to_pos = random.choice(non_capture_moves)
            move_type = "non-capture"
        
        # Convert to algebraic notation
        from_sq = engine.coords_to_square(from_pos)
        to_sq = engine.coords_to_square(to_pos)
        
        # Debug output
        piece = engine.board[from_pos[0]][from_pos[1]]
        print(f"DEBUG CaptureBot({self.color}): {move_type} with {piece} from {from_sq} to {to_sq}")
        
        # Verify not same square
        if from_sq == to_sq:
            return super().get_move(engine)
        
        return from_sq, to_sq

class CenterControlBot(RandomBot):
    """Bot 3: Prefers center squares"""
    def get_move(self, engine: ChessEngine) -> Optional[Tuple[str, str]]:
        # Get all legal moves for this bot's color
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = engine.board[row][col]
                if piece != "  " and piece[0] == self.color:
                    moves = engine.get_legal_moves_for_piece((row, col))
                    for move in moves:
                        all_moves.append(((row, col), move))
        
        if not all_moves:
            return None
        
        # Score moves
        scored_moves = []
        
        for from_pos, to_pos in all_moves:
            to_row, to_col = to_pos
            
            # Distance to center (d4=3,3, e4=3,4, d5=4,3, e5=4,4)
            center_distance = min(
                abs(to_row - 3) + abs(to_col - 3),
                abs(to_row - 3) + abs(to_col - 4),
                abs(to_row - 4) + abs(to_col - 3),
                abs(to_row - 4) + abs(to_col - 4)
            )
            
            # Lower distance = better
            score = -center_distance
            
            # Bonus for captures
            target_piece = engine.board[to_row][to_col]
            if target_piece != "  " and target_piece[0] != self.color:
                score += 3
            
            scored_moves.append((score, from_pos, to_pos))
        
        # Sort by score
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        
        # Pick best move
        if scored_moves:
            _, from_pos, to_pos = scored_moves[0]
        else:
            from_pos, to_pos = all_moves[0]
        
        # Convert to algebraic notation
        from_sq = engine.coords_to_square(from_pos)
        to_sq = engine.coords_to_square(to_pos)
        
        # Debug output
        piece = engine.board[from_pos[0]][from_pos[1]]
        print(f"DEBUG CenterControlBot({self.color}): Moving {piece} from {from_sq} to {to_sq}")
        
        # Verify not same square
        if from_sq == to_sq:
            return super().get_move(engine)
        
        return from_sq, to_sq