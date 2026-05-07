import pygame;
import load;
import settings;

assets = {};
def load_assets():
    global assets;
    
    assets['font18'] = pygame.font.Font(load.path('asset/font/Minecraft.ttf'), 18);
    assets['font25'] = pygame.font.Font(load.path('asset/font/Minecraft.ttf'), 25);
    assets['font40'] = pygame.font.Font(load.path('asset/font/Minecraft.ttf'), 40);
    assets['font80'] = pygame.font.Font(load.path('asset/font/Minecraft.ttf'), 80);
    assets['font150'] = pygame.font.Font(load.path('asset/font/Minecraft.ttf'), 150);
    assets['grass.png'] = pygame.image.load(load.path('asset/sprites/tiles/grass.png'));
    assets['tree.png'] = pygame.image.load(load.path('asset/sprites/structures/tree.png')).convert_alpha();
    assets['stone.png'] = pygame.image.load(load.path('asset/sprites/structures/stone.png')).convert_alpha();
    

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
    def __init__(self, pause_menu):
        self.pause_menu = pause_menu;
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
        self.pause_menu.restart.renderer.draw(screen);
        self.pause_menu.exit.renderer.draw(screen);
        
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
            
            text_surface = self.font.render(f"{data['score']}", True, pygame.Color('white'));
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
        
class TileRenderer(Renderer):
    def __init__(self, tile):
        self.tile = tile;
        self.grass = None;
        
    def draw(self, screen, position, delta_time):
        if self.tile.type == 'grass':
            if not self.grass:
                self.grass = GrassRenderer(self.tile);
            
            self.grass.draw(screen, position, delta_time);
        
class GrassRenderer(Renderer):
    def __init__(self, tile):
        self.tile = tile;
        self.image = assets['grass.png'];
        
    def draw(self, screen, position, delta_time):
        x = position[0] * settings.TILE_SIZE;
        y = position[1] * settings.TILE_SIZE;

        screen.blit(self.image, (x, y));
        
class TreeRenderer(Renderer):
    def __init__(self, tree):
        self.tree = tree;
        self.image = assets['tree.png'];
        
    def draw(self, screen, position, delta_time):
        x = (position[0] + 0.5) * settings.TILE_SIZE;
        y = (position[1] + 0.5) * settings.TILE_SIZE - 16;
        
        image_rect = self.image.get_rect(center = (x, y));
        screen.blit(self.image, image_rect);
        
class StoneRenderer(Renderer):
    def __init__(self, stone):
        self.stone = stone;
        self.image = assets['stone.png'];
        
    def draw(self, screen, position, delta_time):
        x = (position[0] + 0.5) * settings.TILE_SIZE;
        y = (position[1] + 0.5) * settings.TILE_SIZE - 8;
        
        image_rect = self.image.get_rect(center = (x, y));
        screen.blit(self.image, image_rect);
        