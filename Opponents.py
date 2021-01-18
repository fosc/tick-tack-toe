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


class RecursiveSearchAlgorithm:
    max_search_depth = 5

    def __init__(self):
        self.current_depth = 0

    def search_depth_exceeded(self):
        return self.current_depth >= self.max_search_depth

    def max_depth(func):
        def wrapper(self, *args, **kwargs):
            self.current_depth += 1
            res = func(self, *args, **kwargs)
            self.current_depth -= 1
            return res

        return wrapper

    @max_depth
    def is_good_move(self, game):
        if game.is_game_over()[0]:
            print("win found")
            return True  # you cannot loose on your turn - only win or draw
        if self.search_depth_exceeded():
            print("Depth exceeded")
            return True  # eventually we stop looking and say its safe
        if game.is_winnable():
            print("opponent win found")
            return False  # it we have left game in a state were opponent can win
        can_be_won = True  # we can win (or draw) unless we find opponent has winning move
        for opponent_move in game.get_moves():
            new_game = game + opponent_move
            # can_win_after_this_move is False until we find a good move (or if there are no moves --> draw)
            can_win_after_this_move = True if not new_game.get_moves() else False
            for move in new_game.get_moves():
                can_win_after_this_move = can_win_after_this_move or self.is_good_move(new_game + move)
            can_be_won = can_be_won and can_win_after_this_move  # we need to be able to win after all opponent moves
        return can_be_won

    def play(self, game):
        possible_moves = game.get_moves()
        move_dict = {}
        for move in possible_moves:
            move_dict[move] = self.is_good_move(game + move)
            print(move_dict)
            if move_dict[move]:
                return move
        print(move_dict)
        print("could not find a good move")
        return possible_moves[0]


class HumanPlayer:
    @staticmethod
    def play(game):
        print(game)
        x = int(input("enter x:"))
        y = int(input("enter y:"))
        return x, y


class MediumOpponent:
    @staticmethod
    def play(game):
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
opponentFactory.register_opponent('hard', None, RecursiveSearchAlgorithm)