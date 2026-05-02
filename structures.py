import pygame;
import tiles;
import resources;

class Structure:
    def __init__(self, max_health):
        self.max_health = max_health;
        self.current_health = max_health;
        self.is_destroyed = False;
        self.is_interactable = True;
        self.is_harvestable = False;
        self.is_occupied = False;
    
    def interact(self, miner, delta_time):
        pass;
    
    def draw(self, screen, position):
        pass;
        
class Constructor(Structure):
    def __init__(self, structure):
        super().__init__(1);
        self.structure = structure;
        self.inventory = self.set_inventory();
        
    def set_inventory(self):
        res = [];
        
        if self.structure == 'road':
            res.append(resources.Resource('wood', 1));
        elif type(self.structure) == Spike:
            res.append(resources.Resource('wood', 10));
        
        return res;
        
    def check(self):
        for resource in self.inventory:
            if resource.amount != 0:
                return False;
        return True;
        
    def update(self, tile):
        if self.structure == 'road':
            tile.type = 'road';
            tile.structure = None;
        else:
            tile.structure = self.structure;
    
class Tree(Structure):
    def __init__(self):
        super().__init__(50);
        self.progress = 0;
        self.is_harvestable = True;
        
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
    
class Spike(Structure):
    def __init__(self):
        super().__init__(200);
        self.is_harvestable = False;
        self.is_interactable = False;
        
    def draw(self, screen, position):
        x = position[0] * tiles.TILE_SIZE + tiles.TILE_SIZE // 2;
        y = position[1] * tiles.TILE_SIZE + tiles.TILE_SIZE // 2;
        pygame.draw.circle(screen, (193, 154, 107), (x, y), tiles.TILE_SIZE // 2);
        
class Crossbow(Structure):
    def __init__(self):
        super().__init__(50);
        self.is_harvestable = False;
        self.is_interactable = False;
        
    def draw(self, screen, position):
        x = position[0] * tiles.TILE_SIZE + tiles.TILE_SIZE // 2;
        y = position[1] * tiles.TILE_SIZE + tiles.TILE_SIZE // 2;
        pygame.draw.circle(screen, (193, 154, 107), (x, y), tiles.TILE_SIZE // 2);