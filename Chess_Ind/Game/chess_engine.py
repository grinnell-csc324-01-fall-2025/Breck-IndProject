class ChessEngine:
    def __init__(self, fen_string=None):
        """
        Initialize chess board.
        If fen_string is provided, load from FEN notation.
        Otherwise, start with standard position.
        """
        self.board = [["  " for _ in range(8)] for _ in range(8)]
        self.current_turn = 'w'  # 'w' for white, 'b' for black
        self.castling_rights = {'wK': True, 'wQ': True, 'bK': True, 'bQ': True}
        self.en_passant_target = None  # Square where en passant capture is possible
        self.halfmove_clock = 0  # Moves since last capture or pawn advance
        self.fullmove_number = 1
        self.move_history = []
        
        if fen_string:
            self.load_from_fen(fen_string)
        else:
            self.setup_initial_position()
    
    def setup_initial_position(self):
        """Set up standard starting position"""
        # Place white pieces
        self.board[7][0] = "wR"
        self.board[7][1] = "wN"
        self.board[7][2] = "wB"
        self.board[7][3] = "wQ"
        self.board[7][4] = "wK"
        self.board[7][5] = "wB"
        self.board[7][6] = "wN"
        self.board[7][7] = "wR"
        for i in range(8):
            self.board[6][i] = "wP"
        
        # Place black pieces
        self.board[0][0] = "bR"
        self.board[0][1] = "bN"
        self.board[0][2] = "bB"
        self.board[0][3] = "bQ"
        self.board[0][4] = "bK"
        self.board[0][5] = "bB"
        self.board[0][6] = "bN"
        self.board[0][7] = "bR"
        for i in range(8):
            self.board[1][i] = "bP"
    
    def load_from_fen(self, fen_string):
        """Load position from FEN notation"""
        parts = fen_string.split()
        if len(parts) < 4:
            raise ValueError("Invalid FEN string")
        
        # Parse board position
        board_part = parts[0]
        rows = board_part.split('/')
        if len(rows) != 8:
            raise ValueError("FEN must have 8 rows")
        
        for row_idx, row in enumerate(rows):
            col_idx = 0
            for char in row:
                if char.isdigit():
                    col_idx += int(char)
                else:
                    color = 'w' if char.isupper() else 'b'
                    piece_type = char.upper()
                    self.board[row_idx][col_idx] = f"{color}{piece_type}"
                    col_idx += 1
        
        # Parse current turn
        self.current_turn = parts[1].lower()
        
        # Parse castling rights
        self.castling_rights = {'wK': False, 'wQ': False, 'bK': False, 'bQ': False}
        if parts[2] != '-':
            for char in parts[2]:
                if char == 'K': self.castling_rights['wK'] = True
                elif char == 'Q': self.castling_rights['wQ'] = True
                elif char == 'k': self.castling_rights['bK'] = True
                elif char == 'q': self.castling_rights['bQ'] = True
        
        # Parse en passant target
        if parts[3] != '-':
            self.en_passant_target = self.square_to_coords(parts[3])
        else:
            self.en_passant_target = None
    
    def square_to_coords(self, square):
        """Convert algebraic notation to board coordinates"""
        if len(square) != 2:
            return None
        col = ord(square[0]) - ord('a')
        row = 8 - int(square[1])
        return (row, col)
    
    def coords_to_square(self, coords):
        """Convert board coordinates to algebraic notation"""
        row, col = coords
        if 0 <= row < 8 and 0 <= col < 8:
            return f"{chr(col + ord('a'))}{8 - row}"
        return None
    
    def get_piece_at(self, square):
        """Get piece at given square"""
        coords = self.square_to_coords(square) if isinstance(square, str) else square
        if coords:
            row, col = coords
            return self.board[row][col]
        return None
    
    def is_valid_square(self, square):
        """Check if square is valid"""
        if isinstance(square, str):
            coords = self.square_to_coords(square)
        else:
            coords = square
        if not coords:
            return False
        row, col = coords
        return 0 <= row < 8 and 0 <= col < 8
    
    def get_all_legal_moves(self, color=None):
        """Get all legal moves for the given color"""
        if color is None:
            color = self.current_turn
        
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != "  " and piece[0] == color:
                    moves = self.get_legal_moves_for_piece((row, col))
                    all_moves.extend([((row, col), move) for move in moves])
        
        return all_moves
    
        # Add to ChessEngine class in chess_engine.py
    def get_all_legal_moves_as_strings(self, color=None):
        """Get all legal moves as algebraic notation strings"""
        if color is None:
            color = self.current_turn
        
        move_strings = []
        for from_pos, to_pos in self.get_all_legal_moves(color):
            from_sq = self.coords_to_square(from_pos)
            to_sq = self.coords_to_square(to_pos)
            if from_sq and to_sq:
                move_strings.append((from_sq, to_sq))
        
        return move_strings
    
    def get_legal_moves_for_piece(self, position):
        """Get legal moves for a specific piece"""
        row, col = position
        piece = self.board[row][col]
        if piece == "  ":
            return []
        
        color = piece[0]
        piece_type = piece[1]
        
        # Get pseudo-legal moves (moves without checking for self-check)
        pseudo_moves = []
        
        if piece_type == 'P':  # Pawn
            pseudo_moves = self._get_pawn_moves(row, col, color)
        elif piece_type == 'N':  # Knight
            pseudo_moves = self._get_knight_moves(row, col, color)
        elif piece_type == 'B':  # Bishop
            pseudo_moves = self._get_bishop_moves(row, col, color)
        elif piece_type == 'R':  # Rook
            pseudo_moves = self._get_rook_moves(row, col, color)
        elif piece_type == 'Q':  # Queen
            pseudo_moves = self._get_queen_moves(row, col, color)
        elif piece_type == 'K':  # King
            pseudo_moves = self._get_king_moves(row, col, color)
        
        # Filter out moves that leave king in check
        legal_moves = []
        for move in pseudo_moves:
            if self._is_move_legal((row, col), move, color):
                legal_moves.append(move)
        
        return legal_moves
    
    def _get_pawn_moves(self, row, col, color):
        """Calculate pawn moves"""
        moves = []
        direction = -1 if color == 'w' else 1  # White moves up (decreasing row), black down
        
        # One square forward
        new_row = row + direction
        if 0 <= new_row < 8 and self.board[new_row][col] == "  ":
            moves.append((new_row, col))
            
            # Two squares forward from starting position
            if ((color == 'w' and row == 6) or (color == 'b' and row == 1)):
                new_row2 = row + 2 * direction
                if self.board[new_row2][col] == "  ":
                    moves.append((new_row2, col))
        
        # Captures (including en passant)
        for dcol in [-1, 1]:
            new_col = col + dcol
            new_row = row + direction
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                # Normal capture
                target = self.board[new_row][new_col]
                if target != "  " and target[0] != color:
                    moves.append((new_row, new_col))
                
                # En passant capture
                if self.en_passant_target == (new_row, new_col):
                    moves.append((new_row, new_col))
        
        return moves
    
    def _get_knight_moves(self, row, col, color):
        """Calculate knight moves"""
        moves = []
        knight_moves = [
            (row-2, col-1), (row-2, col+1),
            (row-1, col-2), (row-1, col+2),
            (row+1, col-2), (row+1, col+2),
            (row+2, col-1), (row+2, col+1)
        ]
        
        for r, c in knight_moves:
            if 0 <= r < 8 and 0 <= c < 8:
                target = self.board[r][c]
                if target == "  " or target[0] != color:
                    moves.append((r, c))
        
        return moves
    
    def _get_bishop_moves(self, row, col, color):
        """Calculate bishop moves"""
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = self.board[r][c]
                if target == "  ":
                    moves.append((r, c))
                else:
                    if target[0] != color:
                        moves.append((r, c))
                    break
                r += dr
                c += dc
        
        return moves
    
    def _get_rook_moves(self, row, col, color):
        """Calculate rook moves"""
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = self.board[r][c]
                if target == "  ":
                    moves.append((r, c))
                else:
                    if target[0] != color:
                        moves.append((r, c))
                    break
                r += dr
                c += dc
        
        return moves
    
    def _get_queen_moves(self, row, col, color):
        """Calculate queen moves (bishop + rook)"""
        return self._get_bishop_moves(row, col, color) + self._get_rook_moves(row, col, color)
    
    def _get_king_moves(self, row, col, color):
        """Calculate king moves including castling"""
        moves = []
        
        # Normal king moves
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    target = self.board[r][c]
                    if target == "  " or target[0] != color:
                        # Temporarily make move to check if square is attacked
                        moves.append((r, c))
        
        # Castling moves
        if color == 'w':
            # Kingside castling
            if (self.castling_rights['wK'] and 
                self.board[7][5] == "  " and 
                self.board[7][6] == "  " and
                not self.is_square_attacked((7, 4), 'b') and
                not self.is_square_attacked((7, 5), 'b') and
                not self.is_square_attacked((7, 6), 'b')):
                moves.append((7, 6))
            
            # Queenside castling
            if (self.castling_rights['wQ'] and 
                self.board[7][1] == "  " and 
                self.board[7][2] == "  " and
                self.board[7][3] == "  " and
                not self.is_square_attacked((7, 4), 'b') and
                not self.is_square_attacked((7, 3), 'b') and
                not self.is_square_attacked((7, 2), 'b')):
                moves.append((7, 2))
        else:
            # Black kingside castling
            if (self.castling_rights['bK'] and 
                self.board[0][5] == "  " and 
                self.board[0][6] == "  " and
                not self.is_square_attacked((0, 4), 'w') and
                not self.is_square_attacked((0, 5), 'w') and
                not self.is_square_attacked((0, 6), 'w')):
                moves.append((0, 6))
            
            # Black queenside castling
            if (self.castling_rights['bQ'] and 
                self.board[0][1] == "  " and 
                self.board[0][2] == "  " and
                self.board[0][3] == "  " and
                not self.is_square_attacked((0, 4), 'w') and
                not self.is_square_attacked((0, 3), 'w') and
                not self.is_square_attacked((0, 2), 'w')):
                moves.append((0, 2))
        
        return moves
    
    def is_square_attacked(self, square, by_color):
        """Check if a square is attacked by pieces of given color"""
        row, col = square
        
        # Check knight attacks
        knight_moves = [
            (row-2, col-1), (row-2, col+1),
            (row-1, col-2), (row-1, col+2),
            (row+1, col-2), (row+1, col+2),
            (row+2, col-1), (row+2, col+1)
        ]
        for r, c in knight_moves:
            if 0 <= r < 8 and 0 <= c < 8:
                piece = self.board[r][c]
                if piece != "  " and piece[0] == by_color and piece[1] == 'N':
                    return True
        
        # Check pawn attacks
        pawn_dir = 1 if by_color == 'w' else -1  # Pawns attack forward-up for white
        for dc in [-1, 1]:
            r, c = row + pawn_dir, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                piece = self.board[r][c]
                if piece != "  " and piece[0] == by_color and piece[1] == 'P':
                    return True
        
        # Check king attacks
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    piece = self.board[r][c]
                    if piece != "  " and piece[0] == by_color and piece[1] == 'K':
                        return True
        
        # Check sliding pieces (queen, rook, bishop)
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                piece = self.board[r][c]
                if piece != "  ":
                    if piece[0] == by_color:
                        piece_type = piece[1]
                        # Check if piece can attack in this direction
                        if dr == 0 or dc == 0:  # Rook or Queen direction
                            if piece_type in ['R', 'Q']:
                                return True
                        else:  # Bishop or Queen direction
                            if piece_type in ['B', 'Q']:
                                return True
                    break
                r += dr
                c += dc
        
        return False
    
    def _is_move_legal(self, from_pos, to_pos, color):
        """Check if a move doesn't leave king in check"""
        # Make a copy of the board and try the move
        board_copy = [row[:] for row in self.board]
        
        # Make the move on the copy
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        moving_piece = board_copy[from_row][from_col]
        captured_piece = board_copy[to_row][to_col]
        
        # Handle en passant capture
        is_en_passant = False
        if moving_piece[1] == 'P' and captured_piece == "  " and from_col != to_col:
            if self.en_passant_target == (to_row, to_col):
                is_en_passant = True
                # Remove the captured pawn
                captured_row = to_row + 1 if color == 'w' else to_row - 1
                board_copy[captured_row][to_col] = "  "
        
        # Move the piece
        board_copy[to_row][to_col] = moving_piece
        board_copy[from_row][from_col] = "  "
        
        # Handle castling - move rook too
        if moving_piece[1] == 'K' and abs(from_col - to_col) == 2:
            # Kingside castling
            if to_col > from_col:
                board_copy[to_row][5] = board_copy[to_row][7]
                board_copy[to_row][7] = "  "
            # Queenside castling
            else:
                board_copy[to_row][3] = board_copy[to_row][0]
                board_copy[to_row][0] = "  "
        
        # Find king position
        king_pos = None
        for r in range(8):
            for c in range(8):
                piece = board_copy[r][c]
                if piece == f"{color}K":
                    king_pos = (r, c)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False
        
        # Check if king is in check
        opponent_color = 'b' if color == 'w' else 'w'
        return not self._is_king_in_check_on_board(board_copy, king_pos, opponent_color)
    
    def _is_king_in_check_on_board(self, board, king_pos, opponent_color):
        """Check if king is in check on a given board"""
        return self.is_square_attacked_on_board(board, king_pos, opponent_color)
    
    def is_square_attacked_on_board(self, board, square, by_color):
        """Check if a square is attacked on a given board"""
        row, col = square
        
        # Similar logic to is_square_attacked but using given board
        # (Implement simplified version for brevity)
        # Check immediate surroundings for kings
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    piece = board[r][c]
                    if piece != "  " and piece[0] == by_color and piece[1] == 'K':
                        return True
        
        # Check knights
        knight_moves = [
            (row-2, col-1), (row-2, col+1),
            (row-1, col-2), (row-1, col+2),
            (row+1, col-2), (row+1, col+2),
            (row+2, col-1), (row+2, col+1)
        ]
        for r, c in knight_moves:
            if 0 <= r < 8 and 0 <= c < 8:
                piece = board[r][c]
                if piece != "  " and piece[0] == by_color and piece[1] == 'N':
                    return True
        
        # Check pawns
        pawn_dir = 1 if by_color == 'w' else -1
        for dc in [-1, 1]:
            r, c = row + pawn_dir, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                piece = board[r][c]
                if piece != "  " and piece[0] == by_color and piece[1] == 'P':
                    return True
        
        # Check sliding pieces
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                piece = board[r][c]
                if piece != "  ":
                    if piece[0] == by_color:
                        piece_type = piece[1]
                        if dr == 0 or dc == 0:  # Rook/Queen direction
                            if piece_type in ['R', 'Q']:
                                return True
                        else:  # Bishop/Queen direction
                            if piece_type in ['B', 'Q']:
                                return True
                    break
                r += dr
                c += dc
        
        return False
    
    def make_move(self, from_square, to_square, promotion_piece='Q'):
        """
        Make a move on the board.
        Returns True if move was successful, False otherwise.
        """
        if isinstance(from_square, str):
            from_pos = self.square_to_coords(from_square)
        else:
            from_pos = from_square
        
        if isinstance(to_square, str):
            to_pos = self.square_to_coords(to_square)
        else:
            to_pos = to_square
        
        if not from_pos or not to_pos:
            return False
        
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        moving_piece = self.board[from_row][from_col]
        if moving_piece == "  " or moving_piece[0] != self.current_turn:
            return False
        
        # Check if move is legal
        legal_moves = self.get_legal_moves_for_piece(from_pos)
        if to_pos not in legal_moves:
            return False
        
        # Save game state for undo
        game_state = {
            'board': [row[:] for row in self.board],
            'current_turn': self.current_turn,
            'castling_rights': self.castling_rights.copy(),
            'en_passant_target': self.en_passant_target,
            'halfmove_clock': self.halfmove_clock
        }
        self.move_history.append(game_state)
        
        # Handle en passant capture
        captured_piece = self.board[to_row][to_col]
        is_en_passant = False
        if moving_piece[1] == 'P' and captured_piece == "  " and from_col != to_col:
            if self.en_passant_target == (to_row, to_col):
                is_en_passant = True
                # Remove the captured pawn
                captured_row = to_row + 1 if self.current_turn == 'w' else to_row - 1
                self.board[captured_row][to_col] = "  "
                captured_piece = f"{'b' if self.current_turn == 'w' else 'w'}P"
        
        # Handle castling - move rook
        is_castling = False
        if moving_piece[1] == 'K' and abs(from_col - to_col) == 2:
            is_castling = True
            # Kingside castling
            if to_col > from_col:
                # Move rook from h-file to f-file
                self.board[to_row][5] = self.board[to_row][7]
                self.board[to_row][7] = "  "
            # Queenside castling
            else:
                # Move rook from a-file to d-file
                self.board[to_row][3] = self.board[to_row][0]
                self.board[to_row][0] = "  "
        
        # Move the piece
        self.board[to_row][to_col] = moving_piece
        self.board[from_row][from_col] = "  "
        
        # Handle pawn promotion
        if moving_piece[1] == 'P' and (to_row == 0 or to_row == 7):
            self.board[to_row][to_col] = f"{self.current_turn}{promotion_piece}"
        
        # Update castling rights
        if moving_piece[1] == 'K':
            self.castling_rights[f"{self.current_turn}K"] = False
            self.castling_rights[f"{self.current_turn}Q"] = False
        elif moving_piece[1] == 'R':
            # Lost castling right if rook moves from starting position
            if from_row == 7 and from_col == 0:  # White queenside rook
                self.castling_rights['wQ'] = False
            elif from_row == 7 and from_col == 7:  # White kingside rook
                self.castling_rights['wK'] = False
            elif from_row == 0 and from_col == 0:  # Black queenside rook
                self.castling_rights['bQ'] = False
            elif from_row == 0 and from_col == 7:  # Black kingside rook
                self.castling_rights['bK'] = False
        
        # Update en passant target
        self.en_passant_target = None
        if moving_piece[1] == 'P' and abs(from_row - to_row) == 2:
            # Pawn moved two squares, set en passant target
            en_passant_row = (from_row + to_row) // 2
            self.en_passant_target = (en_passant_row, from_col)
        
        # Update halfmove clock (for 50-move rule)
        if moving_piece[1] == 'P' or captured_piece != "  ":
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1
        
        # Update fullmove number after black's move
        if self.current_turn == 'b':
            self.fullmove_number += 1
        
        # Switch turns
        self.current_turn = 'b' if self.current_turn == 'w' else 'w'
        
        return True
    
    def undo_move(self):
        """Undo the last move"""
        if not self.move_history:
            return False
        
        game_state = self.move_history.pop()
        self.board = game_state['board']
        self.current_turn = game_state['current_turn']
        self.castling_rights = game_state['castling_rights']
        self.en_passant_target = game_state['en_passant_target']
        self.halfmove_clock = game_state['halfmove_clock']
        
        return True
    
    def is_check(self):
        """Check if current player's king is in check"""
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece == f"{self.current_turn}K":
                    king_pos = (row, col)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False
        
        opponent_color = 'b' if self.current_turn == 'w' else 'w'
        return self.is_square_attacked(king_pos, opponent_color)
    
    def is_checkmate(self):
        """Check if current player is in checkmate"""
        if not self.is_check():
            return False
        
        # If in check and no legal moves available, it's checkmate
        return len(self.get_all_legal_moves()) == 0
    
    def is_stalemate(self):
        """Check if current player is in stalemate"""
        if self.is_check():
            return False
        
        # If not in check but no legal moves available, it's stalemate
        return len(self.get_all_legal_moves()) == 0
    
    def is_insufficient_material(self):
        """Check if there's insufficient material to checkmate"""
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != "  ":
                    pieces.append(piece)
        
        # King vs king
        if len(pieces) == 2:
            return True
        
        # King and bishop vs king
        # King and knight vs king
        if len(pieces) == 3:
            for piece in pieces:
                if piece[1] in ['B', 'N']:
                    return True
        
        # Other cases with more pieces
        return False
    
    def is_game_over(self):
        """Check if game is over"""
        return self.is_checkmate() or self.is_stalemate() or self.is_insufficient_material()
    
    def get_game_result(self):
        """Get game result if game is over"""
        if self.is_checkmate():
            return "checkmate"
        elif self.is_stalemate():
            return "stalemate"
        elif self.is_insufficient_material():
            return "insufficient material"
        return None
    
    def get_fen(self):
        """Generate FEN notation for current position"""
        fen_parts = []
        
        # Board position
        for row in range(8):
            empty_count = 0
            row_str = ""
            for col in range(8):
                piece = self.board[row][col]
                if piece == "  ":
                    empty_count += 1
                else:
                    if empty_count > 0:
                        row_str += str(empty_count)
                        empty_count = 0
                    piece_char = piece[1] if piece[0] == 'w' else piece[1].lower()
                    row_str += piece_char
            if empty_count > 0:
                row_str += str(empty_count)
            fen_parts.append(row_str)
        
        board_fen = "/".join(fen_parts)
        
        # Current turn
        turn_fen = self.current_turn
        
        # Castling rights
        castling_fen = ""
        if self.castling_rights['wK']: castling_fen += 'K'
        if self.castling_rights['wQ']: castling_fen += 'Q'
        if self.castling_rights['bK']: castling_fen += 'k'
        if self.castling_rights['bQ']: castling_fen += 'q'
        if not castling_fen: castling_fen = '-'
        
        # En passant target
        en_passant_fen = self.coords_to_square(self.en_passant_target) if self.en_passant_target else '-'
        
        # Halfmove clock and fullmove number
        return f"{board_fen} {turn_fen} {castling_fen} {en_passant_fen} {self.halfmove_clock} {self.fullmove_number}"
    
    def print_board(self):
        """Print the board with coordinates"""
        print("\n   a  b  c  d  e  f  g  h")
        print("  " + "-" * 25)
        
        for i, row in enumerate(self.board):
            print(f"{8-i} |", end="")
            for piece in row:
                if piece == "  ":
                    print(" . ", end="")
                else:
                    # Use Unicode chess symbols or standard notation
                    symbols = {
                        'bK': '♔', 'bQ': '♕', 'bR': '♖', 'bB': '♗', 'bN': '♘', 'bP': '♙',
                        'wK': '♚', 'wQ': '♛', 'wR': '♜', 'wB': '♝', 'wN': '♞', 'wP': '♟'
                    }
                    if piece in symbols:
                        print(f" {symbols[piece]} ", end="")
                    else:
                        print(f" {piece} ", end="")
            print(f"| {8-i}")
        
        print("  " + "-" * 25)
        print("   a  b  c  d  e  f  g  h")
        
        # Print game status
        if self.is_checkmate():
            print(f"\nCheckmate! {'Black' if self.current_turn == 'w' else 'White'} wins!")
        elif self.is_stalemate():
            print("\nStalemate! Game is a draw.")
        elif self.is_check():
            print(f"\n{'White' if self.current_turn == 'w' else 'Black'} is in check!")
        
        print(f"\nTurn: {'White' if self.current_turn == 'w' else 'Black'}")
        print(f"FEN: {self.get_fen()[:50]}...")

    def print_debug_info(self):
        """Print debug info about board state"""
        print(f"\n=== DEBUG INFO ===")
        print(f"Current turn: {'White' if self.current_turn == 'w' else 'Black'}")
        print(f"FEN: {self.get_fen()}")
        
        # Count pieces
        white_pieces = []
        black_pieces = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != "  ":
                    if piece[0] == 'w':
                        white_pieces.append(piece)
                    else:
                        black_pieces.append(piece)
        
        print(f"White pieces: {len(white_pieces)}")
        print(f"Black pieces: {len(black_pieces)}")
        print(f"White legal moves: {len(self.get_all_legal_moves('w'))}")
        print(f"Black legal moves: {len(self.get_all_legal_moves('b'))}")
        print("=" * 20)
    
    def get_board_ascii(self):
        """Get ASCII representation of board"""
        result = "   a  b  c  d  e  f  g  h\n"
        result += "  " + "-" * 25 + "\n"
        
        for i, row in enumerate(self.board):
            result += f"{8-i} |"
            for piece in row:
                if piece == "  ":
                    result += " . "
                else:
                    # Use simpler representation
                    piece_map = {
                        'wK': 'K', 'wQ': 'Q', 'wR': 'R', 'wB': 'B', 'wN': 'N', 'wP': 'P',
                        'bK': 'k', 'bQ': 'q', 'bR': 'r', 'bB': 'b', 'bN': 'n', 'bP': 'p'
                    }
                    result += f" {piece_map.get(piece, piece)} "
            result += f"| {8-i}\n"
        
        result += "  " + "-" * 25 + "\n"
        result += "   a  b  c  d  e  f  g  h"
        return result

