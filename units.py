import queue;
import tiles;
import math;
import resources;

class Unit:
    def __init__(self, speed, position, radius):
        self.speed = speed;
        self.position = position;
        self.radius = radius;
        self.path = queue.Queue();
        self.current_task = None;
        
    def is_busy(self):
        if not self.path.empty():
            return True;
        if self.current_task != None:
            return True;
        return False;
    
    def set_task(self, task):
        self.current_task = task;
    
    def do_task(self, delta_time):
        pass;
        
    def set_path(self, path):
        for items in path:
            self.path.put(items);
            
    def arrived(self, destination):
        mag = magnitude((destination[0] - self.position[0], destination[1] - self.position[1]));
        if mag <= 2:
            return True;
        return False;
    
    def follow_path(self, delta_time):
        if self.path.empty():
            return False;
        
        dest_x, dest_y = self.path.queue[0]; 
        dest_x = dest_x * tiles.TILE_SIZE + tiles.TILE_SIZE // 2;
        dest_y = dest_y * tiles.TILE_SIZE + tiles.TILE_SIZE // 2;
        
        if self.arrived((dest_x, dest_y)):
            self.path.get();
        
        dir_x, dir_y = normalize((dest_x - self.position[0], dest_y - self.position[1]));
        
        self.position = (self.position[0] + dir_x * self.speed * tiles.TILE_SIZE * delta_time,
                         self.position[1] + dir_y * self.speed * tiles.TILE_SIZE * delta_time);
        
        return True;
    
    def update(self, delta_time):
        if self.follow_path(delta_time):
            return;
        self.do_task(delta_time);
        
class Miner(Unit):
    valid_type = ['default', 'horse']
    
    def __init__(self, type, position):
        if type not in self.valid_type:
            raise ValueError(f"Invalid type: {type}");
        
        if type == 'default':
            super().__init__(1, position, 5);
        elif type == 'horse':
            super().__init__(2, position, 5);
            
        self.inventory = resources.Resource();
            
    def do_task(self, delta_time):
        if not self.current_task:
            return;
        
        if self.current_task.is_destroyed:
            self.set_task(None);
            return;
        
        if self.inventory.amount == 10:
            self.set_task(None);
            return;
        
        self.current_task.interact(self, delta_time);
    
    def can_go_through(self, structure):
        if not structure:
            return True;
        return False;
    
def magnitude(vector):
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2);
            
def normalize(vector: tuple[int, int]):
    mag = magnitude(vector);
    res = (vector[0] / mag, vector[1] / mag);
    return res;