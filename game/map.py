import random
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.core.image import Image as CoreImage

# Annahme: Das Tileset ist 16x16 Pixel pro Tile.
# Die Koordinaten sind in (x, y) * 16 Pixel.
TILE_MAPPING = {
    # Böden
    'floor_1': (0, 0),
    'floor_2': (1, 0),
    'floor_3': (2, 0),

    # Wände (Beispiele, müssen eventuell angepasst werden)
    'wall_top': (1, 2),
    'wall_bottom': (1, 4),
    'wall_left': (0, 3),
    'wall_right': (2, 3),
    'wall_top_left': (0, 2),
    'wall_top_right': (2, 2),
    'wall_bottom_left': (0, 4),
    'wall_bottom_right': (2, 4),
    'wall_inner_top_left': (3, 2),
    'wall_inner_top_right': (4, 2),
    'wall_inner_bottom_left': (3, 4),
    'wall_inner_bottom_right': (4, 4),

    # Dekorationen
    'deco_1': (6, 0),
    'deco_2': (7, 0),
}

class Room:
    def __init__(self, x, y, w, h):
        self.x1, self.y1 = x, y
        self.x2, self.y2 = x + w, y + h

    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return (center_x, center_y)

    def intersects(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

class MapGenerator:
    def __init__(self, width, height, tile_size, max_rooms=15, min_room_size=6, max_room_size=10):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.max_rooms = max_rooms
        self.min_room_size = min_room_size
        self.max_room_size = max_room_size
        self.map_grid = []
        self.rooms = []

    def generate_map(self):
        self.map_grid = [['empty' for _ in range(self.width)] for _ in range(self.height)]
        self.rooms = []

        for _ in range(self.max_rooms):
            w = random.randint(self.min_room_size, self.max_room_size)
            h = random.randint(self.min_room_size, self.max_room_size)
            x = random.randint(1, self.width - w - 1)
            y = random.randint(1, self.height - h - 1)

            new_room = Room(x, y, w, h)

            failed = False
            for other_room in self.rooms:
                if new_room.intersects(other_room):
                    failed = True
                    break

            if not failed:
                self.create_room(new_room)
                (new_x, new_y) = new_room.center()

                if self.rooms:
                    (prev_x, prev_y) = self.rooms[-1].center()
                    if random.randint(0, 1) == 1:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                self.rooms.append(new_room)

        self.place_walls()
        self.place_decorations()
        return self.map_grid

    def create_room(self, room):
        for x in range(room.x1, room.x2):
            for y in range(room.y1, room.y2):
                self.map_grid[y][x] = 'floor_1'

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.map_grid[y][x] = 'floor_1'

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.map_grid[y][x] = 'floor_1'

    def place_walls(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map_grid[y][x] == 'empty':
                    is_floor_above = y + 1 < self.height and self.map_grid[y+1][x].startswith('floor')
                    is_floor_below = y - 1 >= 0 and self.map_grid[y-1][x].startswith('floor')
                    is_floor_left = x - 1 >= 0 and self.map_grid[y][x-1].startswith('floor')
                    is_floor_right = x + 1 < self.width and self.map_grid[y][x+1].startswith('floor')

                    if is_floor_below and is_floor_right: self.map_grid[y][x] = 'wall_inner_top_left'
                    elif is_floor_below and is_floor_left: self.map_grid[y][x] = 'wall_inner_top_right'
                    elif is_floor_above and is_floor_right: self.map_grid[y][x] = 'wall_inner_bottom_left'
                    elif is_floor_above and is_floor_left: self.map_grid[y][x] = 'wall_inner_bottom_right'
                    elif is_floor_below: self.map_grid[y][x] = 'wall_top'
                    elif is_floor_above: self.map_grid[y][x] = 'wall_bottom'
                    elif is_floor_left: self.map_grid[y][x] = 'wall_right'
                    elif is_floor_right: self.map_grid[y][x] = 'wall_left'

    def place_decorations(self):
        for room in self.rooms:
            for x in range(room.x1 + 1, room.x2 - 1):
                for y in range(room.y1 + 1, room.y2 - 1):
                    if self.map_grid[y][x].startswith('floor'):
                        if random.random() < 0.1:
                            self.map_grid[y][x] = random.choice(['floor_2', 'floor_3'])
                        if random.random() < 0.05:
                            self.map_grid[y][x] = random.choice(['deco_1', 'deco_2'])

class MapWidget(Widget):
    def __init__(self, map_grid, tile_size, **kwargs):
        super().__init__(**kwargs)
        self.map_grid = map_grid
        self.tile_size = tile_size
        self.tileset_texture = CoreImage('assets/environment/Tilesets/Dungeon_Tiles.png').texture

        self.textures = {}
        for name, coords in TILE_MAPPING.items():
            x, y = coords[0] * 16, coords[1] * 16
            self.textures[name] = self.tileset_texture.get_region(x, y, 16, 16)

        self.draw_map()

    def draw_map(self):
        self.canvas.clear()
        with self.canvas:
            for y, row in enumerate(self.map_grid):
                for x, tile_name in enumerate(row):
                    if tile_name and tile_name in self.textures:
                        pos = (x * self.tile_size, y * self.tile_size)
                        if tile_name.startswith('deco'):
                            # Zeichne zuerst den Boden und dann die Deko darüber
                            Rectangle(texture=self.textures['floor_1'], pos=pos, size=(self.tile_size, self.tile_size))
                            Rectangle(texture=self.textures[tile_name], pos=pos, size=(self.tile_size, self.tile_size))
                        else:
                            Rectangle(texture=self.textures[tile_name], pos=pos, size=(self.tile_size, self.tile_size))

    def update_view(self, camera_pos):
        pass