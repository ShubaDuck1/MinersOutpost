import resources;
import render;
from commands import normalize;

class Structure:
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
        self.current_health -= enemy.damage;
        if self.current_health <= 0:
            self.is_destroyed = True;
            
            if self.tile.structure:
                self.tile.remove_structure();
            
    def can_build(self, tile):
        pass;
        
class Constructor(Structure):
    def __init__(self, structure):
        super().__init__(1);
        self.structure = structure;
        self.inventory = self.set_inventory();
        self.is_interactable = True;
        self.renderer = render.ConstructorRenderer(self);
        
    def set_inventory(self):
        res = [];
        
        if self.structure == 'road':
            res.append(resources.Resource('stone', 1));
        elif self.structure == 'bridge':
            res.append(resources.Resource('wood', 10));
            res.append(resources.Resource('stone', 10));
        elif type(self.structure) == Spike:
            res.append(resources.Resource('wood', 15));
        elif type(self.structure) == Crossbow:
            res.append(resources.Resource('wood', 30));
            res.append(resources.Resource('stone', 10));
        
        return res;
        
    def check(self):
        for resource in self.inventory:
            if resource.amount != 0:
                return False;
        
        self.update();
        return True;
        
    def update(self):
        if self.structure == 'road' or self.structure == 'bridge':
            self.tile.type = 'road';
            self.tile.structure = None;
        else:
            self.tile.remove_structure();
            self.tile.set_structure(self.structure);
    
class Tree(Structure):
    def __init__(self):
        super().__init__(20);
        self.progress = 0;
        self.is_harvestable = True;
        
        self.renderer = render.TreeRenderer(self);
        
    def harvest(self, miner, delta_time):
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
    def __init__(self):
        super().__init__(50);
        self.progress = 0;
        self.is_harvestable = True;
        
        self.renderer = render.StoneRenderer(self);
        
    def harvest(self, miner, delta_time):
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
    def __init__(self):
        super().__init__(1000);
        self.inventory = [resources.Resource() for _ in range(5)];
        self.vision_range = 10;
        self.is_interactable = True;
        self.renderer = render.BaseRenderer(self);
    
class Spike(Structure):
    def __init__(self):
        super().__init__(200);
        self.damage = 5;
        self.renderer = render.SpikeRenderer(self);
        
    def take_damage(self, enemy):
        super().take_damage(enemy);
        enemy.take_damage(self);
        
    def can_build(self, tile):
        if tile.type == 'water':
            return False;
        if tile.structure:
            return False;
        return True;
        
class Crossbow(Structure):
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
        enemy.take_damage(self);
    
    def update(self, delta_time):
        if self.cooldown == 10:
            self.cooldown = 0;
            
        self.cooldown += delta_time;
        
        if self.cooldown >= 1 and self.target:
            self.cooldown = 0;
            self.attack(self.target);
            
        