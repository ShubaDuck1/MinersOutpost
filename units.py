import queue;
import resources;
import commands;
import structures;
import render;

class Unit:
    '''
    Lớp đối tượng kiến.
    
    Attributes:
        speed (int): tốc độ gốc.
        modified_speed (float): tốc độ sau khi được nhân với hệ số của ô.
        position (tuple[float, float]): vị tri hiện tại của đối tượng.
        radius (int): bán kính kiến.
        direction (tuple[int, int]): hướng đối tượng đang nhìn.
    '''
    
    def __init__(self, speed, position, radius):
        self.speed = speed;
        self.modified_speed = speed;
        self.position = position;
        self.radius = radius;
        self.task = queue.Queue();
        self.direction = (0, -1);
        
    def is_busy(self):
        '''
        Hàm kiểm tra sự bận rộn của đối tượng này.
        
        Returns:
            bool: trả về True nếu đang có công việc.
        '''
        
        return not self.task.empty();
    
    def can_go_through(self, tile):
        '''
        Kiểm tra xem đối tượng có đi qua được ô này không.
        
        Args:
            tile (Tile): ô cần kiểm tra.
            
        Returns:
            bool: True nếu đi qua được.
        '''
        
        pass;
    
    def clear_task(self):
        '''
        Hàm bỏ hết công việc của đối tượng này.
        '''
        
        while not self.task.empty():
            curr_task = self.task.get();
            if type(curr_task) in (commands.Harvest, commands.GiveResource):
                curr_task.structure.is_occupied = False;
    
    def set_path(self, path):
        '''
        Hàm đặt đường đi cho đối tượng.
        
        Args:
            path (list[tuple[int, int]]): danh sách điếm trên đường đi.
        '''
        
        for destination in path:
            self.task.put(commands.Move(self, destination));
    
    def update(self, delta_time):
        '''
        Cập nhật trạng thái của đối tượng.
        
        Args:
            delta_time (float): delta time;
        '''
        
        if not self.task.empty():
            curr_task = self.task.queue[0];
            curr_task.execute(delta_time);
            
            if curr_task.is_done:
                self.task.get();
        
class Miner(Unit):
    '''
    Lớp kiến đồng minh.
    
    Attributes:
        valid_type (list[string]): danh sách các loại kiến hợp lệ.
        type (string): loại kiến.
        vision_range (int): khoảng cách tầm nhìn của kiến.
        inventory (Resource): túi đồ của kiến.
        just_get_resource (Resource | None): tài nguyên kiến vừa thu hoạch được.
        full (int): giới hạn số lượng tài nguyên có thể có trong túi đồ.
        renderer (MinerRenderer): xử lí đồ họa.
    '''
    
    valid_type = ['default']
    
    def __init__(self, type, position):
        if type not in self.valid_type:
            raise ValueError(f"Invalid type: {type}");
        
        if type == 'default':
            super().__init__(1, position, 5);
        
        self.type = type;
        self.vision_range = 3;
        self.inventory = resources.Resource();
        self.just_get_resource = None;
        self.full = 5;
        self.renderer = render.MinerRenderer(self);
        
    def set_harvest(self, structure, destination):
        '''
        Đặt nhiệm vụ thu hoạch cho đối tượng.
        
        Args:
            structure (Structure): công trình thu hoạch.
            destination (tuple[int, int]) vị trí thu hoạch.
        '''
        
        self.task.put(commands.Harvest(self, structure, destination));
        
    def set_give_all(self, structure):
        '''
        Đặt nhiệm vụ đưa tài nguyên vào tổ.
        
        Args:
            structure (Base): tổ kiến
        '''
        self.task.put(commands.GiveAll(self, structure));
        
    def set_take_resource(self, structure, type, amount):
        '''
        Đặt nhiệm vụ lấy tài nguyên đi xây dựng.
        
        Args:
            structure (Base): tổ kiến.
            type (string): loại tài nguyên.
            amount (int): số lượng tài nguyên.
        '''
        self.task.put(commands.TakeResource(self, structure, type, amount));
        
    def set_give_resource(self, structure):
        '''
        Đặt đưa tài nguyên cho công trình xây dựng.
        
        Args:
            structure (Constructor): công trình xây dựng
        '''
        self.task.put(commands.GiveResource(self, structure));
        
    def is_full(self):
        '''
        Kiểm tra xem túi đồ kiếm có đầy chưa:
        
        Returns:
            bool: True nếu đã đầy.
        '''
        
        return self.inventory.amount == self.full;
        
    def is_go_to_base(self):
        '''
        Kiểm tra xem kiến có nên đi về tổ không.
        
        Returns:
            bool: True nếu nên đi về tổ.
        '''
        
        if self.is_busy():
            return False;
        
        if self.inventory.type == None:
            return False;
        
        return True;  
    
    def can_go_through(self, tile):
        
        if self.type == 'default':
            if tile.structure and type(tile.structure) in (structures.Spike, structures.Constructor):
                return True;
            if not tile.structure:
                return True;
            return False;
            
        elif self.type == 'horse':
            if tile.type == 'road':
                return True;
            return False;
    
class Enemy(Unit):
    '''
    Lớp kiến kẻ thù.
    
    Attributes:
        max_health (int): máu tối đa.
        current_health(int): máu hiện tại.
        damage (int): sát thương.
        is_destroyed (bool): True nếu kiến kẻ địch đã bị tấn công chết.
        renderer (EnemyRenderer): xử lí đồ họa.
    '''
    
    def __init__(self, position, max_health):
        super().__init__(1, position, 5);
        self.max_health = max_health;
        self.current_health = self.max_health;
        self.damage = 10;
        self.is_destroyed = False;
        self.renderer = render.EnemyRenderer(self);
        
    def take_damage(self, structure):
        '''
        Hàm nhận sát thương từ thành.
        
        Args:
            structure (Structure): thành đang tấn công.
        '''
        
        self.current_health -= structure.damage;
        if self.current_health <= 0:
            self.is_destroyed = True;
        
    def set_attack_base(self, space, path):
        '''
        Đặt nhiệm vụ tấn công tổ kiến.
        
        Args:
            space (Space): không gian trò chơi.
            path (list[tuple[int, int]]): danh sách tọa độ đường đi.
        '''
        
        for x, y in path:
            self.task.put(commands.Attack(self, space.grid[y][x], (x, y)));
            self.task.put(commands.Move(self, (x, y)));
        self.task.put(commands.Attack(self, space.grid[space.base_position[1]][space.base_position[0]], space.base_position));
        
    def can_go_through(self, tile):
        
        if not tile.structure:
            return True;
        return False;