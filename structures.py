import pygame;
import settings;
import resources;

class Structure:
    def __init__(self, max_health):
        self.max_health = max_health;
        self.current_health = max_health;
        self.is_destroyed = False;
        self.is_interactable = False;
        self.is_harvestable = False;
        self.is_attackable = False;
        self.is_occupied = False;
        
    def take_damage(self, enemy):
        self.current_health -= enemy.damage;
        if self.current_health <= 0:
            self.is_destroyed = True;
            
    def can_build(self, tile):
        pass;
            
    def update(self, delta_time):
        pass;
    
    def draw(self, screen, position):
        pass;
        
class Constructor(Structure):
    def __init__(self, structure):
        super().__init__(1);
        self.structure = structure;
        self.inventory = self.set_inventory();
        self.is_interactable = True;
        
    def set_inventory(self):
        res = [];
        
        if self.structure == 'road':
            res.append(resources.Resource('stone', 1));
        elif type(self.structure) == Spike:
            res.append(resources.Resource('wood', 10));
        elif type(self.structure) == Crossbow:
            res.append(resources.Resource('wood', 20));
            res.append(resources.Resource('stone', 10));
        
        return res;
        
    def check(self):
        for resource in self.inventory:
            if resource.amount != 0:
                return False;
        return True;
        
    def update(self, tile):
        if self.structure == 'road':
            tile.type = 'road';
            tile.structure = None;
        else:
            tile.structure = self.structure;
            
    def draw(self, screen, position):
        x, y = position;
        g = pygame.Rect(x * settings.TILE_SIZE + 1, y * settings.TILE_SIZE + 1, settings.TILE_SIZE - 2, settings.TILE_SIZE - 2);
        pygame.draw.rect(screen, pygame.Color('orange'), g)
    
class Tree(Structure):
    def __init__(self):
        super().__init__(50);
        self.progress = 0;
        self.is_harvestable = True;
        
    def draw(self, screen, position):
        x = (position[0] + 0.5) * settings.TILE_SIZE;
        y = (position[1] + 0.5) * settings.TILE_SIZE;
        pygame.draw.circle(screen, pygame.Color('darkgreen'), (x, y), settings.TILE_SIZE // 2);
        
    def harvest(self, miner, delta_time):
        self.progress += delta_time;
        
        if self.progress >= 1:
            self.progress -= 1;
            self.current_health -= 1;
            miner.inventory.add('wood');
        
        if self.current_health <= 0:
            self.is_destroyed = True;
            
class Stone(Structure):
    def __init__(self):
        super().__init__(50);
        self.progress = 0;
        self.is_harvestable = True;
        
    def draw(self, screen, position):
        x = (position[0] + 0.5) * settings.TILE_SIZE;
        y = (position[1] + 0.5) * settings.TILE_SIZE;
        pygame.draw.circle(screen, pygame.Color('grey'), (x, y), settings.TILE_SIZE // 2);
        
    def harvest(self, miner, delta_time):
        self.progress += delta_time;
        
        if self.progress >= 1:
            self.progress -= 1;
            self.current_health -= 1;
            miner.inventory.add('stone');
        
        if self.current_health <= 0:
            self.is_destroyed = True;

class Base(Structure):
    def __init__(self):
        super().__init__(1000);
        self.inventory = [resources.Resource() for _ in range(5)];
        self.vision_range = 10;
        self.is_interactable = True;
        
    def draw(self, screen, position):
        x = (position[0] + 0.5) * settings.TILE_SIZE;
        y = (position[1] + 0.5) * settings.TILE_SIZE;
        pygame.draw.circle(screen, pygame.Color('blue'), (x, y), settings.TILE_SIZE // 2);
        
class Bridge(Structure):
    def __init__(self):
        super().__init__(10);
        
    def draw(self, screen, position):
        x = position[0];
        y = position[1];
        g = pygame.Rect(x * settings.TILE_SIZE, y * settings.TILE_SIZE, settings.TILE_SIZE, settings.TILE_SIZE);
        pygame.draw.rect(screen, pygame.Color('darkgrey'), g);
    
class Spike(Structure):
    def __init__(self):
        super().__init__(200);
        self.damage = 5;
        
    def take_damage(self, enemy):
        super().take_damage(enemy);
        enemy.take_damage(self);
        
    def can_build(self, tile):
        if tile.type == 'water':
            return False;
        if tile.structure:
            return False;
        return True;
        
    def draw(self, screen, position):
        x, y = position;
        g = pygame.Rect(x * settings.TILE_SIZE + 1, y * settings.TILE_SIZE + 1, settings.TILE_SIZE - 2, settings.TILE_SIZE - 2);
        pygame.draw.rect(screen, pygame.Color('brown'), g)
        
class Crossbow(Structure):
    def __init__(self):
        super().__init__(30);
        self.is_attackable = True;
        self.cooldown = 10;
        self.vision_range = 6;
        self.damage = 20;
        
    def can_build(self, tile):
        if tile.structure:
            return False;
        if not tile.type == 'grass':
            return False;
        return True;
        
    def attack(self, enemy):
        self.cooldown = 0;
        enemy.take_damage(self);
        
    def ready_to_attack(self, delta_time):
        self.cooldown += delta_time;
        
        return self.cooldown >= 1;
        
    def draw(self, screen, position):
        radius = (self.vision_range + 0.5) * settings.TILE_SIZE;
        temp_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        
        x = (position[0] + 0.5) * settings.TILE_SIZE;
        y = (position[1] + 0.5) * settings.TILE_SIZE;
        pygame.draw.circle(screen, pygame.Color('purple'), (x, y), settings.TILE_SIZE // 2);
        pygame.draw.circle(temp_surface, (255, 0, 0, 50), (radius, radius), radius);
        screen.blit(temp_surface, (x - radius, y - radius))