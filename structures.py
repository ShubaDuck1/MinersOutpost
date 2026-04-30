import pygame;
import tiles;
import resources;

class Structure:
    def __init__(self, max_health, is_interactable = True):
        self.max_health = max_health;
        self.current_health = max_health;
        self.is_destroyed = False;
        self.is_interactable = is_interactable;
    
    def interact(self):
        pass;
    
class Tree(Structure):
    def __init__(self):
        super().__init__(50);
        self.progress = 0;
        
    def draw(self, screen, position):
        x = position[0] * tiles.TILE_SIZE + tiles.TILE_SIZE // 2;
        y = position[1] * tiles.TILE_SIZE + tiles.TILE_SIZE // 2;
        pygame.draw.circle(screen, pygame.Color('darkgreen'), (x, y), tiles.TILE_SIZE // 2);
        
    def interact(self, miner, delta_time):
        self.progress += delta_time;
        
        if self.progress >= 1:
            self.progress -= 1;
            self.current_health -= 1;
            miner.inventory.add('wood');
        
        if self.current_health <= 0:
            self.is_destroyed = True;

class Base(Structure):
    def __init__(self):
        super().__init__(1000);
        self.inventory = [resources.Resource()];
        
    def draw(self, screen, position):
        x = position[0] * tiles.TILE_SIZE + tiles.TILE_SIZE // 2;
        y = position[1] * tiles.TILE_SIZE + tiles.TILE_SIZE // 2;
        pygame.draw.circle(screen, pygame.Color('blue'), (x, y), tiles.TILE_SIZE // 2);
    