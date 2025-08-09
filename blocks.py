import random
import time as tm
import numpy as np

class blocks():

    def __init__(self, grid, time, shape_name=None, color=None):
        # Initialize block properties
        self.time = time
        self.locked = False
        self.grid = grid
        self.columns = grid.columns
        self.rows = grid.rows
        self.shape_id = random.randint(-10000, 10000)
        
        # Define original shapes for the blocks
        self.ORIGINAL_SHAPES = {
            'Line': np.array([[0, 0], [1, 0], [2, 0], [3, 0]]),
            'L': np.array([[0, 0], [0, 1], [1, 1], [2, 1]]),
            'Square': np.array([[0, 0], [1, 0], [0, 1], [1, 1]]),
            'Snake': np.array([[2, 0], [1, 0], [1, 1], [0, 1]]),
            'Inv_L': np.array([[0, 1], [1, 1], [2, 1], [2, 0]]),
            'Inv_Snake': np.array([[1, 1], [2, 1], [0, 0], [1, 0]]),
            'T': np.array([[0, 1], [1, 1], [2, 1], [1, 0]])
        }
        
        # Generate all possible rotations for the shapes
        self.SHAPES = self.generate_rotations()

        # Use the provided shape_name or pick a random one
        self.shape_name = shape_name if shape_name else random.choice(list(self.SHAPES.keys()))
        self.color = color if color else random.choice(["red", "blue", "green", "yellow", "purple"])
        
        # Always pick a new "next" piece randomly
        self.next_color = random.choice(["red", "blue", "green", "yellow", "purple"])
        self.next_shape_name = random.choice(list(self.SHAPES.keys()))
        
        self.shape_coords = self.SHAPES[self.shape_name]

        # Center the block horizontally on the grid
        max_x = max(x for x, _ in self.shape_coords)
        self.dx = (grid.columns - max_x - 1) // 2
        self.dy = 0
        self.update_shape()
        
        # Initialize shape position and movement properties
        self.shape = tuple([tuple([x + self.dx, y + self.dy]) for x, y in self.shape_coords])
        self.last_move_time = tm.time()
        self.on_ground = False
        self.lock_delay_start_time = 0
        self.LOCK_DELAY = 400
        self.game_over = False
        
        # Check for game over condition
        for x, y in self.shape:
            if (x, y) in self.grid.locked_cells:
                self.game_over = True
        

    def test(self):
        # Debugging function to print shape details and screen size
        (SCREEN_WIDTH, SCREEN_HEIGHT) = (self.grid.width,self.grid.height)
        print("Debug: Screen Size ",(SCREEN_WIDTH, SCREEN_HEIGHT))
        print("Shape coords:", self.shape_coords)
        print("Shape name:", self.shape_name)
        print(self.shape)
        print("Type of items:", [type(coord) for coord in self.shape_coords])
        print("Coord lengths:", [len(coord) for coord in self.shape_coords])

    def _reset_lock_delay(self):
        # Resets the lock timer if the piece is moved while on the ground
        if self.on_ground:
            self.lock_delay_start_time = self.time.get_ticks()    
    
    def update_shape(self):
        # Update the shape's position based on current offsets
        self.shape = tuple((x + self.dx, y + self.dy) for x, y in self.shape_coords)

    def generate_rotations(self):
        # Generate all rotations for each shape
        shapes = {}
        for name, shape in self.ORIGINAL_SHAPES.items():
            current = shape
            for i in range(4):
                # Convert shape coordinates to tuples
                coord = [tuple(point) for point in current]
                key = f"{name}-{chr(65 + i)}"
                shapes[key] = coord
                
                # Rotate the shape 90 degrees clockwise
                current = np.array([[y, -x] for x, y in current])
                # Normalize the shape to ensure it fits within the grid
                min_x = min(coord[0] for coord in current)
                min_y = min(coord[1] for coord in current)
                current = np.array([[x - min_x, y - min_y] for x, y in current])
        return shapes

    def move(self, delta: tuple):
        # Move the block by a given delta (dx, dy)
        new_dx = self.dx + delta[0]
        new_dy = self.dy + delta[1]
        new_shape = tuple([tuple([x + new_dx, y + new_dy]) for x, y in self.shape_coords])
        
        # Check if the new position is valid
        if all(0 <= x < self.columns and 0 <= y < self.rows and (x, y) not in self.grid.locked_cells for x, y in new_shape):
            self.dx = new_dx
            self.dy = new_dy
            self.update_shape()
            self._reset_lock_delay()

    def update(self, speed):
        # Automatically move the block down based on speed
        if tm.time() - self.last_move_time > (0.5) / (speed):
            self.move((0, 1))
            self.last_move_time = tm.time()
    
    def rotate(self):
        # Rotate the block to the next orientation
        current_name_part, current_rotation = self.shape_name.split('-')
        next_rotation_char = chr(((ord(current_rotation) - ord('A') + 1) % 4) + ord('A'))
        next_shape_name = f"{current_name_part}-{next_rotation_char}"
        
        if next_shape_name in self.SHAPES:
            next_shape_coords = self.SHAPES[next_shape_name]
            # Create a temporary shape at the current offset to test for collisions
            new_shape = tuple((x + self.dx, y + self.dy) for x, y in next_shape_coords)

            # Check if the rotation is valid
            if all(0 <= x < self.columns and 0 <= y < self.rows and (x, y) not in self.grid.locked_cells for x, y in new_shape):
                # If valid, apply the new shape name and coordinates
                self.shape_name = next_shape_name
                self.shape_coords = next_shape_coords
                self.update_shape()
                self._reset_lock_delay()

    def draw_shape(self):
        # Draw the block on the grid
        self.grid.draw_cells(self.shape, self.color)
        
    def end(self):
        # Handle the end-of-life behavior for the block
        is_touching_ground = False
        for x, y in self.shape:
            # Check if the block is touching the ground or another piece
            if y == self.rows - 1 or (x, y + 1) in self.grid.locked_cells:
                is_touching_ground = True
                break
        
        if is_touching_ground:
            # If the block is on the ground, start the lock timer
            if not self.on_ground:
                self.on_ground = True
                self.lock_delay_start_time = self.time.get_ticks()

            # If the timer has expired, lock the piece
            if self.time.get_ticks() - self.lock_delay_start_time > self.LOCK_DELAY:
                self.locked = True
                self.grid.lock_cells(self.shape, self.color, self.shape_id)
                self.grid.score+=1
                
        else:
            # If the block is in the air, cancel any active timer
            self.on_ground = False

    def _find_landing_y(self, dx_offset):
        """
        Private helper method to find the final y-offset for a piece at a given x-offset.
        Returns the final valid y-offset.
        """
        y_probe = self.dy
        while True:
            test_shape = tuple((x + dx_offset, y + y_probe) for x, y in self.shape_coords)
            if all(0 <= x < self.columns and y < self.rows and (x, y) not in self.grid.locked_cells for x, y in test_shape):
                y_probe += 1
            else:
                break
        return y_probe - 1

    def get_ghost_position(self):
        """
        Calculates the coordinates for the ghost piece by calling the helper method.
        """
        final_dy = self._find_landing_y(dx_offset=self.dx)
        ghost_shape = tuple((x + self.dx, y + final_dy) for x, y in self.shape_coords)
        return ghost_shape
        
    def smash_down(self):
        """
        Instantly moves the block to its final position and locks it.
        """
        final_dy = self._find_landing_y(dx_offset=self.dx)
        self.dy = final_dy
        self.update_shape()
        self.grid.lock_cells(self.shape, self.color, self.shape_id)
        self.locked = True