import resources;
import render;

class Structure:
    '''
    Lớp công trình dùng để cài đặt các công trình trong trò chơi như thành, tài nguyên và tổ kiến.
    
    Attributes:
        max_health (int): máu tối đa.
        current_health (int): máu hiện tại.
        is_destroyed (bool): trả về True nếu công trình bị phá hủy.
        is_interactable (bool): trả về True nếu có thể bị tương tác.
        is_harvestable (bool): trả về True nếu công trình có thể được khai thác.
        is_occupied (bool): trả về True nếu công trình đang được sử dụng.
        tile (Tile): đối tượng ô trò chơi đang chứa côn trình.
    '''
    
    def __init__(self, max_health):
        self.max_health = max_health;
        self.current_health = max_health;
        self.is_destroyed = False;
        self.is_interactable = False;
        self.is_harvestable = False;
        self.is_attackable = False;
        self.is_occupied = False;
        self.tile = None;
        
    def take_damage(self, enemy):
        '''
        Hàm nhận sát thương từ kẻ địch.
        
        Args:
            enemy (Enemy): kiến kẻ địch
        '''
        
        self.current_health -= enemy.damage;
        if self.current_health <= 0:
            self.is_destroyed = True;
            
            if self.tile.structure:
                self.tile.remove_structure();
            
    def can_build(self, tile):
        '''
        Hàm kiểm tra công trình có thể xây được tại ô này không.
        
        Args:
            tile (Tile): ô cần kiểm tra.
            
        Returns:
            bool: True nếu xây được.
        '''
        
        pass;
        
class Constructor(Structure):
    '''
    Lớp công trình xây dựng.
    
    Đối tượng này dùng để xây dựng nên các thành.
    
    Attributes:
        structure (Structure): công trình sẽ được xây dựng.
        inventory (list[Resource]): danh sách các tài nguyên cần thiết để xây công trình.
        renderer (ConstructorRenderer): xử lí đồ họa.
    '''
    
    def __init__(self, structure):
        super().__init__(1);
        self.structure = structure;
        self.inventory = self.set_inventory();
        self.is_interactable = True;
        self.renderer = render.ConstructorRenderer(self);
        
    def set_inventory(self):
        '''
        Hàm đặt tài nguyên cần thiết để xây dựng công trình.
        
        Returns:
            list[Resource]: danh sách tài nguyên.
        '''
        
        res = [];
        
        if self.structure == 'road':
            res.append(resources.Resource('stone', 1));
        elif self.structure == 'bridge':
            res.append(resources.Resource('wood', 10));
            res.append(resources.Resource('stone', 10));
        elif type(self.structure) == Spike:
            res.append(resources.Resource('wood', 15));
        elif type(self.structure) == Crossbow:
            res.append(resources.Resource('wood', 20));
            res.append(resources.Resource('stone', 30));
        
        return res;
        
    def check(self):
        '''
        Kiểm tra sự hoàn thành của công trình.
        
        Returns:
            bool: trả về True nếu công trình được xây dựng xong.
        '''
        
        for resource in self.inventory:
            if resource.amount != 0:
                return False;
        
        self.update();
        return True;
        
    def update(self):
        '''
        Cập nhật trạng thái của ô trò chơi với công trình được xây.
        '''
        
        if self.structure == 'road' or self.structure == 'bridge':
            self.tile.type = 'road';
            self.tile.structure = None;
        else:
            self.tile.remove_structure();
            self.tile.set_structure(self.structure);
    
class Tree(Structure):
    '''
    Lớp cây.
    
    Attributes:
        progress (float): trạng thái khai thác của cây.
        renderer (TreeRenderer): xử lí đồ họa.
    '''
    
    def __init__(self):
        super().__init__(20);
        self.progress = 0;
        self.is_harvestable = True;
        
        self.renderer = render.TreeRenderer(self);
        
    def harvest(self, miner, delta_time):
        '''
        Xử lí khai thác cây.
        
        Args:
            miner (Miner): đối tượng kiến đang khai thác cây.
            delta_time (float): delta time.
        '''
        
        self.progress += delta_time;
        
        if self.progress >= 5:
            self.progress = 0;
            self.current_health -= 1;
            miner.inventory.add('wood');
            return resources.Resource('wood', 1);
        
        if self.current_health <= 0:
            self.is_destroyed = True;
            self.tile.remove_structure();
            
