import pygame;
import load;
import settings;
import random;
import commands;
import pygame;

def angle(v1, v2):
    tmp = pygame.math.Vector2(v1);
    return tmp.angle_to(v2);

assets = {};
def load_assets():
    global assets;
    
    assets['font18'] = pygame.font.Font(load.path('asset/font/Minecraft.ttf'), 18);
    assets['font25'] = pygame.font.Font(load.path('asset/font/Minecraft.ttf'), 25);
    assets['font40'] = pygame.font.Font(load.path('asset/font/Minecraft.ttf'), 40);
    assets['font80'] = pygame.font.Font(load.path('asset/font/Minecraft.ttf'), 80);
    assets['font150'] = pygame.font.Font(load.path('asset/font/Minecraft.ttf'), 150);
    assets['cursor.png'] = pygame.image.load(load.path('asset/sprites/UI/cursor.png')).convert_alpha();
    assets['button_box.png'] = pygame.image.load(load.path('asset/sprites/UI/button_box.png')).convert_alpha();
    assets['options_icons.png'] = load_sprite_sheet(pygame.image.load(load.path('asset/sprites/UI/options_icons.png')).convert_alpha(), 16, 16);
    assets['grass.png'] = pygame.image.load(load.path('asset/sprites/tiles/grass-block.png')).convert_alpha();
    assets['water.png'] = load_sprite_sheet(pygame.image.load(load.path('asset/sprites/tiles/water.png')).convert_alpha(), 16, 16);
    assets['sand.png'] = pygame.image.load(load.path('asset/sprites/tiles/sand.png')).convert_alpha();
    assets['road.png'] = pygame.image.load(load.path('asset/sprites/tiles/road.png')).convert_alpha();
    assets['tree.png'] = pygame.image.load(load.path('asset/sprites/structures/tree.png')).convert_alpha();
    assets['stone.png'] = pygame.image.load(load.path('asset/sprites/structures/stone.png')).convert_alpha();
    assets['constructor.png'] = pygame.image.load(load.path('asset/sprites/structures/constructor.png')).convert_alpha();
    assets['spike.png'] = pygame.image.load(load.path('asset/sprites/structures/spike.png')).convert_alpha();
    assets['miner.png'] = load_sprite_sheet(pygame.image.load(load.path('asset/sprites/units/blue_ant.png')).convert_alpha(), 48, 48);
    assets['enemy.png'] = load_sprite_sheet(pygame.image.load(load.path('asset/sprites/units/red_ant.png')).convert_alpha(), 48, 48);
    

def load_sprite_sheet(sheet: pygame.Surface, width : int, height: int):
    sheet_width, sheet_height = sheet.get_size();
    res = []
    
    for y in range(0, sheet_height, height):
        for x in range(0, sheet_width, width):
            rect = pygame.Rect(x, y, width, height);
            tmp = sheet.subsurface(rect);
            res.append(tmp);
            
    return res;

class Renderer:
    def __init__(self):
        raise NotImplementedError();
    
    def draw(self):
        raise NotImplementedError();
    
class ButtonRenderer(Renderer):
    def __init__(self, button):
        self.button = button;
        
        self.g = pygame.Rect(button.left, button.top, button.width, button.height);
        font = assets['font25'];
        self.text_surface = font.render(f"{self.button.name}", True, pygame.Color('white'));
        self.text_rect = self.text_surface.get_rect(center = (self.g.center[0], self.g.center[1] + 2));
    
        self.temp_surface = pygame.Surface((button.width, button.height), pygame.SRCALPHA);
        self.temp_surface.fill((0, 0, 0, 25));
    
    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color('grey'), self.g);
        
        screen.blit(self.text_surface, self.text_rect);
        
        if self.button.is_pressed:
            screen.blit(self.temp_surface, self.g);
            
