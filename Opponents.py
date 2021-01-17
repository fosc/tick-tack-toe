from TickTackToe import Square


class OpponentFactory:

    def __init__(self):
        self._creators = {}

    def register_opponent(self, level, size, creator):
        self._creators[(level, size)] = creator

    def get_opponent(self, level, size):
        creator = self._creators.get((level, size))
        if not creator:
            raise ValueError((level, size))
        return creator()


class HumanPlayer:
    def play(self, game):
        print(game)
        print("top left is 0,0")
        x = int(input("enter x:"))
        y = int(input("enter y:"))
        return x, y

class MediumOpponent:
    def play(self, game):
        move_for = game.next_player()
        other_player = Square.X if move_for == Square.O else Square.O

        wins_for_this_player = game.gameBoard.find_winning_move(move_for)
        if len(wins_for_this_player) > 0:
            return wins_for_this_player[0]

        wins_for_other_player = game.gameBoard.find_winning_move(other_player)
        if len(wins_for_other_player) > 0:
            return wins_for_other_player[0]

        return game.gameBoard.get_empty_squares()[0]


class HardOpponentSize3:
    board_size = 3
    OPENING_BOOK = {
        'player_x': {
            'first_move': lambda: (0, 0),
            'second_move': lambda x: {
                (0, 1): (1, 0),
                (0, 2): (1, 0),
                (1, 1): (1, 0),
                (1, 0): (0, 1),
                (2, 0): (0, 1),
                (1, 2): (2, 0),
                (2, 2): (2, 0),
                (2, 1): (1, 1)
                            }[x]
        },
        'player_o': {
            'first_move': lambda x: (0, 0) if x == (1, 1) else (1, 1)
        }
    }

    def play(self, game):
        move_for = game.next_player()
        other_player = Square.X if move_for == Square.O else Square.O
        move_number = game.number_of_moves(move_for)
        if move_for is Square.O:
            if move_number == 0:
                first_x = game.history[Square.X][0]
                return self.OPENING_BOOK['player_o']['first_move'](first_x)

        if move_for is Square.X:
            if move_number == 0:
                return self.OPENING_BOOK['player_x']['first_move']()
            if move_number == 1:
                first_o = game.history[Square.O][0]
                return self.OPENING_BOOK['player_x']['second_move'](first_o)

        wins_for_this_player = game.gameBoard.find_winning_move(move_for)
        if len(wins_for_this_player) > 0:
            return wins_for_this_player[0]

        wins_for_other_player = game.gameBoard.find_winning_move(other_player)
        if len(wins_for_other_player) > 0:
            return wins_for_other_player[0]

        return game.gameBoard.get_empty_squares()[0]


opponentFactory = OpponentFactory()
opponentFactory.register_opponent('hard', 3, HardOpponentSize3)
opponentFactory.register_opponent('medium', 3, MediumOpponent)
opponentFactory.register_opponent('medium', 4, MediumOpponent)
opponentFactory.register_opponent('human', None, HumanPlayer)
