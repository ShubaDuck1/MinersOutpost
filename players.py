import structures
import tiles;
import math;
import queue;
import settings;

class PlayerCommand:
    '''
    Lớp mẫu để cài đặt mệnh lệnh được người chơi đưa ra và giao nhiệm vụ cho đàn kiến.
    
    Attributes:
        is_done (bool): giá trị boolean thể hiện nhiệm vụ được hoàn thành.
    '''
    
    def __init__(self):
        self.is_done = False;
    
    def execute(self):
        '''
        Hàm thực hiện lệnh.
        '''
        
        raise NotImplementedError("execute() Not Implemented");
    
class Harvest(PlayerCommand):
    '''
    Mệnh lệnh thu hoạch.
    
    Mệnh lệnh này sẽ điều kiển đàn kiến đi thu hoạch trong một khoảng ô vuông trong các giá trị ``left``, ``top``, ``right``, ``bottom``.
    
    Attributes:
        left (int): tọa độ bên trái ô vuông.
        top (int): tọa độ bên trên ô vuông.
        right (int): tọa độ bên phải ô vuông.
        bottom (int): tọa độ bên dưới ô vuông.
    '''
    
    def __init__(self, left, top, right, bottom):
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
        '''
        Hàm tìm đường đi đến vùng cần thu hoạch.
        
        Args:
            space (Space): không gian trò chơi.
            
        Returns:
            None: nếu không tìm thấy.
            
            curr_miner (Miner): đối tượng kiến tìm được. 
            path (list[tuple[int, int]]): danh sách các tọa độ đường đi.
            new_x (int): tọa độ x của địa điểm đến.
            new_y (int): tọa độ y của địa điểm đến.
        '''
        
        found_path = False;
        visited = [None for _ in range(settings.TILE_WIDTH * settings.TILE_HEIGHT)];
        path = [];
        que = queue.PriorityQueue();
        
        for miner in space.space_miners:
            if miner.is_busy():
                continue;
            
            curr_x, curr_y = tiles.pixel_to_tile(miner.position);
            que.put((0, curr_x, curr_y))
            visited[curr_y * settings.TILE_WIDTH + curr_x] = (curr_x, curr_y, miner);
        
        while not que.empty():
            cost, curr_x, curr_y = que.get();
            curr_miner = visited[curr_y * settings.TILE_WIDTH + curr_x][2];
            
            for x, y in tiles.Tile.diagonal:
                new_x = curr_x + x;
                new_y = curr_y + y;
                
                if not (0 <= new_x < settings.TILE_WIDTH):
                    continue;
                
                if not (0 <= new_y < settings.TILE_HEIGHT):
                    continue;
                
                curr_tile = space.grid[new_y][new_x];
                if not curr_miner.can_go_through(curr_tile):
                    continue;
                
                if not visited[new_y * settings.TILE_WIDTH + new_x]:
                    que.put((cost + math.sqrt(2) / (curr_tile.modify_speed() * curr_miner.speed), new_x, new_y));
                    visited[new_y * settings.TILE_WIDTH + new_x] = (curr_x, curr_y, curr_miner);
            
            for x, y in tiles.Tile.adjacent:
                new_x = curr_x + x;
                new_y = curr_y + y;
                
                if not (0 <= new_x < settings.TILE_WIDTH):
                    continue;
                
                if not (0 <= new_y < settings.TILE_HEIGHT):
                    continue;
                
                curr_tile = space.grid[new_y][new_x];
                curr_task = curr_tile.structure;
                
                if self.top <= new_y <= self.bottom and self.left <= new_x <= self.right:
                    if curr_task and curr_task.is_harvestable and not curr_task.is_occupied:
                        found_path = True;
                        break;
                
                if not curr_miner.can_go_through(curr_tile):
                    continue;
                
                if not visited[new_y * settings.TILE_WIDTH + new_x]:
                    que.put((cost + 1 / (curr_tile.modify_speed() * curr_miner.speed), new_x, new_y));
                    visited[new_y * settings.TILE_WIDTH + new_x] = (curr_x, curr_y, curr_miner);
            
            if found_path:
                break;
        
        if not found_path:
            return None;
        
        path.append((curr_x, curr_y))
        while not (curr_x, curr_y, curr_miner) == visited[curr_y * settings.TILE_WIDTH + curr_x]:
            curr_x, curr_y, curr_miner = visited[curr_y * settings.TILE_WIDTH + curr_x];
            path.append((curr_x, curr_y));
        
        path.reverse();        
        return curr_miner, path, new_x, new_y;
        
    def check(self, space):
        cnt = 0;
        for x in range(self.left, self.right + 1):
            for y in range(self.top, self.bottom + 1):
                task = space.grid[y][x].structure;
                if task:
                    cnt += 1;
                    if task.is_harvestable and not task.is_occupied:
                        return False;
        if not cnt:
            self.is_done = True;
        return True;
        
    def execute(self, space):
        '''
        Hàm thực hiện mệnh lệnh.
        
        Args:
            space (Space): không gian trò chơi.
        '''
        
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
        miner.set_harvest(curr_task, (dest_x, dest_y));

