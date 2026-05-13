import settings;
import math;

def magnitude(vector: tuple[int, int]):
    '''
    Hàm tính toàn độ lớn của vector.
    
    Args:
        vector (tuple[int, int]): tuple chứa tọa độ của vector.
        
    Returns:
        float: độ lớn của vector.
    '''
    
    return math.hypot(vector[0], vector[1]);
            
def normalize(vector: tuple[int, int]):
    '''
    Hàm chuẩn hóa vector.
    
    Args:
        vector (tuple[int, int]): tuple chứa tọa độ vector.
        
    Returns:
        tuple[int, int]: vector sau khi đã được chuẩn hóa.
    '''
    
    mag = magnitude(vector);
    if not mag:
        mag = 0.1;
    
    return round(vector[0] / mag, 1), round(vector[1] / mag, 1);

class Command:
    '''
    Lớp các nhiệm vụ của đàn kiến.
    
    Đây là một lớp mẫu để cài đặt các nhiệm vụ của đàn kiến.
    
    Các đối tượng nhiệm vụ sẽ được bỏ vào một hàng đợi và lần lượt thực hiện mỗi frame.
    
    Các lớp kế thừa từ lớp này sẽ gồm có các hàm và tham số của lớp này:
        
    Attributes:
        unit (units): đối tượng kiến được giao nhiệm vụ.
        is_done (bool): giá trị boolean thể hiện sự hoàn thành của nhiệm vụ. 
    '''
    
    def __init__(self, unit):
        '''
        Khởi tạo nhiệm vụ.
        '''
        
        self.unit = unit;
        self.is_done = False;
    
    def execute(self):
        '''
        Hàm thực hiện nhiệm vụ.
        
        Khi thực hiện xong sẽ đặt lại giá trị is_done là True.
        '''
        
        raise NotImplementedError();
    
SPEED_SCALAR = settings.TILE_SIZE * 2;
    
class Move(Command):
    '''
    Nhiệm vụ di chuyển của đối tượng kiến.
    
    Attributes:
        destination (tuple[int, int]): tuple chứa tọa độ điểm cần di chuyển đến.
    '''
    
    def __init__(self, unit, destination):
        super().__init__(unit);
        self.destination = destination;
        
    def execute(self, delta_time):
        '''
        Di chuyển đối tượng đến vị trí được khởi tạo.
        
        Args:
            delta_time (float): delta time của trò chơi được đưa vào để tính độ dịch chuyển của vật.
        '''
        
        dest_x, dest_y = self.destination;
        dest_x = (dest_x + 0.5) * settings.TILE_SIZE;
        dest_y = (dest_y + 0.5) * settings.TILE_SIZE;
        
        dir_x, dir_y = normalize((dest_x - self.unit.position[0], dest_y - self.unit.position[1]));
        self.unit.direction = (dir_x, dir_y);
        
        self.unit.position = (self.unit.position[0] + dir_x * self.unit.modified_speed * SPEED_SCALAR * delta_time, 
                              self.unit.position[1] + dir_y * self.unit.modified_speed * SPEED_SCALAR * delta_time);
        
        mag = magnitude((dest_x - self.unit.position[0], 
                         dest_y - self.unit.position[1]));
        
        if mag <= 2:
            self.is_done = True;
            
class Attack(Command):
    '''
    Nhiệm vụ tấn công.
    
    Nhiệm vụ này sẽ tấn công một ô cho đến khi ô đó có thể đi qua được.
    
    Lớp này chỉ được sử dụng với những con kiến kẻ địch.
    
    Attributes:
        tile (tiles.Tile): Ô trò chơi trên lưới mà cần tấn công.
        destination (tuple[int, int]): tọa độ của ô cần tấn công.
    '''
    
    def __init__(self, enemy, tile, destination):
        super().__init__(enemy);
        self.tile = tile;
        self.progress = 0;
        self.destination = destination;
    
    def check(self):
        return self.unit.can_go_through(self.tile);
    
    def execute(self, delta_time):
        dest_x, dest_y = self.destination;
        dest_x = (dest_x + 0.5) * settings.TILE_SIZE;
        dest_y = (dest_y + 0.5) * settings.TILE_SIZE;
        
        dir_x, dir_y = normalize((dest_x - self.unit.position[0], dest_y - self.unit.position[1]));
        self.unit.direction = (dir_x, dir_y);
        
        if self.check():
            self.is_done = True;
            return;
        
        self.progress += delta_time;
        if self.progress >= 1:
            self.progress = 0;
            self.tile.structure.take_damage(self.unit);        

