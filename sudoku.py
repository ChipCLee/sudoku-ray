# %load sudoku.py
def isSolved(np_cells):
    list=np_cells.reshape(81)
    print(list)
    return not ('0' in list)

def map2orginal(row, col, block_row, block_col):
    return (block_row*3 +row, block_col*3 + col)

def getBlockIndex(row_index, col_index):
    r= row_index//3
    c = col_index//3
    return (r,c)

# def getBlock(row, col, np_cells):
#     r, c = getBlockIndex(row,col)
#     return np_cells[r*3:r*3+3, c*3:c*3+3]

def getBlock(block_row, block_col, np_cells):
    return np_cells[block_row*3:block_row*3+3, block_col*3:block_col*3+3]

def getBlockList(block_row, block_col, np_cells):
    return getBlock(block_row, block_col, np_cells).reshape(9)

def getRow(row, np_cells):
    return np_cells[row]

def getCol(col, np_cells):
    return np_cells[:, col]

def calculate(row_index, col_index, np_cells):
    row_index=row_index
    col_index=col_index
    row=getRow(row_index, np_cells)
    col=getCol(col_index, np_cells)
    block_row, block_col = getBlockIndex(row_index, col_index)
    block=getBlockList(block_row, block_col, np_cells)
    possibilities={i+1 for i in range(9)}
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
    logger.info(np_cells)
    while changed:
        iterations+=1
        changed=False
        results=[]
        for i in range(9):
            for j in range(9):
                if np_cells[i,j] == '0' :
                    results.append(calculate(i,j,np_cells))
                    solved=False


        for x,y,s in results:
            if len(s)==1:
                np_cells[x,y]=next(iter(s))
                changed=True
        
        logger.debug("results: {}".format(results))
        logger.debug("iterations: {}".format(iterations) )
        logger.debug("change: {}".format(changed) )

    logger.info(np_cells)
    return solved

logger.debug('info')
print(isSolved(np_solution))
print(isSolved(np_cells))