import pandas as pd
import numpy as np
import logging as logging
logger=logging.getLogger("utils")
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

def getBlockListByCell(cell_row, cell_col, np_cells):
    block_row, block_col = getBlockIndex(cell_row, cell_col)
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