class Harvest(Command):
    '''
    Nhiệm vụ thu hoạch
    
    Sẽ được giao cho đàn kiến để đi thu hoạch tài nguyên.
    
    Attributes:
        structure (Tree | Stone): đối tượng tài nguyên.
        destination (tuple[int, int]): tọa độ ô chứa tài nguyên.
    '''
    
    def __init__(self, miner, structure, destination):
        super().__init__(miner);
        self.structure = structure;
        self.destination = destination;
        
    def execute(self, delta_time):
        dest_x, dest_y = self.destination;
        dest_x = (dest_x + 0.5) * settings.TILE_SIZE;
        dest_y = (dest_y + 0.5) * settings.TILE_SIZE;
        
        dir_x, dir_y = normalize((dest_x - self.unit.position[0], dest_y - self.unit.position[1]));
        self.unit.direction = (dir_x, dir_y);
        
        tmp = self.structure.harvest(self.unit, delta_time);
        if tmp:
            self.unit.just_get_resource = tmp;
        
        if self.structure.is_destroyed or self.unit.is_full():
            self.is_done = True;
            self.structure.is_occupied = False;
            
class GiveAll(Command):
    '''
    Nhiệm vụ đưa hết tài nguyên vào tổ.
    
    Nhiệm vụ sẽ lấy hết tài nguyên trong người đối tượng kiến và đưa vào kho đồ của tổ.
    
    Attributes:
        miner (Miner): đối tượng kiến.
        structure (Base): đối tượng tổ kiến.
    '''
    
    def __init__(self, miner, structure):
        super().__init__(miner);
        self.structure = structure;
        
    def execute(self, delta_time):
        for resource in self.structure.inventory:
            type = self.unit.inventory.type;
            amount = self.unit.inventory.amount;
            if resource.add(type, amount):
                self.unit.inventory.remove(type, amount);
                break;
        self.is_done = True;
        
class TakeResource(Command):
    '''
        Nhiệm vụ lấy tài nguyên từ tổ.
        
        Nhiệm vụ này sẽ đưa một con kiến đến tổ đến lấy tài nguyên đi xây thành.

        Attributes:
            miner (Miner): đối tượng kiến.
            structure (Base): đối tượng tổ kiến.
            type (string): loại tài nguyên.
            amount (int): số lượng tài nguyên.
    '''
    
    def __init__(self, miner, structure, type, amount):
        super().__init__(miner);
        self.structure = structure;
        self.type = type;
        self.amount = amount;
        
    def execute(self, delta_time):
        type = self.type;
        amount = self.amount;
        
        for resource in self.structure.inventory:
            if resource.remove(type, amount, False):
                self.unit.inventory.add(type, amount);
                break;
        self.is_done = True;
        
class GiveResource(Command):
    '''
    Nhiệm vụ đưa vài nguyên vào ô xây dựng để xây dựng thành.
    
    Attributes:
        miner (Miner): đối tượng kiến.
        structure (Constructor): công trình dùng để xây dựng thành.
    '''
    
    def __init__(self, miner, structure):
        super().__init__(miner);
        self.structure = structure;
        
    def execute(self, delta_time):
        for resource in self.structure.inventory:
            type = self.unit.inventory.type;
            amount = min(self.unit.inventory.amount, resource.amount);
            if resource.remove(type, amount):
                self.unit.inventory.remove(type, amount);
                break;
        self.is_done = True;
        self.structure.is_occupied = False;