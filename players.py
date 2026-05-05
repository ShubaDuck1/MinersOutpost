import structures
import tiles;
import math;
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
        
    def find_path_harvest(self, space):
        found_path = False;
        visited = [None for _ in range(tiles.TILE_WIDTH * tiles.TILE_HEIGHT)];
        path = [];
        que = queue.PriorityQueue();
        
        for miner in space.space_miners:
            if miner.is_busy():
                continue;
            
            curr_x, curr_y = tiles.pixel_to_tile(miner.position);
            que.put((0, curr_x, curr_y))
            visited[curr_y * tiles.TILE_WIDTH + curr_x] = (curr_x, curr_y, miner);
        
        while not que.empty():
            cost, curr_x, curr_y = que.get();
            curr_miner = visited[curr_y * tiles.TILE_WIDTH + curr_x][2];
            
            for x, y in tiles.Tile.diagonal:
                new_x = curr_x + x;
                new_y = curr_y + y;
                
                if not (0 <= new_x < tiles.TILE_WIDTH):
                    continue;
                
                if not (0 <= new_y < tiles.TILE_HEIGHT):
                    continue;
                
                curr_tile = space.grid[new_y][new_x];
                if not curr_miner.can_go_through(curr_tile):
                    continue;
                
                if not visited[new_y * tiles.TILE_WIDTH + new_x]:
                    que.put((cost + math.sqrt(2) / (curr_tile.modify_speed() * curr_miner.speed), new_x, new_y));
                    visited[new_y * tiles.TILE_WIDTH + new_x] = (curr_x, curr_y, curr_miner);
            
            for x, y in tiles.Tile.adjacent:
                new_x = curr_x + x;
                new_y = curr_y + y;
                
                if not (0 <= new_x < tiles.TILE_WIDTH):
                    continue;
                
                if not (0 <= new_y < tiles.TILE_HEIGHT):
                    continue;
                
                curr_tile = space.grid[new_y][new_x];
                curr_task = curr_tile.structure;
                
                if self.top <= new_y <= self.bottom and self.left <= new_x <= self.right:
                    if curr_task and curr_task.is_harvestable and not curr_task.is_occupied:
                        found_path = True;
                        break;
                
                if not curr_miner.can_go_through(curr_tile):
                    continue;
                
                if not visited[new_y * tiles.TILE_WIDTH + new_x]:
                    que.put((cost + 1 / (curr_tile.modify_speed() * curr_miner.speed), new_x, new_y));
                    visited[new_y * tiles.TILE_WIDTH + new_x] = (curr_x, curr_y, curr_miner);
            
            if found_path:
                break;
        
        if not found_path:
            return None;
        
        path.append((curr_x, curr_y))
        while not (curr_x, curr_y, curr_miner) == visited[curr_y * tiles.TILE_WIDTH + curr_x]:
            curr_x, curr_y, curr_miner = visited[curr_y * tiles.TILE_WIDTH + curr_x];
            path.append((curr_x, curr_y));
        
        path.reverse();        
        return curr_miner, path, new_x, new_y;
        
    def check(self, space):
        for x in range(self.left, self.right + 1):
            for y in range(self.top, self.bottom + 1):
                task = space.grid[y][x].structure;
                if task and task.is_harvestable and not task.is_occupied:
                    return False;
        return True;
        
    def execute(self, space):
        # cnt = space.count_not_busy();
        # if not cnt:
        #     return;
        
        if self.check(space):
            return;
        
        tmp = self.find_path_harvest(space);
        
        if not tmp:
            self.is_done = True;
            return;
            
        miner, path, dest_x, dest_y = tmp;
        curr_task = space.grid[dest_y][dest_x].structure;
        curr_task.is_occupied = True;
        miner.set_path(path);
        miner.set_harvest(curr_task);

