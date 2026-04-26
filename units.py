import queue;
import tiles;
import math;

class Unit:
    def __init__(self, speed, position, radius):
        self.speed = speed;
        self.position = position;
        self.radius = radius;
        self.path = queue.Queue();
        
    def is_busy(self):
        if not self.path.empty():
            return True;
        
        return False;
        
    def set_path(self, path):
        for items in path:
            self.path.put(items);
    
    def follow_path(self, delta_time):
        if self.path.empty():
            return;
        dest_x, dest_y = self.path.queue[0]; 
        if tiles.pixel_to_tile(self.position) == (dest_x, dest_y):
            self.path.get();
        
        dest_x = dest_x * tiles.TILE_SIZE + tiles.TILE_SIZE // 2;
        dest_y = dest_y * tiles.TILE_SIZE + tiles.TILE_SIZE // 2;
        dir_x, dir_y = normalize((dest_x - self.position[0], dest_y - self.position[1]));
        
        self.position = (self.position[0] + dir_x * self.speed * delta_time,
                         self.position[1] + dir_y * self.speed * delta_time);
    
    def update(self, delta_time):
        self.follow_path(delta_time);
        
            
def normalize(vector: tuple[int, int]):
    magnitude = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    res = (vector[0] / magnitude, vector[1] / magnitude);
    
    return res;