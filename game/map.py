import random
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.core.image import Image as CoreImage

# For the new generator, we only need two basic tile types.
# The MapWidget can still use a tileset for visual flair.
TILE_MAPPING = {
    'FLOOR': (0, 0), # Example: floor_1 from old mapping
    'WALL': (1, 2),  # Example: wall_top from old mapping
}

class MapGenerator:
    def __init__(self, width, height, iterations=5, wall_chance=0.45):
        self.width = width
        self.height = height
        self.iterations = iterations
        self.wall_chance = wall_chance
        self.map_grid = []

    def generate_map(self):
        # 1. Randomly initialize the map
        self.map_grid = [['WALL' if random.random() < self.wall_chance else 'FLOOR'
                          for _ in range(self.width)] for _ in range(self.height)]

        # 2. Run the cellular automata simulation
        for _ in range(self.iterations):
            self.map_grid = self._simulation_step(self.map_grid)

        # 3. (Optional but recommended) Post-processing: Remove small islands, ensure connectivity
        # This part can be complex, so we'll start with the raw output first.

        return self.map_grid

    def _simulation_step(self, grid):
        new_grid = [row[:] for row in grid]
        for y in range(self.height):
            for x in range(self.width):
                wall_neighbors = self._count_wall_neighbors(grid, x, y)

                # Rule: A cell becomes a wall if it has 5 or more wall neighbors.
                # A cell becomes a floor if it has 4 or fewer.
                if wall_neighbors > 4:
                    new_grid[y][x] = 'WALL'
                elif wall_neighbors < 4:
                    new_grid[y][x] = 'FLOOR'
                # If it's exactly 4, it remains unchanged to create stability.

        return new_grid

    def _count_wall_neighbors(self, grid, x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue

                check_x, check_y = x + i, y + j

                # Treat out-of-bounds as walls to create a solid border
                if (check_x < 0 or check_x >= self.width or
                    check_y < 0 or check_y >= self.height or
                    grid[check_y][check_x] == 'WALL'):
                    count += 1
        return count

    def get_random_floor_tile(self):
        """
        Finds a random, accessible floor tile to spawn the player.
        """
        floor_tiles = []
        for y in range(self.height):
            for x in range(self.width):
                if self.map_grid[y][x] == 'FLOOR':
                    floor_tiles.append((x, y))

        return random.choice(floor_tiles) if floor_tiles else (self.width // 2, self.height // 2)


class MapWidget(Widget):
    def __init__(self, map_grid, tile_size, **kwargs):
        super().__init__(**kwargs)
        self.map_grid = map_grid
        self.tile_size = tile_size
        self.size = (len(map_grid[0]) * tile_size, len(map_grid) * tile_size)
        # For simplicity in testing, we'll use colors first.
        # A proper tileset can be re-integrated later.
        self.tile_colors = {
            'WALL': (0.3, 0.3, 0.3, 1), # Dark grey
            'FLOOR': (0.7, 0.7, 0.7, 1)  # Light grey
        }
        self.draw_map()

    def draw_map(self):
        self.canvas.clear()
        with self.canvas:
            for y, row in enumerate(self.map_grid):
                for x, tile_name in enumerate(row):
                    Color(*self.tile_colors.get(tile_name, (0, 0, 0, 1)))
                    Rectangle(pos=(x * self.tile_size, y * self.tile_size),
                              size=(self.tile_size, self.tile_size))