class Build(PlayerCommand):
    def __init__(self, position, structure):
        super().__init__();
        self.position = position;
        self.structure = structure;
        
    def get_resource(self, space):
        type = None;
        amount = 0;
        
        for i in self.structure.inventory:
            if not i.amount:
                continue;
            
            for j in space.base.inventory:
                if j.type != i.type:
                    continue;
                
                type = j.type;
                amount = min(i.amount, j.amount);
        
        return type, amount;
        
    def find_path(self, space, base_position):
        found_path = False;
        visited = [None for _ in range(tiles.TILE_WIDTH * tiles.TILE_HEIGHT)];
        path = [];
        que = queue.PriorityQueue();
        
        for miner in space.space_miners:
            if miner.is_busy():
                continue;
            
            curr_x, curr_y = tiles.pixel_to_tile(miner.position);
            que.put((0, curr_x, curr_y))
            visited[curr_y * tiles.TILE_WIDTH + curr_x] = (curr_x, curr_y, miner);
        
        while not que.empty():
            cost, curr_x, curr_y = que.get();
            curr_miner = visited[curr_y * tiles.TILE_WIDTH + curr_x][2];
            
            for x, y in tiles.Tile.diagonal:
                new_x = curr_x + x;
                new_y = curr_y + y;
                
                if not (0 <= new_x < tiles.TILE_WIDTH):
                    continue;
                
                if not (0 <= new_y < tiles.TILE_HEIGHT):
                    continue;
                
                curr_tile = space.grid[new_y][new_x];
                if not curr_miner.can_go_through(curr_tile):
                    continue;
                
                if not visited[new_y * tiles.TILE_WIDTH + new_x]:
                    que.put((cost + math.sqrt(2) / (curr_tile.modify_speed() * curr_miner.speed), new_x, new_y));
                    visited[new_y * tiles.TILE_WIDTH + new_x] = (curr_x, curr_y, curr_miner);
            
            for x, y in tiles.Tile.adjacent:
                new_x = curr_x + x;
                new_y = curr_y + y;
                
                if not (0 <= new_x < tiles.TILE_WIDTH):
                    continue;
                
                if not (0 <= new_y < tiles.TILE_HEIGHT):
                    continue;
                
                curr_tile = space.grid[new_y][new_x];
                curr_task = curr_tile.structure;
                
                if (new_x, new_y) == base_position:
                    if curr_task and curr_task.is_interactable and not curr_task.is_occupied:
                        found_path = True;
                        break;
                
                if not curr_miner.can_go_through(curr_tile):
                    continue;
                
                if not visited[new_y * tiles.TILE_WIDTH + new_x]:
                    que.put((cost + 1 / (curr_tile.modify_speed() * curr_miner.speed), new_x, new_y));
                    visited[new_y * tiles.TILE_WIDTH + new_x] = (curr_x, curr_y, curr_miner);
            
            if found_path:
                break;
        
        if not found_path:
            return None;
        
        path.append((curr_x, curr_y))
        while not (curr_x, curr_y, curr_miner) == visited[curr_y * tiles.TILE_WIDTH + curr_x]:
            curr_x, curr_y, curr_miner = visited[curr_y * tiles.TILE_WIDTH + curr_x];
            path.append((curr_x, curr_y));
        
        path.reverse();        
        return curr_miner, path;
        
    def execute(self, space):
        curr_x, curr_y = self.position;
        curr_task = space.grid[curr_y][curr_x].structure;
        
        if not curr_task or self.structure.check():
            self.is_done = True;
            return;
            
        # cnt = space.count_not_busy();
        # if not cnt:
        #     return;
    
        if curr_task.is_occupied:
            return;
        
        type, amount = self.get_resource(space);
        if not amount:
            return;
        
        miner, path = self.find_path(space, space.base_position);
        amount = min(amount, miner.full);
        miner.set_path(path);
        miner.set_take_resource(space.base, type, amount);
        
        path = space.find_path(miner, path[-1], self.position);
        miner.set_path(path);
        miner.set_give_resource(curr_task);
        curr_task.is_occupied = True;
        
class Explore(PlayerCommand):
    def execute(self):
        return super().execute()

class PlayerAction:
    def __init__(self, space):
        self.task = [];
        self.space = space;
    
    def add_harvest(self, top, left, bottom, right):
        self.task.append(Harvest(top, left, bottom, right));
        
    def add_road(self, position):
        curr_tile = self.space.grid[position[1]][position[0]];
        if curr_tile.structure or curr_tile.type == 'road':
            return;
        
        curr_tile.structure = structures.Constructor('road');
        self.task.append(Build(position, curr_tile.structure));
        
    def add_spike(self, position):
        curr_tile = self.space.grid[position[1]][position[0]];
        if curr_tile.structure:
            return;
        
        curr_tile.structure = structures.Constructor(structures.Spike());
        self.task.append(Build(position, curr_tile.structure));
        
    def add_crossbow(self, position):
        curr_tile = self.space.grid[position[1]][position[0]];
        if curr_tile.structure:
            return;
        
        curr_tile.structure = structures.Constructor(structures.Crossbow());
        self.task.append(Build(position, curr_tile.structure));
        
    def update(self):
        for curr_task in self.task:
            cnt = self.space.count_not_busy();
            if not cnt:
                break;
            
            curr_task.execute(self.space);
            if curr_task.is_done:
                self.task.remove(curr_task);