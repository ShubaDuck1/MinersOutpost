import pygame;
import structures;
import settings;
import render;

class Tile:
    valid_type = ['grass', 'road', 'water', 'sand'];
    adjacent = [(1, 0), (0, 1), (-1, 0), (0, -1)];
    diagonal = [(1, 1), (1, -1), (-1, 1), (-1, -1)];
    
    def __init__(self):
        self._type = 'grass';
        self.is_foggy = True;
        self.structure = None;
        
        self.renderer = render.TileRenderer(self);
        
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
            return 0.25;
        elif self.type == 'sand':
            return 0.8;
        
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
            
        if type(self.structure) == structures.Constructor and self.structure.check():
            self.structure.update(self);
        
def pixel_to_tile(position):
    return int(position[0] // settings.TILE_SIZE), int(position[1] // settings.TILE_SIZE);
        
def draw_tile(screen, grid, offset, delta_time):
    for y in range(max(0, -3 - offset[1] // settings.TILE_SIZE), min(settings.TILE_HEIGHT, (settings.HEIGHT - offset[1]) // settings.TILE_SIZE + 3)):
        for x in range(max(0, -3 - offset[0] // settings.TILE_SIZE), min(settings.TILE_WIDTH, (settings.WIDTH - offset[0]) // settings.TILE_SIZE + 3)):
            curr_tile = grid[y][x];
            if curr_tile.is_foggy:
                continue;
            
            curr_tile.renderer.draw(screen, (x, y), offset, delta_time);
            
def draw_fog(screen, grid, offset):
    for y in range(max(0, -3 - offset[1] // settings.TILE_SIZE), min(settings.TILE_HEIGHT, (settings.HEIGHT - offset[1]) // settings.TILE_SIZE + 3)):
        for x in range(max(0, -3 - offset[0] // settings.TILE_SIZE), min(settings.TILE_WIDTH, (settings.WIDTH - offset[0]) // settings.TILE_SIZE + 3)):
            curr_tile = grid[y][x];
            
            if not curr_tile.is_foggy:
                continue;
            
            curr_tile.renderer.fog.draw(screen, (x, y), offset);

def draw_structure(screen, grid, offset, delta_time):
    for y in range(max(0, -3 - offset[1] // settings.TILE_SIZE), min(settings.TILE_HEIGHT, (settings.HEIGHT - offset[1]) // settings.TILE_SIZE + 3)):
        for x in range(max(0, -3 - offset[0] // settings.TILE_SIZE), min(settings.TILE_WIDTH, (settings.WIDTH - offset[0]) // settings.TILE_SIZE + 3)):
            curr_tile = grid[y][x];
            if curr_tile.structure and not curr_tile.is_foggy:
                try:
                    curr_tile.structure.renderer.draw(screen, (x, y), offset, delta_time);
                except:
                    curr_tile.structure.draw(screen, (x, y), offset);
    
def draw_hover(screen, offset):
    pos = pygame.mouse.get_pos();
    x, y = pixel_to_tile((pos[0] - offset[0], pos[1] - offset[1]));
    
    g = pygame.Rect(x * settings.TILE_SIZE + offset[0], y * settings.TILE_SIZE + offset[1], settings.TILE_SIZE, settings.TILE_SIZE);
    pygame.draw.rect(screen, pygame.Color('white'), g, 2)
    
def draw_drag(screen, last_pos, last_offset, offset):
    left, top = pixel_to_tile((last_pos[0] - last_offset[0], last_pos[1] - last_offset[1]));
    pos = pygame.mouse.get_pos();
    right, bottom = pixel_to_tile((pos[0] - offset[0], pos[1] - offset[1]));
    
    if top > bottom:
        top, bottom = bottom, top;
    if left > right:
        left, right = right, left;
    
    g = pygame.Rect(left * settings.TILE_SIZE + offset[0], top * settings.TILE_SIZE + offset[1], 
                    (right - left + 1) * settings.TILE_SIZE, (bottom - top + 1) * settings.TILE_SIZE);
    pygame.draw.rect(screen, pygame.Color('white'), g, 2);