class PlayButtonRenderer(Renderer):
    def __init__(self, play_button):
        self.play_button = play_button;
        self.box = pygame.transform.scale2x(assets['button_box.png']);
        
        if play_button.name == 'slow down':
            self.icon = pygame.transform.scale2x(assets['options_icons.png'][0]);
        elif play_button.name == 'default':
            self.icon = pygame.transform.scale2x(assets['options_icons.png'][1]);
        elif play_button.name == 'speed up':
            self.icon = pygame.transform.scale2x(assets['options_icons.png'][2]);
        elif play_button.name == 'options':
            self.icon = pygame.transform.scale2x(assets['options_icons.png'][3]);
        
    def draw(self, screen):
        g = pygame.Rect(self.play_button.left, self.play_button.top, self.play_button.width, self.play_button.height);
        temp_rect = self.box.get_rect(center = g.center);
        screen.blit(self.box, temp_rect);
        
        temp_rect = self.icon.get_rect(center = g.center);
        screen.blit(self.icon, temp_rect);
            
class TextBoxRenderer(Renderer):
    def __init__(self, box):
        self.text_box = box;
        
        self.g = pygame.Rect(box.left, box.top, box.width, box.height);
        self.font = assets['font25'];
        self.text_surface = self.font.render(f"{box.name}", True, pygame.Color('white'));
        self.text_rect = self.text_surface.get_rect(midleft = (box.left + 10, self.g.center[1] + 2));
        
        self.dot_surface = self.font.render(f"...", True, pygame.Color('white'));
        self.dot_rect = self.dot_surface.get_rect(midleft = self.text_rect.midright);
        
    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color("#766F6F"), self.g);
        pygame.draw.rect(screen, pygame.Color("#C6BBBB"), self.g, 5);
        
        if self.text_box.current_text != '':
            text_surface = self.font.render(f"{self.text_box.current_text}", True, pygame.Color('white'));
            screen.blit(text_surface, self.text_rect);
            return;

        screen.blit(self.text_surface, self.text_rect);
        
