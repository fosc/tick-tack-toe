"""Demo of the tick_tack_toe and opponents modules"""
from tick_tack_toe import Game
from opponents import opponent_factory


def get_player_mark():
    """Return string 'X' or 'O' based on input."""
    x_or_o = input("Play as X or O?:").upper().strip()
    while x_or_o not in ['X', 'O']:
        print("invalid input. Please enter X or O")
        x_or_o = input("Play as X or O?:").upper().strip()
    return x_or_o


X_OR_O = get_player_mark()
HUMAN = opponent_factory.get_opponent('human')
HARD_AI = opponent_factory.get_opponent('hard')

GAME = Game(HUMAN if X_OR_O == 'X' else HARD_AI, HARD_AI if X_OR_O == 'X' else HUMAN, 3)
GAME.start_game()
