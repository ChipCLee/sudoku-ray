# %load sudoku.py
import pandas as pd
import numpy as np
def getPuzzle(puzale_str):
    return np.array(list(puzale_str)).reshape(9,9)

def isSolved(np_cells):
    list=np_cells.reshape(81)
    logger.debug(list)
    return not ('0' in list)

def map2orginal(row, col, block_row, block_col):
    return (block_row*3 +row, block_col*3 + col)

def getBlockIndex(row_index, col_index):
    r= row_index//3
    c = col_index//3
    return (r,c)

def getBlock(block_row, block_col, np_cells):
    return np_cells[block_row*3:block_row*3+3, block_col*3:block_col*3+3]

def getBlockList(block_row, block_col, np_cells):
    return getBlock(block_row, block_col, np_cells).reshape(9)

def getRow(row, np_cells):
    return np_cells[row]

def getCol(col, np_cells):
    return np_cells[:, col]

def calculate_possibilitie(row_index, col_index, np_cells):
    row=getRow(row_index, np_cells)
    col=getCol(col_index, np_cells)
    block_row, block_col = getBlockIndex(row_index, col_index)
    block=getBlockList(block_row, block_col, np_cells)
    possibilities={i for i in "123456789"}
    for i in row:
        if i in possibilities:
            possibilities.remove(i)
    for j in col:
        if j in possibilities:
            possibilities.remove(j)
    for k in block:
        if k in possibilities:
            possibilities.remove(k)
    return (row_index, col_index, possibilities)

def calculate_cells(np_cells):
    solved=True
    changed=True
    results=[]
    iterations=0
    logger.debug(np_cells)
    while changed:
        iterations+=1
        changed=False
        results=[]
        for i in range(9):
            for j in range(9):
                if np_cells[i,j] == '0' :
                    results.append(calculate_possibilitie(i,j,np_cells))
                    solved=False


        for x,y,s in results:
            if len(s)==1:
                np_cells[x,y]=next(iter(s))
                changed=True
        
        logger.debug("results: {}".format(results))
        logger.debug("iterations: {}".format(iterations) )
        logger.debug("change: {}".format(changed) )

    logger.debug(np_cells)
    return solved

def addCellToMissingsMap(key, cell, missings_map):
    if key in missings_map.keys():
        missings_map[key].append(cell)
    else:
        missings_map[key]=[cell]

def getMissingValeusAndUnknownCells(block):
    missing_values={i for i in "123456789"}
    unknown_cells=[]
    for i in range(3):
        for j in range(3):
            v=block[i,j]
            if v=='0':
                unknown_cells.append((i,j))
            else:
                missing_values.remove(v)
    logger.debug("unknown_cells: {}".format(unknown_cells) )
    logger.debug("missing_values".format(missing_values))
    return (missing_values, unknown_cells)

class Block:
    def __init__(self, r, c, np_cells) -> None:
        self.block=getBlock(r,c,np_cells)
        logger.debug(self.block)
        self.block_row, self.block_col=(r,c)
        self.np_cells=np_cells

        self.missings_map=self.getMissingsMap()
        
        logger.debug(self.missings_map)

    def getMissingsMap(self):
        missing_values, unknown_cells = getMissingValeusAndUnknownCells(self.block)
        logger.debug("missing_values: {}, unknown_cells: {}".format(missing_values, unknown_cells))
        
        missings_map={}

        for key in missing_values:
            for cell in unknown_cells:
                logger.debug("key {}, cell: {}".format(key, cell))
                if self.couldfit(key, cell):
                    logger.debug("add {} to {}".format(cell, key))
                    addCellToMissingsMap(key, cell, missings_map)
                else:
                    logger.debug("could not add {} to {}".format(cell, key))
        return missings_map


    def couldfit(self, key, cell):
        row_index, col_index = map2orginal(cell[0], cell[1],self.block_row, self.block_col)

        row=getRow(row_index, self.np_cells)
       
        col=getCol(col_index, self.np_cells)
       
        result =True
        if key in row:
            logger.debug("found {} in {}".format(key, row))
            result=False
        else:
            logger.debug("No {} in row {}: {}".format(key, row_index, row))
        if key in col:
            logger.debug("found {} in {}".format(key, col))
            result=False
        else:
            logger.debug("No {} in col {}: {}".format(key,col_index, col))
       
        return result

    # def addpos(self, m, u):
    #     if m in self.missings.keys():
    #         poss=self.missings[m]
    #         poss.append(u)
    #     else:
    #         poss=[u]
    #         self.missings[m]=poss

    def removepos(self,removes):
        deleted=[]
        for r in removes:
            for key in self.missings_map.keys():
                if r in self.missings_map[key]:
                    self.missings_map[key].remove(r)
                    if len(self.missings_map[key])==0:
                        deleted.append(key)
                    
        for d in deleted:
            self.missings_map.pop(d)


    def calculate(self):
        removes=[]
        changed=False
        repeat=True
        while repeat:
            repeat=False
            for key in self.missings_map.keys():
                if len(self.missings_map[key]) == 1:
                    px, py=self.missings_map[key][0]
                    logger.debug("Solved {} at {}".format(key,self.missings_map[key][0]))
                    self.block[px, py]=key
                    removes.append((px,py))
                    logger.debug(self.block)
                    changed=True
                    repeat=False
            self.removepos(removes)
        
        return changed
    
def calculate_blocks(np_cells):
    changed=False
    for block_row in range(3):
        for block_col in range(3):
            logger.debug("solving {},{}".format(block_row, block_col) )
            b=Block(block_row, block_col, np_cells)
            if b.calculate():
                changed=True
    return changed

def single_solve(np_cells):
    changed=True
    solved=False
    while changed:
        changed=False
        if calculate_cells(np_cells):
            solved=True
        else:
            if calculate_blocks(np_cells):
                changed=True
        if not solved:
            solved=isSolved(np_cells)

    logger.debug(np_cells)
    return solved

logger.debug('info')