class Build(PlayerCommand):
    '''
    Lệnh xây dựng thành.
    
    Attributes:
        position (tuple[int, int]): vị trí.
        structure (Constuctor): công trình xây dựng thành.
    '''
    
    def __init__(self, position, structure):
        super().__init__();
        self.position = position;
        self.structure = structure;
        
    def get_resource(self, space):
        '''
        Hàm tính toàn tài nguyên cần lấy từ tổ.
        
        Args:
            space (Space): không gian trò chơi.
            
        Returns:
            None: Nếu không có:
            
            type (string): loại tài nguyên.
            amount (int): số lượng tài nguyên.
        '''
        
        type = None;
        amount = 0;
        
        for i in self.structure.inventory:
            if not i.amount:
                continue;
            
            for j in space.base.inventory:
                if j.type != i.type:
                    continue;
                
                type = i.type;
                amount = min(i.amount, j.amount);
                
                if amount:
                    return type, amount;

        return None, 0;
        
    def find_path(self, space, base_position):
        '''
        Hàm tìm đường đi về tổ.
        
        Args:
            space (Space): không gian trò chơi.
            base_position (tuple[int, int]): vị trí của tổ.
            
        Returns:
            None: nếu không tìm thấy.
            
            curr_miner (Miner): đối tượng kiến.
            path (list[tuple[int, int]]): danh sách tọa độ đường đi.
        '''
        
        found_path = False;
        visited = [None for _ in range(settings.TILE_WIDTH * settings.TILE_HEIGHT)];
        path = [];
        que = queue.PriorityQueue();
        
        for miner in space.space_miners:
            if miner.is_busy():
                continue;
            
            curr_x, curr_y = tiles.pixel_to_tile(miner.position);
            que.put((0, curr_x, curr_y))
            visited[curr_y * settings.TILE_WIDTH + curr_x] = (curr_x, curr_y, miner);
        
        while not que.empty():
            cost, curr_x, curr_y = que.get();
            curr_miner = visited[curr_y * settings.TILE_WIDTH + curr_x][2];
            
            for x, y in tiles.Tile.diagonal:
                new_x = curr_x + x;
                new_y = curr_y + y;
                
                if not (0 <= new_x < settings.TILE_WIDTH):
                    continue;
                
                if not (0 <= new_y < settings.TILE_HEIGHT):
                    continue;
                
                curr_tile = space.grid[new_y][new_x];
                if not curr_miner.can_go_through(curr_tile):
                    continue;
                
                if not visited[new_y * settings.TILE_WIDTH + new_x]:
                    que.put((cost + math.sqrt(2) / (curr_tile.modify_speed() * curr_miner.speed), new_x, new_y));
                    visited[new_y * settings.TILE_WIDTH + new_x] = (curr_x, curr_y, curr_miner);
            
            for x, y in tiles.Tile.adjacent:
                new_x = curr_x + x;
                new_y = curr_y + y;
                
                if not (0 <= new_x < settings.TILE_WIDTH):
                    continue;
                
                if not (0 <= new_y < settings.TILE_HEIGHT):
                    continue;
                
                curr_tile = space.grid[new_y][new_x];
                curr_task = curr_tile.structure;
                
                if (new_x, new_y) == base_position:
                    if curr_task and curr_task.is_interactable and not curr_task.is_occupied:
                        found_path = True;
                        break;
                
                if not curr_miner.can_go_through(curr_tile):
                    continue;
                
                if not visited[new_y * settings.TILE_WIDTH + new_x]:
                    que.put((cost + 1 / (curr_tile.modify_speed() * curr_miner.speed), new_x, new_y));
                    visited[new_y * settings.TILE_WIDTH + new_x] = (curr_x, curr_y, curr_miner);
            
            if found_path:
                break;
        
        if not found_path:
            return None;
        
        path.append((curr_x, curr_y))
        while not (curr_x, curr_y, curr_miner) == visited[curr_y * settings.TILE_WIDTH + curr_x]:
            curr_x, curr_y, curr_miner = visited[curr_y * settings.TILE_WIDTH + curr_x];
            path.append((curr_x, curr_y));
        
        path.reverse();        
        return curr_miner, path;
        
    def execute(self, space):
        '''
        Hàm chạy lệnh.
        
        Args:
            space (Space): không gian trò chơi.
        '''
        
        curr_x, curr_y = self.position;
        curr_task = space.grid[curr_y][curr_x].structure;
        
        if not curr_task or self.structure.check():
            self.is_done = True;
            return;
    
        if curr_task.is_occupied:
            return;
        
        type, amount = self.get_resource(space);
        if not amount:
            return;
        
        tmp = self.find_path(space, space.base_position);
        if not tmp:
            return;
        
        miner, path = tmp;
        amount = min(amount, miner.full);
        miner.set_path(path);
        miner.set_take_resource(space.base, type, amount);
        
        path = space.find_path(miner, path[-1], self.position);
        if not path:
            return;
        
        miner.set_path(path);
        miner.set_give_resource(curr_task);
        curr_task.is_occupied = True;

