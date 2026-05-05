import queue;
import resources;
import commands;
import structures;

class Unit:
    def __init__(self, speed, position, radius):
        self.speed = speed;
        self.modified_speed = speed;
        self.position = position;
        self.radius = radius;
        self.task = queue.Queue();
        
    def is_busy(self):
        return not self.task.empty();
    
    def set_path(self, path):
        for destination in path:
            self.task.put(commands.Move(self, destination));
    
    def update(self, delta_time):
        if not self.task.empty():
            curr_task = self.task.queue[0];
            curr_task.execute(delta_time);
            
            if curr_task.is_done:
                self.task.get();
        
class Miner(Unit):
    valid_type = ['default', 'horse']
    
    def __init__(self, type, position):
        if type not in self.valid_type:
            raise ValueError(f"Invalid type: {type}");
        
        if type == 'default':
            super().__init__(1, position, 5);
        elif type == 'horse':
            super().__init__(2, position, 5);
        
        self.type = type;
        self.vision_range = 3;
        self.inventory = resources.Resource();
        self.full = 5;
        
    def set_harvest(self, structure):
        self.task.put(commands.Harvest(self, structure));
        
    def set_give_all(self, structure):
        self.task.put(commands.GiveAll(self, structure));
        
    def set_take_resource(self, structure, type, amount):
        self.task.put(commands.TakeResource(self, structure, type, amount));
        
    def set_give_resource(self, structure):
        self.task.put(commands.GiveResource(self, structure));
        
    def is_full(self):
        return self.inventory.amount == self.full;
        
    def is_go_to_base(self):
        if self.is_busy():
            return False;
        
        if self.inventory.type == None:
            return False;
        
        return True;  
    
    def can_go_through(self, tile):
        if self.type == 'default':
            if tile.structure and type(tile.structure) != structures.Spike:
                return False;
            return True;
        elif self.type == 'horse':
            return tile.type == 'road';
    
class Enemy(Unit):
    def __init__(self, position):
        super().__init__(1, position, 5);
        self.max_health = 30;
        self.current_health = self.max_health;
        self.damage = 10;
        self.is_destroyed = False;
        
    def take_damage(self, structure):
        self.current_health -= structure.damage;
        if self.current_health <= 0:
            self.is_destroyed = True;
        
    def set_attack_base(self, space, path):
        for x, y in path:
            self.task.put(commands.Attack(self, space.grid[y][x]));
            self.task.put(commands.Move(self, (x, y)));
        self.task.put(commands.Attack(self, space.grid[space.base_position[1]][space.base_position[0]]));
        
    def can_go_through(self, tile):
        if tile.structure:
            return False;
        return True;