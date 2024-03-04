import ray
from sudokux.solver.utils import *

@ray.remote
class SudokuWorker:

    def __init__(self, solver, puller) -> None:
        self.solver = solver
        self.poller=puller
        self.run=False
        self.success=0
        self.failure=0
    

    def solve(self, sudoku_str):
        puzzle= getPuzzle(sudoku_str)
        self.solver.init(puzzle)
        result= self.solver.solve()
        return (result, self.solver.grid)

    def start(self):
        self.run=True
        while self.run:
            puzzleStr= self.puller.pull()
            if puzzleStr!="":
                self.solver.init(puzzleStr)
                results= ray.get(self.solve.remote(puzzleStr))
                if results.result:
                    self.success+=1
                else:
                    self.failure+=1
            else:
                self.run=False
                break

    def stop(self):
        self.run=False