import pygame;

TILE_SIZE = 16;
TILE_WIDTH = 80;
TILE_HEIGHT = 45;

class Tile:
    valid_type = ['grass', 'road', 'building'];
    adjacent = [(1, 0), (0, 1), (-1, 0), (0, -1)];
    
    def __init__(self):
        self._type = 'grass';
        self.is_fog = True;
    
    @property
    def type(self):
        return self._type;
    
    @type.setter
    def type(self, value):
        if value not in Tile.valid_type:
            raise ValueError(f'Invalid type: {value}');
        self._type = value;
        
def pixel_to_tile(position):
    return position[0] // TILE_SIZE, position[1] // TILE_SIZE;
        
def draw_tile(screen, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            g = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE);
            pygame.draw.rect(screen, pygame.Color('green'), g);
    
    x, y = pixel_to_tile(pygame.mouse.get_pos());
    g = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE);
    pygame.draw.rect(screen, pygame.Color('white'), g, 2)