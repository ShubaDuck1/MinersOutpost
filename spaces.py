import units;
import pygame;
import tiles;
import queue;
import math;
import structures;
import settings;
import random;

class Space:
    '''
    Lớp không gian trò chơi.
    
    Lớp này chứa dữ liệu của lưới bản đồ, các thành tấn công, kiến đồng mình và kiến kẻ địch
    
    Lớp này hoạt động như một lớp trung gian điều kiển các đối tượng trò chơi tương tác với nhau.
    Attributes:
        grid (list[list[Tile]]): Bản đồ trò chơi.
        space_miners (list[Miner]): danh sách chứa kiến đồng minh.
        space_enemies (list[Enemy]): danh sách chứa kiến kẻ địch.
        space_attack_tower (list[structure]): danh sách chứa các thành tấn công.
        water_time (float): đây là một giá trị để điều kiển chuyển động của nước.
        
        base_position (tuple[int, int]): vị trí của tổ.
        base (Base): đối tượng tổ kiến.
        day_counter (int): số đếm ngày đã trôi qua.
        is_night (bool): trạng thái ngày/đêm của trò chơi.
    '''
    
    def __init__(self, grid : list[list[tiles.Tile]], base_position):
        self.grid = grid;
        self.space_miners = [];
        self.space_enemies = [];
        self.space_attack_tower = [];
        self.water_time = 0;
        
        self.base_position = base_position;
        self.base = structures.Base();
        self.grid[base_position[1]][base_position[0]].set_structure(self.base);
        self.day_counter = 0;
        self.is_night = False;
        
        self.update_fog(((base_position[0] + 0.5) * settings.TILE_SIZE, (base_position[1] + 0.5) * settings.TILE_SIZE), self.base.vision_range);
        
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                grid[y][x].space = self;
    
    def add(self, unit: units.Unit):
        '''
        Thêm kiến đồng minh hoặc kiến kẻ địch vào không gian.
        
        Args:
            unit (Unit);
        '''
        
        if type(unit) == units.Miner:
            self.space_miners.append(unit);
        elif type(unit) == units.Enemy:
            self.space_enemies.append(unit);
        
    def step(self, delta_time):
        '''
        Di chuyển các đối tượng trong không gian thêm một bước theo delta_time.
        
        Args:
            delta_time (float): delta time.
        '''
        
        for miner in self.space_miners:
            if not miner.is_busy():
                continue;
            miner.update(delta_time);

        for enemy in self.space_enemies:
            if not enemy.is_busy():
                continue;
            enemy.update(delta_time);
    
        for curr_structure, x, y in self.space_attack_tower:
            curr_structure = self.grid[y][x].structure;
            if not curr_structure or not curr_structure.is_attackable:
                continue;
            
            enemy = self.find_enemy((x, y), curr_structure.vision_range);
            curr_structure.target = enemy;
            
            if curr_structure.cooldown == 10:
                self.update_fog(((x + 0.5) * settings.TILE_SIZE, (y + 0.5) * settings.TILE_SIZE), self.grid[y][x].structure.vision_range);
            
            curr_structure.update(delta_time);

    def update(self):
        '''
        Cập nhật trạng thái của các đối tượng trong không gian.
        '''
        
        for miner in self.space_miners:
            curr_x, curr_y = tiles.pixel_to_tile(miner.position);
            curr_tile = self.grid[curr_y][curr_x];
            miner.modified_speed = miner.speed * curr_tile.modify_speed();
            self.update_fog(miner.position, miner.vision_range);
            
            if miner.is_go_to_base():
                path = self.find_path(miner, tiles.pixel_to_tile(miner.position), self.base_position);
                if not path:
                    return;
                miner.set_path(path);
                miner.set_give_all(self.base);    
                
        for enemy in self.space_enemies:
            if enemy.is_destroyed: 
                self.space_enemies.remove(enemy);
                continue;
            curr_x, curr_y = tiles.pixel_to_tile(enemy.position);
            curr_tile = self.grid[curr_y][curr_x];
            enemy.modified_speed = enemy.speed * curr_tile.modify_speed();
                
        if not self.space_enemies and self.is_night:
            self.set_day_time();
        
    def count_not_busy(self):
        '''
        Đếm số lượng kiến đồng minh đang có nhiệm vụ đang xử lí.
        
        Returns:
            int: số lượng đếm được.
        '''
        
        cnt = 0;
        for miner in self.space_miners:
            if not miner.is_busy():
                cnt += 1;
        
        return cnt;
    
    def set_night_time(self):
        '''
        Đặt thời gian thành trời tối.
        '''
        
        self.is_night = True;
        for miner in self.space_miners:
            miner.clear_task();
            path = self.find_path(miner, tiles.pixel_to_tile(miner.position), self.base_position);
            if not path:
                continue;
            
            miner.set_path(path);
            miner.set_path([self.base_position]);
            if miner.inventory.amount:
                miner.set_give_all(self.base);
        
        enemy_amount = int(5 * pow(1.1, self.day_counter));
        enemy_hp = int(50 * pow(1.1, self.day_counter));
        spawn_tile = [];
        
        visited = [False for _ in range(settings.TILE_WIDTH * settings.TILE_HEIGHT)];
        que = queue.Queue();
        
        curr_x, curr_y = self.base_position;
        que.put((curr_x, curr_y))
        visited[curr_y * settings.TILE_WIDTH + curr_x] = True;
        
        while not que.empty():
            curr_x, curr_y = que.get();
            
            for x, y in tiles.Tile.adjacent:
                new_x = curr_x + x;
                new_y = curr_y + y;
                
                if not (0 <= new_x < settings.TILE_WIDTH):
                    continue;
                
                if not (0 <= new_y < settings.TILE_HEIGHT):
                    continue;
                
                if self.grid[new_y][new_x].is_foggy:
                    spawn_tile.append((new_x, new_y));
                    continue;

                if not visited[new_y * settings.TILE_WIDTH + new_x]:
                    que.put((new_x, new_y));
                    visited[new_y * settings.TILE_WIDTH + new_x] = True;
                    
        if not spawn_tile:
            return;
        
        while enemy_amount:
            enemy_amount -= 1;
            i = random.randint(0, len(spawn_tile) - 1);
            x, y = spawn_tile[i];
            
            if self.grid[y][x].structure:
                continue;

            enemy = units.Enemy(((x + 0.5) * settings.TILE_SIZE, (y + 0.5) * settings.TILE_SIZE), enemy_hp);
            self.add(enemy);
            path = self.find_path_enemy(enemy, (x, y), self.base_position);
            enemy.set_attack_base(self, path);
        
    def set_day_time(self):
        '''
        Đặt thời gian thành trời sáng.
        '''
        
        self.day_counter += 1;
        self.is_night = False;
    
    def find_enemy(self, position, _range):
        '''
        Tìm kiếm kẻ địch trong một khoảng hình tròn.
        
        Args:
            position (tuple[int, int]): vị trí.
            _range (int): bán kính của hình tròn để kiểm tra.
            
        Returns:
            None: nếu không tìm thấy.
            
            Enemy: kẻ địch tìm được.
        '''
        
        if not self.space_enemies:
            return;
        x, y = position;
        min_mag = math.inf;
        res_enemy = None;
        
        for enemy in self.space_enemies:
            curr_x, curr_y = enemy.position;
            mag = math.hypot((x + 0.5) * settings.TILE_SIZE - curr_x, 
                             (y + 0.5) * settings.TILE_SIZE - curr_y);
            
            if mag <= (_range + 0.5) * settings.TILE_SIZE and mag < min_mag:
                min_mag = mag;
                res_enemy = enemy;
            
        return res_enemy;
    
    def update_fog(self, position, _range):
        '''
        Cập nhật trạng thái sương mù trong một khoảng hình tròn.
        
        Args:
            position (tuple[int, int]): vị trí.
            _range (int): bán kính hình tròn.
        '''
        
        curr_x, curr_y = position;
        tmp_x, tmp_y = tiles.pixel_to_tile(position);
        
        for x in range(tmp_x - _range, tmp_x + _range + 1):
            if not 0 <= x < settings.TILE_WIDTH:
                continue;
            
            for y in range(tmp_y - _range, tmp_y + _range + 1):
                if not 0 <= y < settings.TILE_HEIGHT:
                    continue;
                
                mag = math.hypot((x + 0.5) * settings.TILE_SIZE - curr_x, 
                                (y + 0.5) * settings.TILE_SIZE - curr_y);
                
                if mag <= (_range + 0.5) * settings.TILE_SIZE:
                    self.grid[y][x].is_foggy = False;
                        
    def find_path(self, miner, position, destination):
        '''
        Tìm đường đi từ một vị trí đến vị trí khác của kiến đồng minh.
        
        Args:
            miner (Miner): đối tượng kiến đồng minh.
            position (tuple[int, int]): điểm khởi đầu.
            destination (tuple[int, int]): điểm đến.
            
        Returns:
            None: nếu không tìm được đường.
            
            list[tuple[int, int]]: danh sách tọa độ điểm trên đường.
        '''
        
        curr_tile = self.grid[destination[1]][destination[0]];
        if curr_tile.structure and not curr_tile.structure.is_interactable:
            return None;
        
        found_path = False;
        visited = [None for _ in range(settings.TILE_WIDTH * settings.TILE_HEIGHT)];
        path = [];
        que = queue.PriorityQueue();
        
        curr_x, curr_y = position;
        que.put((0, curr_x, curr_y))
        visited[curr_y * settings.TILE_WIDTH + curr_x] = (curr_x, curr_y);
        
        while not que.empty():
            cost, curr_x, curr_y= que.get();
            
            for x, y in tiles.Tile.diagonal:
                new_x = curr_x + x;
                new_y = curr_y + y;
                
                if not (0 <= new_x < settings.TILE_WIDTH):
                    continue;
                
                if not (0 <= new_y < settings.TILE_HEIGHT):
                    continue;
                
                curr_tile = self.grid[new_y][new_x];
                if not miner.can_go_through(curr_tile):
                    continue;
                
                if not visited[new_y * settings.TILE_WIDTH + new_x]:
                    que.put((cost + math.sqrt(2) / curr_tile.modify_speed(), new_x, new_y));
                    visited[new_y * settings.TILE_WIDTH + new_x] = (curr_x, curr_y);
            
            for x, y in tiles.Tile.adjacent:
                new_x = curr_x + x;
                new_y = curr_y + y;
                
                if not (0 <= new_x < settings.TILE_WIDTH):
                    continue;
                
                if not (0 <= new_y < settings.TILE_HEIGHT):
                    continue;
                
                if (new_x, new_y) == destination:
                    found_path = True;
                    break;
                
                curr_tile = self.grid[new_y][new_x];
                if not miner.can_go_through(curr_tile):
                    continue;
                
                if not visited[new_y * settings.TILE_WIDTH + new_x]:
                    que.put((cost + 1 / curr_tile.modify_speed(), new_x, new_y));
                    visited[new_y * settings.TILE_WIDTH + new_x] = (curr_x, curr_y);
            
            if found_path:
                break;
        
        if not found_path:
            return None;
        
        path.append((curr_x, curr_y))
        while not (curr_x, curr_y) == visited[curr_y * settings.TILE_WIDTH + curr_x]:
            curr_x, curr_y = visited[curr_y * settings.TILE_WIDTH + curr_x];
            path.append((curr_x, curr_y));
        
        path.reverse();
        return path;
    
    def find_path_enemy(self, enemy, position, destination):
        '''
        Tìm kiếm đường đi từ một điểm đến một điểm cho kiến kẻ địch.
        
        Args:
            enemy (Enemy): đối tượng kiến kẻ địch.
            position (tuple[int, int]): điểm khởi đầu.
            destination (tuple[int, int]): điểm đến.
            
        Returns:
            None: nếu không tìm được đường.
            
            list[tuple[int, int]]: danh sách tọa độ điểm trên đường.
            
        '''
        
        curr_tile = self.grid[destination[1]][destination[0]];
        if not curr_tile.structure.is_interactable:
            return None;
        
        found_path = False;
        visited = [None for _ in range(settings.TILE_WIDTH * settings.TILE_HEIGHT)];
        path = [];
        que = queue.PriorityQueue();
        
        curr_x, curr_y = position;
        que.put((0, curr_x, curr_y))
        visited[curr_y * settings.TILE_WIDTH + curr_x] = (curr_x, curr_y);
        
        while not que.empty():
            cost, curr_x, curr_y = que.get();
            
            for x, y in tiles.Tile.diagonal:
                new_x = curr_x + x;
                new_y = curr_y + y;
                
                if not (0 <= new_x < settings.TILE_WIDTH):
                    continue;
                
                if not (0 <= new_y < settings.TILE_HEIGHT):
                    continue;
                
                curr_tile = self.grid[new_y][new_x];
                attack_cost = 0;
                if not enemy.can_go_through(curr_tile):
                    if curr_tile.structure:
                        attack_cost = math.ceil(curr_tile.structure.current_health / enemy.damage);
                
                if not visited[new_y * settings.TILE_WIDTH + new_x]:
                    que.put((cost + attack_cost + math.sqrt(2) / curr_tile.modify_speed(), new_x, new_y));
                    visited[new_y * settings.TILE_WIDTH + new_x] = (curr_x, curr_y);
            
            for x, y in tiles.Tile.adjacent:
                new_x = curr_x + x;
                new_y = curr_y + y;
                
                if not (0 <= new_x < settings.TILE_WIDTH):
                    continue;
                
                if not (0 <= new_y < settings.TILE_HEIGHT):
                    continue;
                
                if (new_x, new_y) == destination:
                    found_path = True;
                    break;
                
                curr_tile = self.grid[new_y][new_x];
                attack_cost = 0;
                if not enemy.can_go_through(curr_tile):
                    if curr_tile.structure:
                        attack_cost = math.ceil(curr_tile.structure.current_health / enemy.damage);
                
                if not visited[new_y * settings.TILE_WIDTH + new_x]:
                    que.put((cost + attack_cost + 1 / curr_tile.modify_speed(), new_x, new_y));
                    visited[new_y * settings.TILE_WIDTH + new_x] = (curr_x, curr_y);
            
            if found_path:
                break;
        
        if not found_path:
            return None;
        
        path.append((curr_x, curr_y))
        while not (curr_x, curr_y) == visited[curr_y * settings.TILE_WIDTH + curr_x]:
            curr_x, curr_y = visited[curr_y * settings.TILE_WIDTH + curr_x];
            path.append((curr_x, curr_y));
        
        path.reverse();
        return path;
    
    def draw_all(self, screen, offset, delta_time):
        '''
        Vẽ toàn bộ đối tượng trong không gian.
        
        Args:
            screen (Surface): màn hình để vẽ lên.
            offset (tuple[int, int]): khoảng dịch đi của camera.
            delta_time (float): delta time.
        '''
        
        tmp_list = [];
        self.water_time += delta_time;
        
        for y in range(max(0, -3 - offset[1] // settings.TILE_SIZE), min(settings.TILE_HEIGHT, (settings.HEIGHT - offset[1]) // settings.TILE_SIZE + 3)):
            for x in range(max(0, -3 - offset[0] // settings.TILE_SIZE), min(settings.TILE_WIDTH, (settings.WIDTH - offset[0]) // settings.TILE_SIZE + 3)):
                curr_tile = self.grid[y][x];
                new_x = (x + 0.5) * settings.TILE_SIZE + offset[0];
                new_y = (y + 0.5) * settings.TILE_SIZE + offset[1]
                
                tmp_list.append((new_x, new_y, 5, curr_tile.renderer.fog, ((x, y), offset, delta_time)));
                if curr_tile.is_foggy:
                    continue;
                
                tmp_list.append((new_x, new_y, 1, curr_tile.renderer, ((x, y), offset, self.water_time)));
                
                if curr_tile.structure:
                    if type(curr_tile.structure) == structures.Constructor:
                        tmp_list.append((new_x, new_y, 2, curr_tile.structure.renderer, ((x, y), offset, delta_time)));
                    elif type(curr_tile.structure) == structures.Crossbow:
                        tmp_list.append((new_x, new_y, 3, curr_tile.structure.renderer, ((x, y), offset, delta_time)));
                        tmp_list.append((new_x, new_y, 4, curr_tile.structure.renderer.tracer, ((x, y), offset, delta_time)));
                    elif type(curr_tile.structure) == structures.Base:
                        tmp_list.append((new_x, new_y, 3, curr_tile.structure.renderer, ((x, y), offset, delta_time)));
                        tmp_list.append((new_x, new_y, 4, curr_tile.structure.renderer.health, ((x, y), offset, delta_time)));
                    else:
                        tmp_list.append((new_x, new_y, 3, curr_tile.structure.renderer, ((x, y), offset, delta_time)));
        
        for miner in self.space_miners:
            new_x = miner.position[0] + offset[0];
            new_y = miner.position[1] + offset[1];
            
            if not -3 * settings.TILE_SIZE <= new_x <= settings.WIDTH + 3 * settings.TILE_SIZE:
                continue;
            if not -3 * settings.TILE_SIZE <= new_y <= settings.HEIGHT + 3 * settings.TILE_SIZE:
                continue;
            
            if tiles.pixel_to_tile(miner.position) == self.base_position:
                continue;
            
            tmp_list.append((new_x, new_y, 3, miner.renderer, (offset, delta_time)));
            tmp_list.append((new_x, new_y, 4, miner.renderer.resource_ping, (offset, delta_time)));
            tmp_list.append((new_x, new_y, 4, miner.renderer.give_resource_ping, (self.base_position, offset, delta_time)));
            
        for enemy in self.space_enemies:
            new_x = enemy.position[0] + offset[0];
            new_y = enemy.position[1] + offset[1];
            
            if not -3 * settings.TILE_SIZE <= new_x <= settings.WIDTH + 3 * settings.TILE_SIZE:
                continue;
            if not -3 * settings.TILE_SIZE <= new_y <= settings.HEIGHT + 3 * settings.TILE_SIZE:
                continue;
            
            if tiles.pixel_to_tile(enemy.position) == self.base_position:
                continue;
            
            tmp_list.append((new_x, new_y, 3, enemy.renderer, (offset, delta_time)));  
            tmp_list.append((new_x, new_y, 4, enemy.renderer.health, (offset, delta_time)));  
            
        tmp_list.sort(key=lambda x: (x[2], x[1]));
        for obj in tmp_list:
            obj[3].draw(screen, *obj[4]);
            
        if self.is_night:
            self.draw_night(screen);
        
    def draw_night(self, screen):
        '''
        Vẽ trời tối.
        
        Args:
            screen (Surface): màn hình cần vẽ.
        '''
        
        temp_surface = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA);
        temp_surface.fill((0, 0, 0, 100));
        screen.blit(temp_surface, (0, 0));