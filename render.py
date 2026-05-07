import pygame;
import load;
import settings;

class Renderer:
    def __init__(self):
        raise NotImplementedError();
    
    def draw(self):
        raise NotImplementedError();
    
class ButtonRenderer(Renderer):
    def __init__(self, button):
        self.button = button;
        
        self.g = pygame.Rect(button.left, button.top, button.width, button.height);
        font = pygame.font.Font(load.path('asset/font/Minecraft.ttf'), 25);
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
        
        font = pygame.font.Font(load.path('asset/font/Minecraft.ttf'), 150);
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
        self.font = pygame.font.Font(load.path('asset/font/Minecraft.ttf'), 80);
        
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
        self.start_line = 100;
        self.background_font = pygame.font.Font(load.path('asset/font/Minecraft.ttf'), 40);
        self.font = pygame.font.Font(load.path('asset/font/Minecraft.ttf'), 25);
        
        self.text_surface = self.background_font.render(f"Scoreboard", True, pygame.Color('white'));
        self.text_rect = self.text_surface.get_rect(center = (settings.WIDTH // 2, 50));
        
    def draw_background(self, screen):
        screen.fill(pygame.Color("#08d958"));
        screen.blit(self.text_surface, self.text_rect);
        
    def draw(self, screen):
        self.draw_background(screen);
        self.scoreboard.back.renderer.draw(screen);
        
        width = self.scoreboard.board_width;
        height = self.scoreboard.board_height;
        offset = 30;
        
        self.start_line = max(self.start_line, height - offset * (len(self.scoreboard.scores) + 1));
        self.start_line = min(self.start_line, 0);
        curr_line = self.start_line;
        
        board_surface = pygame.Surface((width, height), pygame.SRCALPHA);
        board_rect = board_surface.get_rect(center = (settings.WIDTH // 2, settings.HEIGHT // 2));
        
        for data in self.scoreboard.scores:
            if curr_line + offset >= height:
                text_surface = self.font.render(f"...", True, pygame.Color('white'));
                text_rect = text_surface.get_rect(topleft = (0, curr_line));
                board_surface.blit(text_surface, text_rect);
                break;
            
            text_surface = self.font.render(f"{data['name']}", True, pygame.Color('white'));
            text_rect = text_surface.get_rect(topleft = (0, curr_line));
            board_surface.blit(text_surface, text_rect);
            
            text_surface = self.font.render(f"{data['score']}", True, pygame.Color('white'));
            text_rect = text_surface.get_rect(topright = (width, curr_line));
            board_surface.blit(text_surface, text_rect);
            
            curr_line += offset;

        screen.blit(board_surface, board_rect);
        
class TreeRenderer(Renderer):
    def __init__(self, tree):
        self.tree = tree;
        self.image = pygame.image.load(load.path('asset/sprites/structures/tree.png')).convert_alpha();
        
    def draw(self, screen, position, delta_time):
        x = (position[0] + 0.5) * settings.TILE_SIZE;
        y = (position[1] + 0.5) * settings.TILE_SIZE - 16;
        
        image_rect = self.image.get_rect(center = (x, y));
        screen.blit(self.image, image_rect);
        
class StoneRenderer(Renderer):
    def __init__(self, stone):
        self.stone = stone;
        self.image = pygame.image.load(load.path('asset/sprites/structures/stone.png')).convert_alpha();
        
    def draw(self, screen, position, delta_time):
        x = (position[0] + 0.5) * settings.TILE_SIZE;
        y = (position[1] + 0.5) * settings.TILE_SIZE - 8;
        
        image_rect = self.image.get_rect(center = (x, y));
        screen.blit(self.image, image_rect);
        