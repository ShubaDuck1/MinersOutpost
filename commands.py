import tiles
import math;

def magnitude(vector):
    return round(math.sqrt(vector[0] ** 2 + vector[1] ** 2), 1);
            
def normalize(vector: tuple[int, int]):
    mag = magnitude(vector);
    if mag == 0:
        mag = 0.1;
    
    return round(vector[0] / mag, 1), round(vector[1] / mag, 1);

class Command:
    def __init__(self, unit):
        self.unit = unit;
        self.is_done = False;
    
    def execute(self):
        raise NotImplementedError("execute() Not Implemented");
    
SPEED_SCALAR = tiles.TILE_SIZE * 2;
    
class Move(Command):
    def __init__(self, unit, destination):
        super().__init__(unit);
        self.destination = destination;
        
    def execute(self, delta_time):
        dest_x, dest_y = self.destination;
        dest_x = dest_x * tiles.TILE_SIZE + tiles.TILE_SIZE // 2;
        dest_y = dest_y * tiles.TILE_SIZE + tiles.TILE_SIZE // 2;
        
        dir_x, dir_y = normalize((dest_x - self.unit.position[0], dest_y - self.unit.position[1]));
        
        self.unit.position = (self.unit.position[0] + dir_x * self.unit.modified_speed * SPEED_SCALAR * delta_time, 
                              self.unit.position[1] + dir_y * self.unit.modified_speed * SPEED_SCALAR * delta_time);
        
        mag = magnitude((dest_x - self.unit.position[0], 
                         dest_y - self.unit.position[1]));
        
        if mag <= 2:
            self.is_done = True;
            
class Attack(Command):
    def __init__(self, enemy, tile):
        super().__init__(enemy);
        self.tile = tile;
        self.progress = 0;
    
    def check(self):
        return self.unit.can_go_through(self.tile);
    
    def execute(self, delta_time):
        if self.check():
            self.is_done = True;
            return;
        
        self.progress += delta_time;
        if self.progress >= 1:
            self.progress = 0;
            self.tile.structure.current_health -= self.unit.damage;
            
            if self.tile.structure.current_health <= 0:
                self.tile.structure.is_destroyed = True;
            

class Harvest(Command):
    def __init__(self, miner, structure):
        super().__init__(miner);
        self.structure = structure;
        
    def execute(self, delta_time):
        self.structure.interact(self.unit, delta_time);
        
        if self.structure.is_destroyed or self.unit.is_full():
            self.is_done = True;
            self.structure.is_occupied = False;
            
class GiveAll(Command):
    def __init__(self, miner, structure):
        super().__init__(miner);
        self.structure = structure;
        
    def execute(self, delta_time):
        for resource in self.structure.inventory:
            type = self.unit.inventory.type;
            amount = self.unit.inventory.amount;
            if resource.add(type, amount):
                self.unit.inventory.remove(type, amount);
                break;
        self.is_done = True;
        
class TakeResource(Command):
    def __init__(self, miner, structure, type, amount):
        super().__init__(miner);
        self.structure = structure;
        self.type = type;
        self.amount = amount;
        
    def execute(self, delta_time):
        type = self.type;
        amount = self.amount;
        
        for resource in self.structure.inventory:
            if resource.remove(type, amount):
                self.unit.inventory.add(type, amount);
                break;
        self.is_done = True;
        
class GiveResource(Command):
    def __init__(self, miner, structure):
        super().__init__(miner);
        self.structure = structure;
        
    def execute(self, delta_time):
        for resource in self.structure.inventory:
            type = resource.type;
            amount = min(self.unit.inventory.amount, resource.amount);
            if resource.remove(type, amount):
                self.unit.inventory.remove(type, amount);
                break;
        self.is_done = True;
        self.structure.is_occupied = False;