class Stone(Structure):
    '''
    Lớp đá.
    
    Attributes:
        progress (float): trạng thái khai thác của đá.
        renderer (StoneRenderer): xử lí đồ họa.
    '''
    
    def __init__(self):
        super().__init__(50);
        self.progress = 0;
        self.is_harvestable = True;
        
        self.renderer = render.StoneRenderer(self);
        
    def harvest(self, miner, delta_time):
        '''
        Xử lí khai thác đá.
        
        Args:
            miner (Miner): đối tượng kiến đang khai thác đá.
            delta_time (float): delta time.
        '''
        
        self.progress += delta_time;
        
        if self.progress >= 10:
            self.progress = 0;
            self.current_health -= 1;
            miner.inventory.add('stone');
            return resources.Resource('stone', 1);
        
        if self.current_health <= 0:
            self.is_destroyed = True;
            self.tile.remove_structure();

class Base(Structure):
    '''
    Lớp tổ kiến.
    
    Attributes:
        inventory (list[Resource]): danh sách tài nguyên có trong tổ.
        vision_range (int): bán kính tầm nhìn của tổ.
        renderer (BaseRenderer): xử lí đồ họa.
    '''
    
    def __init__(self):
        super().__init__(1000);
        self.inventory = [resources.Resource() for _ in range(5)];
        self.vision_range = 10;
        self.is_interactable = True;
        self.renderer = render.BaseRenderer(self);
    
class Spike(Structure):
    '''
    Lớp cọc gỗ.
    
    Attributes:
        damage (int): sát thương của cọc.
        renderer (SpikeRenderer): xử lí đồ họa.
    '''
    
    def __init__(self):
        super().__init__(200);
        self.damage = 5;
        self.renderer = render.SpikeRenderer(self);
        
    def take_damage(self, enemy):
        '''
        Nhận sát thương từ kẻ địch.
        
        Sau khi nhận sát thương thì gây lại sát thương đến kẻ địch
        
        Args
            enemy (Enemy): kẻ địch.
        '''
        
        super().take_damage(enemy);
        enemy.take_damage(self);
        
    def can_build(self, tile):
        if tile.type == 'water':
            return False;
        if tile.structure:
            return False;
        return True;
        
class Crossbow(Structure):
    '''
    Lớp nỏ.
    
    Attributes:
        cooldown (float): thời gian hồi của nỏ.
        vision_range (int): độ rộng tầm nhìn của nỏ.
        damage (int): sát thương của nỏ.
        renderer (CrossbowRenderer): xử lí đồ họa.
        target (Enemy): mục tiêu nhắm đến.
    '''
    
    def __init__(self):
        super().__init__(30);
        self.is_attackable = True;
        self.cooldown = 10;
        self.vision_range = 6;
        self.damage = 20;
        self.renderer = render.CrossbowRenderer(self);
        self.target = None;
        
    def can_build(self, tile):
        if tile.type == 'water':
            return False;
        if tile.structure:
            return False;
        return True;
        
    def attack(self, enemy):
        '''
        Hàm tấn công kẻ địch.
        
        Args:
            enemy (Enemy): kẻ địch.
        '''
        
        enemy.take_damage(self);
    
    def update(self, delta_time):
        '''
        Cập nhật trạng thái của nỏ.
        
        Args:
            delta_time (float): delta time.
        '''
        
        if self.cooldown == 10:
            self.cooldown = 0;
            
        self.cooldown += delta_time;
        
        if self.cooldown >= 1 and self.target:
            self.cooldown = 0;
            self.attack(self.target);
            
        