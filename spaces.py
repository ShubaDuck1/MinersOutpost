import units;
import pygame;
import tiles;
import queue;
import math;
import structures;

class Space:
    def __init__(self, grid, base_position):
        self.grid = grid;
        self.space_miners = [];
        self.space_enemies = [];
        
        self.base_position = base_position;
        self.base = structures.Base();
        self.grid[base_position[1]][base_position[0]].set_structure(self.base);
        self.is_night = False;
        
        self.update_fog(((base_position[0] + 0.5) * tiles.TILE_SIZE, (base_position[1] + 0.5) * tiles.TILE_SIZE), self.base.vision_range);
    
    def add(self, unit: units.Unit):
        if type(unit) == units.Miner:
            self.space_miners.append(unit);
        elif type(unit) == units.Enemy:
            self.space_enemies.append(unit);
        
    def step(self, delta_time):
        for miner in self.space_miners:
            miner.update(delta_time);

        for enemy in self.space_enemies:
            enemy.update(delta_time);
            
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                curr_structure = self.grid[y][x].structure;
                if not curr_structure or not curr_structure.is_attackable:
                    continue;
                
                if curr_structure.cooldown == 10:
                    self.update_fog(((x + 0.5) * tiles.TILE_SIZE, (y + 0.5) * tiles.TILE_SIZE), self.grid[y][x].structure.vision_range);
                
                if not curr_structure.ready_to_attack(delta_time):
                    continue;
                
                enemy = self.find_enemy((x, y), curr_structure.vision_range);
                
                if not enemy:
                    continue;
                
                curr_structure.attack(enemy);
        
    def update(self):
        for miner in self.space_miners:
            curr_x, curr_y = tiles.pixel_to_tile(miner.position);
            curr_tile = self.grid[curr_y][curr_x];
            miner.modified_speed = miner.speed * curr_tile.modify_speed();
            self.update_fog(miner.position, miner.vision_range);
            
            if miner.is_go_to_base():
                path = self.find_path(miner, tiles.pixel_to_tile(miner.position), self.base_position);
                miner.set_path(path);
                miner.set_give_all(self.base);    
                
        for enemy in self.space_enemies:
            if enemy.is_destroyed: 
                self.space_enemies.remove(enemy);
                continue;
            curr_x, curr_y = tiles.pixel_to_tile(enemy.position);
            curr_tile = self.grid[curr_y][curr_x];
            enemy.modified_speed = enemy.speed * curr_tile.modify_speed();
            
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.grid[y][x].update();
        
    def count_not_busy(self):
        cnt = 0;
        for miner in self.space_miners:
            if not miner.is_busy():
                cnt += 1;
        
        return cnt;
    
    def find_enemy(self, position, _range):
        x, y = position;
        min_mag = math.inf;
        res_enemy = None;
        
        for enemy in self.space_enemies:
            curr_x, curr_y = enemy.position;
            mag = math.hypot((x + 0.5) * tiles.TILE_SIZE - curr_x, 
                             (y + 0.5) * tiles.TILE_SIZE - curr_y);
            
            if mag <= (_range + 0.5) * tiles.TILE_SIZE and mag < min_mag:
                min_mag = mag;
                res_enemy = enemy;
            
            return res_enemy;
    
    def update_fog(self, position, _range):
        curr_x, curr_y = position;
        tmp_x, tmp_y = tiles.pixel_to_tile(position);
        
        for x in range(tmp_x - _range, tmp_x + _range + 1):
            if not 0 <= x < tiles.TILE_WIDTH:
                continue;
            
            for y in range(tmp_y - _range, tmp_y + _range + 1):
                if not 0 <= y < tiles.TILE_HEIGHT:
                    continue;
                
                mag = math.hypot((x + 0.5) * tiles.TILE_SIZE - curr_x, 
                                (y + 0.5) * tiles.TILE_SIZE - curr_y);
                
                if mag <= (_range + 0.5) * tiles.TILE_SIZE:
                    self.grid[y][x].is_foggy = False;
                        
    def find_path(self, miner, position, destination):
        curr_tile = self.grid[destination[1]][destination[0]];
        if not curr_tile.structure.is_interactable:
            return None;
        
        found_path = False;
        visited = [None for _ in range(tiles.TILE_WIDTH * tiles.TILE_HEIGHT)];
        path = [];
        que = queue.PriorityQueue();
        
        curr_x, curr_y = position;
        que.put((0, curr_x, curr_y))
        visited[curr_y * tiles.TILE_WIDTH + curr_x] = (curr_x, curr_y);
        
        while not que.empty():
            cost, curr_x, curr_y= que.get();
            
            for x, y in tiles.Tile.diagonal:
                new_x = curr_x + x;
                new_y = curr_y + y;
                
                if not (0 <= new_x < tiles.TILE_WIDTH):
                    continue;
                
                if not (0 <= new_y < tiles.TILE_HEIGHT):
                    continue;
                
                curr_tile = self.grid[new_y][new_x];
                if not miner.can_go_through(curr_tile):
                    continue;
                
                if not visited[new_y * tiles.TILE_WIDTH + new_x]:
                    que.put((cost + math.sqrt(2) / curr_tile.modify_speed(), new_x, new_y));
                    visited[new_y * tiles.TILE_WIDTH + new_x] = (curr_x, curr_y);
            
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
                
                curr_tile = self.grid[new_y][new_x];
                if not miner.can_go_through(curr_tile):
                    continue;
                
                if not visited[new_y * tiles.TILE_WIDTH + new_x]:
                    que.put((cost + 1 / curr_tile.modify_speed(), new_x, new_y));
                    visited[new_y * tiles.TILE_WIDTH + new_x] = (curr_x, curr_y);
            
            if found_path:
                break;
        
        if not found_path:
            return None;
        
        path.append((curr_x, curr_y))
        while not (curr_x, curr_y) == visited[curr_y * tiles.TILE_WIDTH + curr_x]:
            curr_x, curr_y = visited[curr_y * tiles.TILE_WIDTH + curr_x];
            path.append((curr_x, curr_y));
        
        path.reverse();
        return path;
    
    def find_path_enemy(self, enemy, position, destination):
        curr_tile = self.grid[destination[1]][destination[0]];
        if not curr_tile.structure.is_interactable:
            return None;
        
        found_path = False;
        visited = [None for _ in range(tiles.TILE_WIDTH * tiles.TILE_HEIGHT)];
        path = [];
        que = queue.PriorityQueue();
        
        curr_x, curr_y = position;
        que.put((0, curr_x, curr_y))
        visited[curr_y * tiles.TILE_WIDTH + curr_x] = (curr_x, curr_y);
        
        while not que.empty():
            cost, curr_x, curr_y = que.get();
            
            for x, y in tiles.Tile.diagonal:
                new_x = curr_x + x;
                new_y = curr_y + y;
                
                if not (0 <= new_x < tiles.TILE_WIDTH):
                    continue;
                
                if not (0 <= new_y < tiles.TILE_HEIGHT):
                    continue;
                
                curr_tile = self.grid[new_y][new_x];
                attack_cost = 0;
                if not enemy.can_go_through(curr_tile):
                    if curr_tile.structure:
                        attack_cost = math.ceil(curr_tile.structure.current_health / enemy.damage);
                
                if not visited[new_y * tiles.TILE_WIDTH + new_x]:
                    que.put((cost + attack_cost + math.sqrt(2) / curr_tile.modify_speed(), new_x, new_y));
                    visited[new_y * tiles.TILE_WIDTH + new_x] = (curr_x, curr_y);
            
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
                
                curr_tile = self.grid[new_y][new_x];
                attack_cost = 0;
                if not enemy.can_go_through(curr_tile):
                    if curr_tile.structure:
                        attack_cost = math.ceil(curr_tile.structure.current_health / enemy.damage);
                
                if not visited[new_y * tiles.TILE_WIDTH + new_x]:
                    que.put((cost + attack_cost + 1 / curr_tile.modify_speed(), new_x, new_y));
                    visited[new_y * tiles.TILE_WIDTH + new_x] = (curr_x, curr_y);
            
            if found_path:
                break;
        
        if not found_path:
            return None;
        
        path.append((curr_x, curr_y))
        while not (curr_x, curr_y) == visited[curr_y * tiles.TILE_WIDTH + curr_x]:
            curr_x, curr_y = visited[curr_y * tiles.TILE_WIDTH + curr_x];
            path.append((curr_x, curr_y));
        
        path.reverse();
        return path;
                
    def draw_space(self, screen: pygame.Surface):
        for miner in self.space_miners:
            pygame.draw.circle(screen, pygame.Color('blue'), miner.position, miner.radius);
            
        for enemy in self.space_enemies:
            pygame.draw.circle(screen, pygame.Color('red'), enemy.position, enemy.radius);