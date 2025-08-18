import grid, blocks
SIM_GRID = 0

def algo(_grid, _block):
    SIM_GRIDS_BLOCKS = {}    
    while True:
        SIM_GRID = _grid
        SIM_BLOCK = _block
        while True:
            if SIM_BLOCK.shape_coords not in SIM_GRIDS_BLOCKS.values():
                SIM_BLOCK.rotate()
            else:
                break