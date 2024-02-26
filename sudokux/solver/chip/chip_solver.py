from .utils import *
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


class Row:
    def __init__(self, r, np_cells) -> None:
        self.row_index=r
        self.row=getRow(r,np_cells)
        logger.debug(self.row)
        self.np_cells=np_cells

        self.missings_map=self.getMissingsMap()
        
        logger.debug(self.missings_map)

    def getMissingValeusAndUnknownCells(self):
        missing_values={i for i in "123456789"}
        unknown_cells=[]
        for j in range(9):
            v=self.row[j]
            if v=='0':
                unknown_cells.append((self.row_index,j))
            else:
                missing_values.remove(v)
        logger.debug("unknown_cells: {}".format(unknown_cells) )
        logger.debug("missing_values:".format(missing_values))
        return (missing_values, unknown_cells)

    def getMissingsMap(self):
        missing_values, unknown_cells = self.getMissingValeusAndUnknownCells()
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
        row_index, col_index = cell[0],cell[1]

        blockList=getBlockListByCell(row_index, col_index, self.np_cells)
       
        col=getCol(col_index, self.np_cells)
       
        result =True
        if key in blockList:
            logger.debug("found {} in {}".format(key, blockList))
            result=False
        else:
            logger.debug("No {} in block {}: {}".format(key, row_index, blockList))
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
                    self.np_cells[px, py]=key
                    removes.append((px,py))
                    changed=True
                    repeat=False
            self.removepos(removes)
        
        return changed
    
def calculate_Rows(np_cells):
    changed=False
    for row_index in range(3):
        logger.debug("solving row {}".format(row_index) )
        r=Row(row_index, np_cells)
        if r.calculate():
            changed=True
    return changed


class Col:
    def __init__(self, c, np_cells) -> None:
        self.col_index=c
        self.col=getCol(c,np_cells)
        logger.debug(self.col)
        self.np_cells=np_cells

        self.missings_map=self.getMissingsMap()
        
        logger.debug(self.missings_map)

    def getMissingValeusAndUnknownCells(self):
        missing_values={i for i in "123456789"}
        unknown_cells=[]
        for j in range(9):
            v=self.col[j]
            if v=='0':
                unknown_cells.append((self.col_index,j))
            else:
                missing_values.remove(v)
        logger.debug("unknown_cells: {}".format(unknown_cells) )
        logger.debug("missing_values:".format(missing_values))
        return (missing_values, unknown_cells)

    def getMissingsMap(self):
        missing_values, unknown_cells = self.getMissingValeusAndUnknownCells()
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
        row_index, col_index = cell[0],cell[1]

        blockList=getBlockListByCell(row_index, col_index, self.np_cells)
       
        row=getRow(col_index, self.np_cells)
       
        result =True
        if key in blockList:
            logger.debug("found {} in {}".format(key, blockList))
            result=False
        else:
            logger.debug("No {} in block {}: {}".format(key, row_index, blockList))
        if key in row:
            logger.debug("found {} in {}".format(key, row))
            result=False
        else:
            logger.debug("No {} in col {}: {}".format(key,col_index, row))
       
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
                    self.np_cells[px, py]=key
                    removes.append((px,py))
                    changed=True
                    repeat=False
            self.removepos(removes)
        
        return changed
    
def calculate_Cols(np_cells):
    changed=False
    for col_index in range(3):
        logger.debug("solving col {}".format(col_index) )
        r=Row(col_index, np_cells)
        if r.calculate():
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
                logger.debug("Block changed")
                changed=True
            if calculate_Rows(np_cells):
                logger.debug("Row changed")
                if not changed:
                    changed=True
            if calculate_Cols(np_cells):
                logger.debug("Col changed")
                if not changed:
                    changed=True
        
        if not solved:
            solved=isSolved(np_cells)

    logger.debug(np_cells)
    return solved