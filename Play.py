from tick_tack_toe import Game
from opponents import opponentFactory


def get_player_mark():
    XorO = input("Play as X or O?:").upper().strip()
    while XorO not in ['X', 'O']:
        print("invalid input. Please enter X or O")
        XorO = input("Play as X or O?:").upper().strip()
    return XorO


x_or_o = get_player_mark()

if x_or_o == 'X':
    team_x = opponentFactory.get_opponent('human')
    team_o = opponentFactory.get_opponent('hard')
else:
    team_x = opponentFactory.get_opponent('hard')
    team_o = opponentFactory.get_opponent('human')

game = Game(team_x, team_o, 3)
game.start_game()
