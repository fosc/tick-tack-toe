from enum import Enum
from copy import deepcopy
Square = Enum("Square", "Empty X O")


class Board:
    def __init__(self, size, def_val):
        self._board = [[def_val]*size for i in range(size)]
        self.size = size

    def get_square(self, coord):
        return self._board[coord[1]][coord[0]]

    def set_square(self, coord, mark):
        self._board[coord[1]][coord[0]] = mark


class GameBoard(Board):

    def __init__(self, size):
        super().__init__(size, Square.Empty)
        self._rows = [[(j, i) for j in range(size)] for i in range(size)]
        self._columns = [[(i, j) for j in range(size)] for i in range(size)]
        self._diagonal = [(i, i) for i in range(size)]
        self._off_diagonal = [(i, size - 1 - i) for i in range(size)]

    def __str__(self):
        def row_to_string(this_row):
            return ''.join([f"|{square_to_string[x]}" for x in this_row]) + '|\n'

        def get_squares(row):
            return list(map(self.get_square, row))

        square_to_string = {Square.Empty: " ", Square.O: "O", Square.X: "X"}
        rows = list(map(get_squares, self._rows))
        return ''.join(list(map(row_to_string, reversed(rows))))

    def get_empty_squares(self):
        def get_empty_squares(list_of_coords):
            return self.get_squares(list_of_coords)[Square.Empty]
        coords_of_empty = list(map(get_empty_squares, self._rows))
        return [item for sublist in coords_of_empty for item in sublist]

    def are_there_n_in_a_row(self, player):
        for row in [self._diagonal, self._off_diagonal] + self._rows + self._columns:
            if len(self.get_squares(row)[player]) == self.size:
                return True
        return False

    def find_winning_move(self, player):
        def check_list_of_squares(list_of_squares):
            squares = self.get_squares(list_of_squares)
            if len(squares[Square.Empty]) == 1 and len(squares[player]) == self.size - 1:
                return squares[Square.Empty][0]
            return None
        potential_wins = [check_list_of_squares(self._diagonal)]
        potential_wins += [check_list_of_squares(self._off_diagonal)]
        potential_wins += list(map(check_list_of_squares, self._rows))
        potential_wins += list(map(check_list_of_squares, self._columns))
        return [x for x in potential_wins if x is not None]

    def get_squares(self, list_of_coords):
        d = {x: self.get_square(x) for x in list_of_coords}
        d2 = {Square.X: [], Square.O: [], Square.Empty: []}
        for key, value in d.items():
            d2[value].append(key)
        return d2


class RuleManager:
    """RuleManager has a GameBoard. It handles interactions with that GameBoard."""
    def __init__(self, size):
        self.gameBoard = GameBoard(size)
        self.history = {Square.X: [], Square.O: []}

    def __add__(self, other):
        if type(other) is tuple:
            game_copy = deepcopy(self)
            game_copy.set(*other, self.next_player())
            return game_copy
        raise ValueError('Only Tuples can be added to this class with the + operator.')

    def get_moves(self):
        return self.gameBoard.get_empty_squares()

    def set(self, x, y, mark):
        """Write and X or and O on gameBord. Check to make sure its and empty square."""
        if self.gameBoard.get_square((x, y)) is not Square.Empty:
            raise ValueError(f'square {x} {y} is not empty. Cannot set to {mark}')
        self.gameBoard.set_square((x, y), mark)
        self.history[mark].append((x, y))

    def number_of_moves(self, player):
        """Return how many moves player has made"""
        return len(self.history[player])

    def next_player(self):
        """Return who goes next. Remember, X goes first"""
        x_count = self.number_of_moves(Square.X)
        o_count = self.number_of_moves(Square.O)
        return Square.X if x_count <= o_count else Square.O

    def is_winnable(self):
        """Return true if the active player can win."""
        return len(self.gameBoard.find_winning_move(self.next_player())) > 0

    def is_game_over(self):
        if self.gameBoard.are_there_n_in_a_row(Square.X):
            return True, Square.X
        if self.gameBoard.are_there_n_in_a_row(Square.O):
            return True, Square.O
        if len(self.gameBoard.get_empty_squares()) == 0:
            return True, None
        return False, None

    def __str__(self):
        return str(self.gameBoard)


class Game:
    """Orchestrate a game between team_x and team_o on board of size 'size'"""
    def __init__(self, team_x, team_o, size):
        self.game_manager = RuleManager(size)
        self.this_turn = Square.X
        self.team = {Square.X: team_x, Square.O: team_o}

    def do_turn(self):
        x, y = self.team[self.this_turn].play(self.game_manager)
        self.game_manager.set(x, y, self.this_turn)
        self.this_turn = Square.X if self.this_turn is Square.O else Square.O

    def is_win_or_tie(self):
        is_over, winner = self.game_manager.is_game_over()
        if is_over and winner is not None:
            print(self.game_manager)
            print(f"{winner} the winner")
            return True
        elif is_over:
            print(self.game_manager)
            print(f"Tie Game")
            return True
        return False

    def start_game(self):
        while not self.is_win_or_tie():
            self.do_turn()
