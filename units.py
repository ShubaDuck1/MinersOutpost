import queue;
import resources;
import commands;

class Unit:
    def __init__(self, speed, position, radius):
        self.speed = speed;
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
    valid_type = ['default', 'horse', 'cheat']
    
    def __init__(self, type, position):
        if type not in self.valid_type:
            raise ValueError(f"Invalid type: {type}");
        
        if type == 'default':
            super().__init__(1, position, 5);
        elif type == 'horse':
            super().__init__(2, position, 5);
        elif type == 'cheat':
            super().__init__(7, position, 5);
            
        self.inventory = resources.Resource();
        
    def set_interact(self, structure):
        self.task.put(commands.Interact(self, structure));
        
    def set_give_all(self, structure):
        self.task.put(commands.GiveAll(self, structure));
        
    def is_full(self):
        return self.inventory.amount == 5;
        
    def is_go_to_base(self):
        if self.is_busy():
            return False;
        
        if self.inventory.type == None:
            return False;
        
        return True;  
    
    def can_go_through(self, tile):
        if tile.structure:
            return False;
        return True;