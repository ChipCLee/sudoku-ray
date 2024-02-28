from sudokux.solver.chip.chip_solver import *
import unittest

logger.setLevel(logging.INFO)
puzzle_str='070000043040009610800634900094052000358460020000800530080070091902100005007040802'
puzzle=getPuzzle(puzzle_str)
solution_str='679518243543729618821634957794352186358461729216897534485276391962183475137945862'
solution=getPuzzle(solution_str)

#row=Row(0,puzzle)
class TestSolver(unittest.TestCase):

    def test_Block(self):
        expected={'1','2','5','6','9','3'}
        block=Block(0,0,puzzle)
        keys=block.missings_map.keys()
        logger.debug("keys: {}".format(keys))
        # print("len: {}, result: {}".format(len(result),result))
        self.assertTrue(keys,expected)
    def test_Row(self):
        expected={'1','2','5','6','9','3'}
        row=Row(0,puzzle)
        keys=row.missings_map.keys()
        logger.debug("keys: {}".format(keys))
        # print("len: {}, result: {}".format(len(result),result))
        self.assertTrue(keys,expected)
    def test_Col(self):
        expected={'1','2','3','6'}
        col=Col(1,puzzle)
        keys=col.missings_map.keys()
        logger.debug("keys: {}".format(keys))
        # print("len: {}, result: {}".format(len(result),result))
        self.assertTrue(keys,expected)

