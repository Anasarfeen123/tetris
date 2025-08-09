import pygame
class Grid():
    def __init__(self, row_columns =(20,20),screen=None, block_size=30) -> None: 
        # Initialize grid dimensions, screen, block size, and other attributes
        (self.width, self.height) = pygame.display.get_window_size()
        self.BLOCK = block_size
        self.GRIDCOLOR = (200, 200, 200)
        self.rows = row_columns[0]
        self.columns = row_columns[1]
        self.grid_width = self.columns * self.BLOCK
        self.grid_height = self.rows * self.BLOCK
        self.offset_x = (self.width - self.grid_width) // 2
        self.offset_y = (self.height - self.grid_height) // 2
        self.screen = screen
        self.score = 0
        self.locked_cells = {}
    
    def draw_grid(self):
        # Draw horizontal and vertical grid lines
        for i in range(self.rows + 1):
            y = i * self.BLOCK + self.offset_y
            pygame.draw.line(self.screen, self.GRIDCOLOR, (self.offset_x, y), (self.offset_x + self.grid_width, y)) #type: ignore
        for i in range(self.columns + 1):
            x = i * self.BLOCK + self.offset_x
            pygame.draw.line(self.screen, self.GRIDCOLOR, (x, self.offset_y), (x, self.offset_y + self.grid_height)) #type: ignore

    def to_pixel(self, grid):
        # Convert grid coordinates to pixel coordinates
        x = self.offset_x + grid[0] * self.BLOCK
        y = self.offset_y + grid[1] * self.BLOCK
        return (x, y)

    def draw_cell(self, grid, color, br = 0):
        # Draw a single cell at the specified grid position
        x, y = self.to_pixel(grid)
        pygame.draw.rect(self.screen, color, (x, y, self.BLOCK, self.BLOCK), border_radius = br) #type: ignore
    
    def draw_cells(self, grids, color, br = 0):
        # Draw multiple cells at the specified grid positions
        for i in grids:
            x, y = self.to_pixel(i)
            pygame.draw.rect(self.screen, color, (x, y, self.BLOCK, self.BLOCK), border_radius = br) #type: ignore

    def get_neighbor_pos(self, pos:tuple):
        # Get neighboring positions of a given grid cell
        neighbors = []
        if pos[0] < self.columns - 1:
            neighbors.append((pos[0] + 1, pos[1]))
        if pos[0] > 0:
            neighbors.append((pos[0] - 1, pos[1]))
        if pos[1] < self.rows - 1:
            neighbors.append((pos[0], pos[1] + 1))
        if pos[1] > 0:
            neighbors.append((pos[0], pos[1] - 1))
        return neighbors

    def draw_path(self, path, color=(89, 102, 95), border_radius=4):
        # Draw a path of cells with the specified color and border radius
        for pos in path:
            self.draw_cell(pos, color, br=border_radius)
        
    def lock_cells(self, cells, color, shapeid):
        # Lock specified cells with a given color
        for cell in cells:
            self.locked_cells[tuple(cell)] = {'color':color, 'shape-id': shapeid}
    
    def draw_locked(self):
        # Draw all locked cells
        for i,j in self.locked_cells.items():
            self.draw_cell(i,j['color'])
    
    def delete_cell(self, grid, color = (0, 0, 40), br=0):
        # Delete a single cell by drawing over it with the background color
        x, y = self.to_pixel(grid)
        pygame.draw.rect(self.screen, color, (x, y, self.BLOCK, self.BLOCK), border_radius = br) #type: ignore
    
    def clear_line(self, debug=True):
        if debug:
            print("Before:", sorted(self.locked_cells.keys(), key=lambda x: x[1]))

        row_count = {}
        for x, y in self.locked_cells:
            row_count[y] = row_count.get(y, 0) + 1

        full_rows = [y for y, count in row_count.items() if count == self.columns]

        if not full_rows:
            return False # nothing to clear

        self.score += 10*len(full_rows)
        
        # ✅ STEP: Delete the full rows
        for y in full_rows:
            for x in range(self.columns):
                if (x, y) in self.locked_cells:
                    del self.locked_cells[(x, y)]
        

        # ✅ STEP: Rebuild the grid by shifting everything down
        new_locked_cells = {}
        for y in range(self.rows - 1, -1, -1):
            if y not in full_rows:
                shift = sum(1 for cleared_row in full_rows if cleared_row > y)
                for x in range(self.columns):
                    if (x, y) in self.locked_cells:
                        new_pos = (x, y + shift) if shift > 0 else (x, y)
                        new_locked_cells[new_pos] = self.locked_cells[(x, y)]

        self.locked_cells = new_locked_cells
        if debug:
            print("After:", sorted(self.locked_cells.keys(), key=lambda x: x[1]))
        return True

    def draw_ghost_cells(self, grids, color):
        # Draw multiple cells as outlines for the ghost piece
        for i in grids:
            x, y = self.to_pixel(i)
            # The 'width=2' parameter tells pygame to draw only the border of the rectangle
            pygame.draw.rect(self.screen, color, (x, y, self.BLOCK, self.BLOCK), width=2, border_radius=7) #type: ignore