# Helper function for quick testing
def play_interactive_game():
    """Play an interactive chess game against yourself"""
    engine = ChessEngine()
    
    print("Chess Engine - Interactive Mode")
    print("Enter moves in format: e2 e4")
    print("Type 'undo' to undo last move, 'quit' to exit")
    print("For pawn promotion: e7 e8 Q (promote to queen)")
    
    while not engine.is_game_over():
        engine.print_board()
        print(f"\n{'White' if engine.current_turn == 'w' else 'Black'} to move")
        
        user_input = input("Enter move: ").strip()
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'undo':
            engine.undo_move()
            continue
        elif user_input.lower() == 'fen':
            print(f"FEN: {engine.get_fen()}")
            continue
        
        parts = user_input.split()
        if len(parts) < 2:
            print("Invalid input. Use format: e2 e4")
            continue
        
        from_sq, to_sq = parts[0], parts[1]
        promotion = parts[2] if len(parts) > 2 else 'Q'
        
        if engine.make_move(from_sq, to_sq, promotion):
            print(f"Move made: {from_sq} -> {to_sq}")
        else:
            print("Invalid move! Try again.")
    
    if engine.is_game_over():
        engine.print_board()
        result = engine.get_game_result()
        print(f"\nGame Over: {result}")

if __name__ == "__main__":
    # Quick test
    print("Testing Chess Engine...")
    engine = ChessEngine()
    engine.print_board()
    
    # Test a few moves
    print("\nMaking moves e2-e4, e7-e5...")
    engine.make_move("e2", "e4")
    engine.make_move("e7", "e5")
    engine.print_board()
    
    print("\nTesting legal moves for white knight:")
    moves = engine.get_legal_moves_for_piece(engine.square_to_coords("g1"))
    for move in moves:
        print(f"  Knight can move to: {engine.coords_to_square(move)}")
    
    print(f"\nIs white in check? {engine.is_check()}")
    print(f"Game over? {engine.is_game_over()}")