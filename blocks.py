import random, time
class blocks():
    def __init__(self, grid):
        self.grid = grid
        self.columns = grid.columns
        self.rows = grid.rows
        self.color = random.choice(["red", "blue", "green", "yellow", "purple"])
        self.shapes = {'Line': [[0, 0], [1, 0], [2, 0], [3, 0]],
                  'L-Shape': [[0, 0], [0, 1], [1, 1], [2, 1]],
                  'Square': [[0, 0], [1, 0], [0, 1], [1, 1]],
                  'Snake': [[1, 0], [2, 0], [0, 1], [1, 1]],
                  'Inv-L-Shape': [[2, 0], [0, 1], [1, 1], [2, 1]],
                  'Inv-Snake': [[1, 1], [2, 1], [0, 0], [1, 0]],
                  'Inv-T-shape': [[0, 1], [1, 1], [2, 1], [1, 0]]}
        self.shape_name = random.choice(list(self.shapes.keys()))
        shape_coords = self.shapes[self.shape_name]
        max_x = max(x for x, _ in shape_coords)
        self.dx = random.randint(0, grid.columns - max_x - 1)
        self.shape = [[x + self.dx, y] for x, y in shape_coords]
        self.last_move_time = time.time()

    def move(self, delta: tuple):
        new_shape = [[x + delta[0], y + delta[1]] for x, y in self.shape]
        if all(0 <= x < self.columns and 0 <= y < self.rows for x, y in new_shape):
            self.shape = new_shape

    def update(self, speed):
        if time.time() - self.last_move_time > (0.5)/(speed):
            self.move((0,1))
            self.last_move_time = time.time()
            print(self.shape)

    def draw_shape(self):
        self.grid.draw_cells(self.shape, self.color)
        
    def end(self):
        for i in self.shape:
            if i[1] == (self.rows)-1:
                print("\nNEW SHAPE\n")
                return True
        return False