import structures
import resources;

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
        
    def check(self, space):
        for x in range(self.left, self.right + 1):
            for y in range(self.top, self.bottom + 1):
                task = space.grid[y][x].structure;
                if task and not task.is_occupied:
                    return False;
        return True;
        
    def execute(self, space):
        cnt = space.count_not_busy();
        if not cnt:
            return;
        
        if self.check(space):
            return;
        
        tmp = space.find_path_range(self.top, self.left, self.bottom, self.right);
        
        if not tmp:
            self.is_done = True;
            return;
            
        miner, path, dest_x, dest_y = tmp;
        curr_task = space.grid[dest_y][dest_x].structure;
        curr_task.is_occupied = True;
        miner.set_path(path);
        miner.set_interact(curr_task);

class BuildRoad(PlayerCommand):
    def __init__(self, position):
        super().__init__();
        self.position = position;
        self.road = structures.ConstructRoad();
        
    def get_resource(self, space):
        res = resources.Resource();
        for i in self.road.inventory:
            if not i.amount:
                continue;
            
            for j in space.base.inventory:
                if j.type != i.type:
                    continue;
                
                res.type = j.type;
                res.amount = min(i.amount, j.amount);
        
        return res;
        
    def execute(self, space):
        curr_x, curr_y = self.position;
        curr_task = space.grid[curr_y][curr_x].structure;
        
        if self.road.check():
            self.is_done = True;
            return;
        
        if not curr_task:
            space.grid[curr_y][curr_x].structure = self.road;
            curr_task = self.road;
            
        cnt = space.count_not_busy();
        if not cnt:
            return;
    
        if curr_task.is_occupied:
            return;
        
        base_x, base_y = space.base_position;
        tmp = space.find_path_range(base_y, base_x, base_y, base_x);
        
        if not tmp:
            return;
        
        resource = self.get_resource(space);
        
        if not resource.amount:
            return;
        
        miner, path, dest_x, dest_y = tmp;
        miner.set_path(path);
        miner.set_take_resource(space.base, resource);
        
        path = space.find_path(miner, path[-1], self.position);
        miner.set_path(path);
        miner.set_give_resource(curr_task);
        curr_task.is_occupied = True;

class PlayerAction:
    def __init__(self, space):
        self.task = [];
        self.space = space;
    
    def add_harvest(self, top, left, bottom, right):
        self.task.append(Harvest(top, left, bottom, right));
        
    def add_build_road(self, position):
        curr_tile = self.space.grid[position[1]][position[0]];
        if curr_tile.structure or curr_tile.type == 'road':
            return;
        self.task.append(BuildRoad(position));
        
    def update(self):
        for i in range(len(self.task)):
            curr_task = self.task[i];
            curr_task.execute(self.space);
            
        for i in range(len(self.task)):
            if curr_task.is_done:
                self.task.pop(i);
        
                