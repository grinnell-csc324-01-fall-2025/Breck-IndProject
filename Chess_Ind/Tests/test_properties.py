from hypothesis import given, strategies as st, settings
from Chess_Ind.Game.chess_engine import ChessEngine

@given(
    st.integers(min_value=0, max_value=7),
    st.integers(min_value=0, max_value=7)
)
@settings(max_examples=50)
def test_board_coordinates_always_valid(x, y):
    """Property: All board coordinates should contain valid pieces"""
    engine = ChessEngine()
    piece = engine.board[x][y]
    # Piece should be either empty or a valid piece
    if piece != "  ":
        assert piece[0] in ['w', 'b']
        assert piece[1] in ['P', 'N', 'B', 'R', 'Q', 'K']

def test_move_makes_board_change():
    """Property: Making a move changes the board state"""
    engine = ChessEngine()
    initial_state = str(engine.board)
    engine.make_move("e2", "e4")
    new_state = str(engine.board)
    assert initial_state != new_state