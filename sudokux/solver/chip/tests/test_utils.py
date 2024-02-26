from ..utils import *
import unittest

logger.setLevel(logging.INFO)
puzzle_str='070000043040009610800634900094052000358460020000800530080070091902100005007040802'
puzzle=getPuzzle(puzzle_str)
solution_str='679518243543729618821634957794352186358461729216897534485276391962183475137945862'
solution=getPuzzle(solution_str)

class TestNotebook(unittest.TestCase):

    def test_getPuzzle(self):
        expected=np.array(
        [['0', '7', '0', '0', '0', '0', '0', '4', '3'],
        ['0', '4', '0', '0', '0', '9', '6', '1', '0'],
        ['8', '0', '0', '6', '3', '4', '9', '0', '0'],
        ['0', '9', '4', '0', '5', '2', '0', '0', '0'],
        ['3', '5', '8', '4', '6', '0', '0', '2', '0'],
        ['0', '0', '0', '8', '0', '0', '5', '3', '0'],
        ['0', '8', '0', '0', '7', '0', '0', '9', '1'],
        ['9', '0', '2', '1', '0', '0', '0', '0', '5'],
        ['0', '0', '7', '0', '4', '0', '8', '0', '2']])
        
        self.assertTrue(np.array_equal(puzzle,expected))

    def test_solved(self):
        self.assertEqual(isSolved(puzzle),False)

    def test_unsolved(self):
        self.assertEqual(isSolved(solution),True)

    def test_getBlockIndex(self):
        self.assertEqual(getBlockIndex(8,8),(2,2))

    def test_getBlock(self):
        expected=np.array(
            [['0','0','0'],
            ['0','2','0'],
            ['5','3','0']])
        result=getBlock(1,2,puzzle)
        self.assertTrue(np.array_equal(result,expected))

    def test_getBlockList(self):
        expected=np.array(['0','0','0','0','2','0','5','3','0'])
        result=getBlockList(1,2,puzzle)
        self.assertTrue(np.array_equal(result,expected))

    def test_getRow(self):
        expected=np.array(['0', '4', '0', '0', '0', '9', '6', '1', '0'])
        result=getRow(1,puzzle)
        self.assertTrue(np.array_equal(result,expected))

    def test_getCol(self):
        expected=np.array(['0','0','0','4','8','0','0','2','7'])
        
        result=getCol(2,puzzle)
        logger.debug(result)
        self.assertTrue(np.array_equal(result,expected))

    def test_getCol(self):
        expected=np.array(['0','0','0','4','8','0','0','2','7'])
        
        result=getCol(2,puzzle)
        logger.debug(result)
        self.assertTrue(np.array_equal(result,expected))

    def test_calculate_possibilitie(self):
        expected={'1','2','5','6'}
        
        result=calculate_possibilitie(0,0,puzzle)
        logger.debug(result)
        self.assertTrue(np.array_equal(result[2],expected))
    