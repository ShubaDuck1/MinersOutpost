import pygame;
import structures;

TILE_SIZE = 16;
TILE_WIDTH = 80;
TILE_HEIGHT = 45;

class Tile:
    valid_type = ['grass', 'road', 'water'];
    adjacent = [(1, 0), (0, 1), (-1, 0), (0, -1)];
    diagonal = [(1, 1), (1, -1), (-1, 1), (-1, -1)];
    
    def __init__(self):
        self._type = 'grass';
        self.is_foggy = True;
        self.structure = None;
        
    @property
    def type(self):
        return self._type;
    
    @type.setter
    def type(self, value):
        if value not in Tile.valid_type:
            raise ValueError(f'Invalid type: {value}');
        self._type = value;
        
    def modify_speed(self):
        if self.type == 'grass':
            return 1;
        elif self.type == 'road':
            return 1.5;
        elif self.type == 'water':
            return 0.5;
        
    def set_structure(self, structure):
        if self.structure:
            return;
        self.structure = structure;
    
    def remove_structure(self):
        self.structure = None;
    
    def update(self):
        if not self.structure:
            return;
        
        if self.structure.is_destroyed:
            self.remove_structure();
            
        if type(self.structure) == structures.Constructor  and self.structure.check():
            self.structure.update(self);
        
def pixel_to_tile(position):
    return int(position[0] // TILE_SIZE), int(position[1] // TILE_SIZE);
        
def draw_tile(screen, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            curr_tile = grid[y][x];
            if curr_tile.is_foggy:
                continue;
            g = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE);
            if curr_tile.type == 'grass':
                color = pygame.Color('green');
            elif curr_tile.type == 'water':
                color = (14, 135, 204);
            elif curr_tile.type == 'road':
                color = pygame.Color('saddlebrown');
            
            pygame.draw.rect(screen, color, g);
            
def draw_fog(screen, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            curr_tile = grid[y][x];
            
            if not curr_tile.is_foggy:
                continue;
            
            g = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE);
            pygame.draw.rect(screen, pygame.Color('grey'), g);

def draw_structure(screen, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            curr_tile = grid[y][x];
            if curr_tile.structure and not curr_tile.is_foggy:
                curr_tile.structure.draw(screen, (x, y));
    
def draw_hover(screen):
    x, y = pixel_to_tile(pygame.mouse.get_pos());
    g = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE);
    pygame.draw.rect(screen, pygame.Color('white'), g, 2)