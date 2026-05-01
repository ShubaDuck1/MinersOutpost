import queue;

class PlayerCommand:
    def __init__(self):
        self.is_done = False;
    
    def execute(self):
        raise NotImplementedError("execute() Not Implemented");
    
class Harvest(PlayerCommand):
    def __init__(self, top, left, bottom, right):
        super().__init__();
        if top > bottom:
            top, bottom = bottom, top;
            
        if left > right:
            right, left = left, right;
        
        self.top = top;
        self.left = left;
        self.bottom = bottom;
        self.right = right;
        
    def execute(self, space):
        cnt = space.count_not_busy();
        i = 0;
        print(cnt);
        
        for i in range(cnt):
            tmp = space.find_harvest(self.top, self.left, self.bottom, self.right);
            
            if not tmp:
                self.is_done = True;
                break;
                
            miner, path, dest_x, dest_y = tmp;
            curr_task = space.grid[dest_y][dest_x].structure;
            miner.set_path(path);
            miner.set_interact(curr_task);

class PlayerAction:
    def __init__(self, space):
        self.task = queue.Queue();
        self.space = space;
    
    def add_harvest(self, top, left, bottom, right):
        self.task.put(Harvest(top, left, bottom, right));
        
    def update(self):
        if not self.task.empty():
            curr_task = self.task.queue[0];
            curr_task.execute(self.space);
            
            if curr_task.is_done:
                self.task.get();
        
                