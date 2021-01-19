"""
This module contains implementations of the Player interface. A Player provides the play method:
1. play(Game State) --> tuple

The Game State interface provides the following methods:
1. is_game_over() --> Boolean
2. get_moves() --> list of tuples
3. is_winnable() --> Boolean
4. + tuple --> new Game State

"""


class PlayerFactory:
    """Factory of the Player interface"""
    def __init__(self):
        self._creators = {}

    def register_opponent(self, level, creator):
        """Register a class with method play() and assign it a difficulty 'level'"""
        self._creators[level] = creator

    def get_opponent(self, level):
        """Get an opponent instance that plays with difficulty 'level'"""
        creator = self._creators.get(level)
        if not creator:
            raise ValueError(level)
        return creator()


def max_depth(my_func):
    """Track recursion depth for a class method based on the current_depth member"""
    def wrapper(self, *args, **kwargs):
        self.current_depth += 1
        res = my_func(self, *args, **kwargs)
        self.current_depth -= 1
        return res
    return wrapper


class RecursiveSearchAlgorithm:
    """Recursively traverses a tree of possible game outcomes and return next move."""
    def __init__(self, max_search_depth):
        self.current_depth = 0
        self.max_search_depth = max_search_depth

    def search_depth_exceeded(self):
        return self.current_depth >= self.max_search_depth

    @max_depth
    def is_good_move(self, game):
        """Draws and Wins are both considered equally good by this method"""
        if game.is_game_over():
            return True  # you cannot loose on your turn - only win or draw
        if self.search_depth_exceeded():
            return True  # eventually we stop looking and say its safe
        if game.is_winnable():
            return False  # it we have left game in a state were opponent can win
        can_be_won = True  # we can win (or draw) unless we find opponent has winning move
        for opponent_move in game.get_moves():
            new_game = game + opponent_move
            # can_win_after_this_move is False until we find a good move
            # (or if there are no moves --> draw)
            can_win_after_this_move = True if not new_game.get_moves() else False
            for move in new_game.get_moves():
                can_win_after_this_move = \
                    can_win_after_this_move or self.is_good_move(new_game + move)
            # we need to be able to win after all opponent moves
            can_be_won = can_be_won and can_win_after_this_move
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


def string_to_tuple(my_str):
    just_numbers = ''.join(c for c in my_str if c.isdigit())
    tuple_of_strings = tuple(just_numbers)
    return int(tuple_of_strings[0]), int(tuple_of_strings[1])


class HumanPlayer:
    @staticmethod
    def get_coordinate(message):
        return string_to_tuple(input(message))

    def play(self, game):
        print(game)
        ask = "enter the coordinates of your move (e.g. enter: 1,2 ):\n(Please note bottom left is 0,0)\n"
        return HumanPlayer.get_coordinate(ask)


class MediumOpponent(RecursiveSearchAlgorithm):
    def __init__(self):
        super().__init__(2)


class HardOpponent(RecursiveSearchAlgorithm):
    def __init__(self):
        super().__init__(5)


opponent_factory = PlayerFactory()
opponent_factory.register_opponent('medium', MediumOpponent)
opponent_factory.register_opponent('human', HumanPlayer)
opponent_factory.register_opponent('hard', HardOpponent)
