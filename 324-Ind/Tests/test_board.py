# tests/test_board.py
import pytest
from 324-Ind.Game.chess_engine import ChessEngine

def test_board_creation():
    engine = ChessEngine()
    board = engine.board
    assert len(board) == 8
    assert len(board[0]) == 8
    # Check some starting positions
    assert board[0][0] == "bR"  # black rook
    assert board[7][4] == "wK"  # white king

def test_make_move():
    engine = ChessEngine()
    # Test pawn move
    engine.make_move("e2", "e4")
    assert engine.board[4][4] == "  "  # e4 should be empty? Wait, check indices
    # Actually e2 is (6,4) and e4 is (4,4) in your system
    assert engine.board[6][4] == "  "  # e2 empty
    assert engine.board[4][4] == "wP"  # e4 has pawn

def test_turn_switching():
    engine = ChessEngine()
    assert engine.current_turn == 'w'
    engine.make_move("e2", "e4")

    assert engine.current_turn == 'b'
