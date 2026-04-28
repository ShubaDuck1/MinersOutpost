import units;
import pygame;
import tiles
import queue;

class Space:
    def __init__(self, grid):
        self.space_miners = [];
        self.grid = grid;
    
    def add(self, miner: units.Unit):
        self.space_miners.append(miner);
        
    def step(self, delta_time):
        for miner in self.space_miners:
            miner.update(delta_time);
            
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.grid[y][x].update();
            
    def count_not_busy(self):
        cnt = 0;
        for miner in self.space_miners:
            if not miner.is_busy():
                cnt += 1;
        
        return cnt;
            
    def find_path_miner(self, destination):
        curr_tile = self.grid[destination[1]][destination[0]];
        if not curr_tile.is_interactable():
            return False;
        
        found_path = False;
        visited = [None for _ in range(tiles.TILE_WIDTH * tiles.TILE_HEIGHT)];
        path = [];
        que = queue.Queue();
        
        for miner in self.space_miners:
            if miner.is_busy():
                continue;
            
            curr_x, curr_y = tiles.pixel_to_tile(miner.position);
            que.put((curr_x, curr_y, miner))
            visited[curr_y * tiles.TILE_WIDTH + curr_x] = (curr_x, curr_y);
        
        if que.empty():
            return;
        
        while not que.empty():
            curr_x, curr_y, curr_miner = que.get();
            
            for x, y in tiles.Tile.adjacent:
                new_x = curr_x + x;
                new_y = curr_y + y;
                
                if not (0 <= new_x < tiles.TILE_WIDTH):
                    continue;
                
                if not (0 <= new_y < tiles.TILE_HEIGHT):
                    continue;
                
                if (new_x, new_y) == destination:
                    found_path = True;
                    break;
                
                curr_structure = self.grid[new_y][new_x].structure;
                if not curr_miner.can_go_through(curr_structure):
                    continue;
                
                if not visited[new_y * tiles.TILE_WIDTH + new_x]:
                    que.put((new_x, new_y, curr_miner));
                    visited[new_y * tiles.TILE_WIDTH + new_x] = (curr_x, curr_y);
            
            if found_path:
                break;
        
        if not found_path:
            return False;
        
        path.append((curr_x, curr_y))
        while not (curr_x, curr_y) == visited[curr_y * tiles.TILE_WIDTH + curr_x]:
            curr_x, curr_y = visited[curr_y * tiles.TILE_WIDTH + curr_x];
            path.append((curr_x, curr_y));
        
        path.reverse();
        curr_miner.set_path(path);
        curr_miner.set_task(curr_tile.structure);
        
        return True;
            
    def draw_space(self, screen: pygame.Surface):
        for miner in self.space_miners:
            pygame.draw.circle(screen, pygame.Color('red'), miner.position, miner.radius);