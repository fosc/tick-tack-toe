import unittest
from TickTackToe import GameBoard, Square, RuleManager
from Opponents import RecursiveSearchAlgorithm


class TestBoard(unittest.TestCase):

    def setUp(self) -> None:
        self.board1 = GameBoard(3)
        self.board1.set_square(1, 1, Square.X)
        self.board1.set_square(2, 2, Square.X)
        self.board1.set_square(0, 2, Square.O)
        self.board1.set_square(0, 1, Square.O)

        self.board2 = GameBoard(3)
        self.board2.set_square(0, 2, Square.X)
        self.board2.set_square(1, 1, Square.X)
        self.board2.set_square(0, 0, Square.O)
        self.board2.set_square(1, 0, Square.O)

        self.board3 = GameBoard(3)
        self.board3.set_square(0, 0, Square.X)
        self.board3.set_square(2, 2, Square.X)
        self.board3.set_square(0, 2, Square.X)
        self.board3.set_square(2, 0, Square.X)

    def test_find_winning_move_board1(self):
        X_win = self.board1.find_winning_move(Square.X)
        O_win = self.board1.find_winning_move(Square.O)
        self.assertEqual([(0, 0)], X_win)
        self.assertEqual([(0, 0)], O_win)

    def test_find_winning_move_board2(self):
        X_win = self.board2.find_winning_move(Square.X)
        O_win = self.board2.find_winning_move(Square.O)
        self.assertEqual([(2, 0)], X_win)
        self.assertEqual([(2, 0)], O_win)

    def test_find_winning_move_board3(self):
        X_win = self.board3.find_winning_move(Square.X)
        self.assertEqual([(1, 1), (1, 1), (1, 0), (1, 2), (0, 1), (2, 1)], X_win)

    def test_string_rep_board1(self):
        board_str = '|O| |X|\n|O|X| |\n| | | |\n'
        self.assertEqual(board_str, str(self.board1))

    def test_get_empty_squares1(self):
        self.assertEqual([(0, 0), (1, 0), (2, 0), (2, 1), (1, 2)], self.board1.get_empty_squares())

    def test_get_empty_squares2(self):
        self.board2.set_square(2, 0, Square.X)
        self.board2.set_square(0, 1, Square.O)
        self.board2.set_square(2, 1, Square.O)
        self.assertEqual([(1,2), (2,2)], self.board2.get_empty_squares())

    def test_get_empty_squares3(self):
        self.assertEqual([(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)], self.board3.get_empty_squares())


class TestRuleManager(unittest.TestCase):

    def setUp(self) -> None:
        self.manager1 = RuleManager(3)
        self.manager1.set(1, 1, Square.X)
        self.manager1.set(2, 2, Square.X)
        self.manager1.set(0, 2, Square.O)
        self.manager1.set(0, 1, Square.O)

    def test_next_player_X(self):
        self.assertEqual(Square.X, self.manager1.next_player())

    def test_next_player_O(self):
        self.manager1.set(2, 0, Square.X)
        self.assertEqual(Square.O, self.manager1.next_player())


class TestRecursiveSearchAlgorithm(unittest.TestCase):

    def setUp(self):
        self.winnable_game = RuleManager(3)
        self.winnable_game.set(0, 0, Square.X)
        self.winnable_game.set(1, 0, Square.O)
        self.winnable_game.set(1, 1, Square.O)
        self.winnable_game.set(0, 1, Square.X)
        self.game = RuleManager(3)
        self.game.set(0, 0, Square.X)
        self.game.set(2, 2, Square.X)
        self.game.set(1, 1, Square.O)
        self.game.set(2, 0, Square.O)
        self.game.set(2, 1, Square.X)
        self.game.set(0, 1, Square.O)
        self.game2 = RuleManager(3)
        self.game2.set(0, 0, Square.X)

    def test_for_winning_move(self):
        x, y = RecursiveSearchAlgorithm().play(self.winnable_game)
        self.assertEqual((0, 2), (x, y))

    def test_for_defensive_move(self):
        print(self.game)
        x, y = RecursiveSearchAlgorithm().play(self.game)
        self.assertEqual((0, 2), (x, y))

    def test_3(self):
        print(self.game2)
        x, y = RecursiveSearchAlgorithm().play(self.game2)
        self.assertEqual((1, 1), (x, y))

if __name__ == '__main__':
    unittest.main()