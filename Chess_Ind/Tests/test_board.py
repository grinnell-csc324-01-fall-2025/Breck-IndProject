# Tests/test_board.py
import pytest
from Game.chess_engine import ChessEngine

def test_board_creation():
    engine = ChessEngine()
    board = engine.board
    assert len(board) == 8
    assert len(board[0]) == 8
    # Check some starting positions
    assert board[0][0] == "bR"  # black rook at a8
    assert board[7][4] == "wK"  # white king at e1

def test_make_move():
    engine = ChessEngine()
    
    # Test pawn move e2 to e4
    # Before move: e2 should have wP, e4 should be empty
    assert engine.board[6][4] == "wP", "e2 should start with white pawn"
    assert engine.board[4][4] == "  ", "e4 should start empty"
    
    # Make the move
    success = engine.make_move("e2", "e4")
    assert success == True, "Move should be successful"
    
    # After move: e2 should be empty, e4 should have wP
    assert engine.board[6][4] == "  ", "e2 should be empty after move"
    assert engine.board[4][4] == "wP", "e4 should have pawn after move"

def test_turn_switching():
    engine = ChessEngine()
    assert engine.current_turn == 'w'  # White starts
    engine.make_move("e2", "e4")
    assert engine.current_turn == 'b'  # Should switch to black

def test_illegal_move():
    """Test that illegal moves are rejected"""
    engine = ChessEngine()
    
    # Try to move pawn 3 squares (illegal)
    success = engine.make_move("e2", "e5")
    assert success == False, "Moving pawn 3 squares should fail"
    
    # Try to move opponent's piece
    success = engine.make_move("e7", "e5")  # Black's turn to move
    assert success == False, "Should not be able to move opponent's piece on white's turn"
    
    # After white moves, black should be able to move
    engine.make_move("e2", "e4")  # White moves
    success = engine.make_move("e7", "e5")  # Black moves
    assert success == True, "Black should be able to move after white"

def test_coordinate_conversion():
    """Test that square_to_coords and coords_to_square work correctly"""
    engine = ChessEngine()
    
    # Test e2
    coords = engine.square_to_coords("e2")
    assert coords == (6, 4), f"e2 should be (6,4), got {coords}"
    
    # Convert back
    square = engine.coords_to_square((6, 4))
    assert square == "e2", f"(6,4) should be e2, got {square}"
    
    # Test e4
    coords = engine.square_to_coords("e4")
    assert coords == (4, 4), f"e4 should be (4,4), got {coords}"
    
    square = engine.coords_to_square((4, 4))
    assert square == "e4", f"(4,4) should be e4, got {square}"
