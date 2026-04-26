import units;
import pygame;
import tiles
import queue;

class Space:
    def __init__(self):
        self.space_object = [];
        self.object_position = [[] for a in range(tiles.TILE_WIDTH * tiles.TILE_HEIGHT)];
    
    def add(self, miner: units.Unit):
        self.space_object.append(miner);
        x, y = tiles.pixel_to_tile(miner.position);
        self.object_position[y * tiles.TILE_WIDTH + x].append(miner);
        
    def step(self, delta_time):
        for miner in self.space_object:
            miner.update(delta_time);
            
    def find_path(self, grid, destination):
        visited = [None for a in range(tiles.TILE_WIDTH * tiles.TILE_HEIGHT)];
        path = [];
        que = queue.Queue();
        que.put(destination)
        visited[destination[1] * tiles.TILE_WIDTH + destination[0]] = destination;
        
        while not que.empty():
            curr_x, curr_y = que.get();
            curr_tile = self.object_position[curr_y * tiles.TILE_WIDTH + curr_x];
            
            if curr_tile and not curr_tile[-1].is_busy():
                break;
            
            for x, y in tiles.Tile.adjacent:
                new_x = curr_x + x;
                new_y = curr_y + y;
                
                if not (0 <= new_x < tiles.TILE_WIDTH):
                    continue;
                
                if not (0 <= new_y < tiles.TILE_HEIGHT):
                    continue;
                
                if visited[new_y * tiles.TILE_WIDTH + new_x] == None:
                    que.put((new_x, new_y));
                    visited[new_y * tiles.TILE_WIDTH + new_x] = (curr_x, curr_y);
        
        path.append((curr_x, curr_y))
        while not (curr_x, curr_y) == visited[curr_y * tiles.TILE_WIDTH + curr_x]:
            curr_x, curr_y = visited[curr_y * tiles.TILE_WIDTH + curr_x];
            path.append((curr_x, curr_y));
        
        if curr_tile:
            curr_tile[-1].set_path(path);
            self.object_position[destination[1] * tiles.TILE_WIDTH + destination[0]].append(curr_tile[-1]);
            curr_tile.pop()
            print(path);
            
            
    def draw_space(self, screen: pygame.Surface):
        for miner in self.space_object:
            pygame.draw.circle(screen, pygame.Color('red'), miner.position, miner.radius);