class PlayerAction:
    '''
    Lớp xử lí các lệnh được người chơi đưa ra.
    
    Lớp này được dùng để xử lí các đối tượng ``PlayerCommand``.
    
    Attributes:
        task (PriorityQueue): hàng đợi ưu tiên chứa các lệnh thực hiện.
        space (Space): không gian trò chơi.
        counter (int): giá trị đếm số lượng lệnh hiện tại. Dùng để đánh dấu lệnh nào được đưa ra trước.
    '''
    
    def __init__(self, space):
        self.task = queue.PriorityQueue();
        self.space = space;
        self.counter = 0;
    
    def add_harvest(self, top, left, bottom, right):
        '''
        Hàm thêm lệnh thu hoạch
        
        Args:
            left (int): tọa độ bên trái ô vuông.
            top (int): tọa độ bên trên ô vuông.
            right (int): tọa độ bên phải ô vuông.
            bottom (int): tọa độ bên dưới ô vuông.
        '''
        
        self.task.put((2, self.counter, Harvest(top, left, bottom, right)));
        self.counter += 1;
        
    def add_road(self, position):
        '''
        Hàm thêm lệnh xây đường đi.
        
        Args:
            position (tuple[int, int]): vị trí cần xây.
        '''
        
        curr_tile = self.space.grid[position[1]][position[0]];
        if curr_tile.structure or curr_tile.type == 'water':
            return;
        
        curr_tile.set_structure(structures.Constructor('road'));
        self.task.put((1, self.counter, Build(position, curr_tile.structure)));
        self.counter += 1;
        
    def add_bridge(self, position):
        '''
        Hàm thêm lệnh xây cầu.
        
        Args:
            position (tuple[int, int]): vị trí cần xây.
        '''
        
        curr_tile = self.space.grid[position[1]][position[0]];
        if curr_tile.structure or not curr_tile.type == 'water':
            return;
        
        curr_tile.set_structure(structures.Constructor('bridge'));
        self.task.put((1, self.counter, Build(position, curr_tile.structure)));
        self.counter += 1;
        
    def add_spike(self, position):
        '''
        Hàm thêm lệnh xây cọc gỗ.
        
        Args:
            position (tuple[int, int]): vị trí cần xây.
        '''
        
        curr_tile = self.space.grid[position[1]][position[0]];
        struc = structures.Spike();
        if not struc.can_build(curr_tile):
            return;
        
        curr_tile.set_structure(structures.Constructor(struc));
        self.task.put((1, self.counter, Build(position, curr_tile.structure)));
        self.counter += 1;
        
    def add_crossbow(self, position):
        '''
        Hàm thêm lệnh xây nỏ.
        
        Args:
            position (tuple[int, int]): vị trí cần xây.
        '''
        
        curr_tile = self.space.grid[position[1]][position[0]];
        struc = structures.Crossbow();
        if not struc.can_build(curr_tile):
            return;
        
        curr_tile.set_structure(structures.Constructor(struc));
        self.task.put((1, self.counter, Build(position, curr_tile.structure)));
        self.counter += 1;
        
    def update(self):
        '''
        Hàm cập nhật vào thực hiện lệnh trong hàng đợi ưu tiên.
        '''
        
        tmp = [];
        last = self.space.count_not_busy();
        while not self.task.empty():
            cnt = self.space.count_not_busy();
            if not cnt or last - cnt > 2:
                break;
            
            prio, counter, curr_task = self.task.get();
            
            curr_task.execute(self.space);
            if not curr_task.is_done:
                tmp.append((prio, counter, curr_task));
        
        for x in tmp:
            self.task.put(x);