class MainMenuRenderer(Renderer):
    def __init__(self, main_menu):
        self.main_menu = main_menu;
        
        font = assets['font150'];
        self.text_surface = font.render(f"Minecraft", True, pygame.Color('white'));
        self.text_rect = self.text_surface.get_rect(center = (settings.WIDTH // 2, 220));
        
    def draw_background(self, screen):
        screen.fill(pygame.Color("#08d958"));
        screen.blit(self.text_surface, self.text_rect);
        
    def draw(self, screen):
        self.draw_background(screen);
        self.main_menu.play.renderer.draw(screen);
        self.main_menu.scoreboard.renderer.draw(screen);
        self.main_menu.exit.renderer.draw(screen);
        
class PauseMenuRenderer(Renderer):
    def __init__(self, pause_menu):
        self.pause_menu = pause_menu;
        
        self.temp_surface = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA);
        self.temp_surface.fill((0, 0, 0, 100));
        
    def draw_background(self, screen):
        screen.blit(self.temp_surface, (0, 0));
        
    def draw(self, screen):
        self.draw_background(screen);
        self.pause_menu.play.renderer.draw(screen);
        self.pause_menu.restart.renderer.draw(screen);
        self.pause_menu.exit.renderer.draw(screen);
    
class GameOverMenuRenderer(Renderer):
    def __init__(self, game_over_menu):
        self.game_over_menu = game_over_menu;
        self.font = assets['font80'];
        
        text_surface = self.font.render(f"Game Over", True, pygame.Color('white'));
        text_rect = text_surface.get_rect(center = (settings.WIDTH // 2, 200));
        
        self.temp_surface = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA);
        self.temp_surface.fill((0, 0, 0, 100));
        self.temp_surface.blit(text_surface, text_rect);
        
    def draw_background(self, screen):
        screen.blit(self.temp_surface, (0, 0));
        
    def draw(self, screen):
        self.draw_background(screen);
        self.game_over_menu.text_box.renderer.draw(screen);
        self.game_over_menu.restart.renderer.draw(screen);
        self.game_over_menu.scoreboard.renderer.draw(screen);
        self.game_over_menu.exit.renderer.draw(screen);
        
class PlayMenuRenderer(Renderer):
    def __init__(self, play_menu):
        self.play_menu = play_menu;
        
    def draw(self, screen):
        self.play_menu.slow_down.renderer.draw(screen);
        self.play_menu.default.renderer.draw(screen);
        self.play_menu.speed_up.renderer.draw(screen);
        self.play_menu.options.renderer.draw(screen);
        
class ScoreboardRenderer(Renderer):
    def __init__(self, scoreboard):
        self.scoreboard = scoreboard;
        self.start_line = 5;
        self.background_font = assets['font40'];
        self.font = pygame.font.Font(load.path('asset/font/Minecraft.ttf'), 25);
        
        self.text_surface = self.background_font.render(f"Scoreboard", True, pygame.Color('white'));
        self.text_rect = self.text_surface.get_rect(center = (settings.WIDTH // 2, 70));
        
    def draw_background(self, screen):
        screen.fill(pygame.Color("#08d958"));
        screen.blit(self.text_surface, self.text_rect);
        
    def draw(self, screen):
        self.draw_background(screen);
        self.scoreboard.back.renderer.draw(screen);
        
        width = self.scoreboard.board_width + 20;
        height = self.scoreboard.board_height;
        offset = 30;
        
        self.start_line = max(self.start_line, height - offset * (len(self.scoreboard.scores)));
        self.start_line = min(self.start_line, 5);
        curr_line = self.start_line;
        
        board_surface = pygame.Surface((width, height), pygame.SRCALPHA);
        board_rect = board_surface.get_rect(center = (settings.WIDTH // 2, settings.HEIGHT // 2));
        
        for data in self.scoreboard.scores:
            text_surface = self.font.render(f"{data['name']}", True, pygame.Color('white'));
            text_rect = text_surface.get_rect(topleft = (10, curr_line));
            board_surface.blit(text_surface, text_rect);
            
            text_surface = self.font.render(f"{int(data['score'] // 60):02d}:{int(data['score'] % 60):02d}", True, pygame.Color('white'));
            text_rect = text_surface.get_rect(topright = (width - 10, curr_line));
            board_surface.blit(text_surface, text_rect);
            
            curr_line += offset;
            if curr_line > height:
                break;
                
        for i in range(10):
            temp_surface = pygame.Surface((width, 1), pygame.SRCALPHA);
            temp_surface.fill((0, 0, 0, 100 - i * 10));
            board_surface.blit(temp_surface, (0, height - i));
        
        board_surface.blit(text_surface, text_rect);
                
        for i in range(10):
            temp_surface = pygame.Surface((width, 1), pygame.SRCALPHA);
            temp_surface.fill((0, 0, 0, 100 - i * 10));
            board_surface.blit(temp_surface, (0, i));


        screen.blit(board_surface, board_rect);
        
class CursorRenderer(Renderer):
    def __init__(self):
        self.image = pygame.transform.scale2x(assets['cursor.png']);

    def draw(self, screen):
        screen.blit(self.image, pygame.mouse.get_pos());
        
class TileRenderer(Renderer):
    def __init__(self, tile):
        self.tile = tile;
        self.fog = FogRenderer(self.tile);
        self.grass = None;
        self.water = None;
        self.sand = None;
        self.road = None;
        
    def draw(self, screen, position, offset, delta_time):
        if self.tile.is_foggy:
            self.fog.draw(screen, position, offset);
        
        elif self.tile.type == 'grass':
            if not self.grass:
                self.grass = GrassRenderer(self.tile);
            
            self.grass.draw(screen, position, offset, delta_time);
            
        elif self.tile.type == 'water':
            if not self.water:
                self.water = WaterRenderer(self.tile);
            
            self.water.draw(screen, position, offset, delta_time);
            
        elif self.tile.type == 'sand':
            if not self.sand:
                self.sand = SandRenderer(self.tile);
            
            self.sand.draw(screen, position, offset, delta_time);
            
        elif self.tile.type == 'road':
            if not self.road:
                self.road = RoadRenderer(self.tile);
            
            if self.grass:
                self.grass.draw(screen, position, offset, delta_time);
            elif not self.sand:
                self.sand = SandRenderer(self.tile);
            if self.sand:
                self.sand.draw(screen, position, offset, delta_time);
            
            self.road.draw(screen, position, offset, delta_time);
            
class FogRenderer(Renderer):
    def __init__(self, tile):
        self.tile = tile;
    
    def draw(self, screen, position, offset):
        x = position[0] * settings.TILE_SIZE + offset[0];
        y = position[1] * settings.TILE_SIZE + offset[1];
        
        g = pygame.Rect(x, y, settings.TILE_SIZE, settings.TILE_SIZE);
        pygame.draw.rect(screen, pygame.Color('grey'), g);
        
class GrassRenderer(Renderer):
    def __init__(self, tile):
        self.tile = tile;
        self.image = pygame.transform.scale2x(assets['grass.png']);
        
    def draw(self, screen, position, offset, delta_time):
        x = position[0] * settings.TILE_SIZE + offset[0];
        y = position[1] * settings.TILE_SIZE + offset[1];

        screen.blit(self.image, (x, y));
        
class WaterRenderer(Renderer):
    def __init__(self, tile):
        self.tile = tile;
        self.image = assets['water.png'];
        self.progress = random.random();
        
    def draw(self, screen, position, offset, delta_time):
        x = position[0] * settings.TILE_SIZE + offset[0];
        y = position[1] * settings.TILE_SIZE + offset[1];
        
        self.progress += delta_time * random.random();
        image = pygame.transform.scale2x(self.image[int(len(self.image) * self.progress) % len(self.image)]);
        screen.blit(image, (x, y));
        
class SandRenderer(Renderer):
    def __init__(self, tile):
        self.tile = tile;
        self.image = pygame.transform.scale2x(assets['sand.png']);
        
    def draw(self, screen, position, offset, delta_time):
        x = position[0] * settings.TILE_SIZE + offset[0];
        y = position[1] * settings.TILE_SIZE + offset[1];
        
        screen.blit(self.image,(x, y));
        
class RoadRenderer(Renderer):
    def __init__(self, tile):
        self.tile = tile;
        self.image = pygame.transform.scale2x(assets['road.png']);
        
    def draw(self, screen, position, offset, delta_time):
        x = (position[0] + 0.5) * settings.TILE_SIZE + offset[0];
        y = (position[1]+ 0.5) * settings.TILE_SIZE + offset[1];
        
        temp_rect = self.image.get_rect(center = (x, y))
        
        screen.blit(self.image, temp_rect);
        
class TreeRenderer(Renderer):
    def __init__(self, tree):
        self.tree = tree;
        self.image = pygame.transform.scale2x(assets['tree.png']);
        
    def draw(self, screen, position, offset, delta_time):
        x = (position[0] + 0.5) * settings.TILE_SIZE + offset[0];
        y = (position[1] + 0.5) * settings.TILE_SIZE - settings.TILE_SIZE + offset[1];
        
        image_rect = self.image.get_rect(center = (x, y));
        screen.blit(self.image, image_rect);
        
class StoneRenderer(Renderer):
    def __init__(self, stone):
        self.stone = stone;
        self.image = pygame.transform.scale2x(assets['stone.png']);
        
    def draw(self, screen, position, offset, delta_time):
        x = position[0] * settings.TILE_SIZE + offset[0];
        y = position[1] * settings.TILE_SIZE + offset[1];
        
        screen.blit(self.image, (x, y));
        
class BaseRenderer(Renderer):
    def __init__(self, base):
        self.base = base;
        
    def draw(self, screen, position, offset, delta_time):
        x = (position[0] + 0.5) * settings.TILE_SIZE + offset[0];
        y = (position[1] + 0.5) * settings.TILE_SIZE + offset[1];
        pygame.draw.circle(screen, pygame.Color('blue'), (x, y), settings.TILE_SIZE // 2);
        
class ConstructorRenderer(Renderer):
    def __init__(self, constructor):
        self.constructor = constructor;
        self.image = pygame.transform.scale2x(assets['constructor.png']);
        
    def draw(self, screen, position, offset, delta_time):
        x = position[0] * settings.TILE_SIZE + offset[0];
        y = position[1] * settings.TILE_SIZE + offset[1];
        
        screen.blit(self.image, (x, y));
        
class SpikeRenderer(Renderer):
    def __init__(self, spike):
        self.spike = spike;
        self.image = pygame.transform.scale2x(assets['spike.png']);
        
    def draw(self, screen, position, offset, delta_time):
        x = (position[0] + 0.5) * settings.TILE_SIZE + offset[0];
        y = (position[1] + 0.5) * settings.TILE_SIZE + offset[1];
        
        temp_rect = self.image.get_rect(center = (x, y));
        screen.blit(self.image, temp_rect);
            
class MinerRenderer(Renderer):
    def __init__(self, miner):
        self.miner = miner;
        self.walk = assets['miner.png'][:6];
        self.attack = assets['miner.png'][6:];
        self.progress = 0;
        self.attack_progress = 0;
        
    def draw(self, screen, offset, delta_time):
        x = self.miner.position[0] + offset[0];
        y = self.miner.position[1] + offset[1];
        ang = angle(self.miner.direction, (0, -1));
        
        if self.miner.task.empty():
            image = pygame.transform.scale2x(self.attack[0]);
            image = pygame.transform.rotate(image, ang);
            
            temp_rect = image.get_rect(center = (x, y));
            screen.blit(image, temp_rect);
        elif type(self.miner.task.queue[0]) == commands.Move:
            self.progress += delta_time * self.miner.modified_speed;
            image = pygame.transform.scale2x(self.walk[int(len(self.walk) * self.progress) % len(self.walk)]);
            image = pygame.transform.rotate(image, ang);
            
            temp_rect = image.get_rect(center = (x, y));
            screen.blit(image, temp_rect);
        elif type(self.miner.task.queue[0]) == commands.Harvest:
            self.attack_progress += delta_time;
            image = pygame.transform.scale2x(self.attack[int(len(self.attack) * self.attack_progress) % len(self.attack)]);
            image = pygame.transform.rotate(image, ang);
            
            temp_rect = image.get_rect(center = (x, y));
            screen.blit(image, temp_rect);
            
class EnemyRenderer(Renderer):
    def __init__(self, enemy):
        self.enemy = enemy;
        self.walk = assets['enemy.png'][:6];
        self.attack = assets['enemy.png'][6:];
        self.progress = 0;
        self.attack_progress = 0;
        
    def draw(self, screen, offset, delta_time):
        x = self.enemy.position[0] + offset[0];
        y = self.enemy.position[1] + offset[1];
        ang = angle(self.enemy.direction, (0, -1));
        
        if self.enemy.task.empty():
            image = pygame.transform.scale2x(self.attack[0]);
            image = pygame.transform.rotate(image, ang);
            
            temp_rect = image.get_rect(center = (x, y));
            screen.blit(image, temp_rect);
        elif type(self.enemy.task.queue[0]) == commands.Move:
            self.progress += delta_time * self.enemy.modified_speed;
            image = pygame.transform.scale2x(self.walk[int(len(self.walk) * self.progress) % len(self.walk)]);
            image = pygame.transform.rotate(image, ang);
            
            temp_rect = image.get_rect(center = (x, y));
            screen.blit(image, temp_rect);
        elif type(self.enemy.task.queue[0]) == commands.Attack:
            self.attack_progress += delta_time;
            image = pygame.transform.scale2x(self.attack[int(len(self.attack) * self.attack_progress) % len(self.attack)]);
            image = pygame.transform.rotate(image, ang);
            
            temp_rect = image.get_rect(center = (x, y));
            screen.blit(image, temp_rect);