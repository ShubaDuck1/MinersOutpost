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
    
    def draw(self, screen):
        top = self.button.top;
        left = self.button.left;
        width = self.button.width;
        height = self.button.height

        if self.button.is_pressed:
            color = pygame.Color('white');
        else:
            color = pygame.Color('grey');
    
        g = pygame.Rect(left, top, width, height);
        pygame.draw.rect(screen, color, g);
        
        font = pygame.font.Font(load.path('data/font/Minecraft.ttf'), 25);
        text_surface = font.render(f"{self.button.name}", True, pygame.Color('white'));
        text_rect = text_surface.get_rect(center = (g.center[0], g.center[1] + 2));
        screen.blit(text_surface, text_rect)
        
class MainMenuRenderer(Renderer):
    def __init__(self, main_menu):
        self.main_menu = main_menu;
        
    def draw_background(self, screen):
        screen.fill(pygame.Color("#08d958"));
        font = pygame.font.Font(load.path('data/font/Minecraft.ttf'), 150);
        text_surface = font.render(f"Minecraft", True, pygame.Color('white'));
        text_rect = text_surface.get_rect(center = (settings.WIDTH // 2, 220));
        screen.blit(text_surface, text_rect);
        
    def draw(self, screen):
        self.draw_background(screen);
        self.main_menu.play.renderer.draw(screen);
        self.main_menu.scoreboard.renderer.draw(screen);
        self.main_menu.exit.renderer.draw(screen);
        
class PauseMenuRenderer(Renderer):
    def __init__(self, pause_menu):
        self.pause_menu = pause_menu;
        
    def draw_background(self, screen):
        temp_surface = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA);
        g = g = pygame.Rect(0, 0, settings.WIDTH, settings.HEIGHT);
        pygame.draw.rect(temp_surface, (0, 0, 0, 100), g);
        screen.blit(temp_surface, (0, 0));
        
    def draw(self, screen):
        self.draw_background(screen);
        self.pause_menu.play.renderer.draw(screen);
        self.pause_menu.restart.renderer.draw(screen);
        self.pause_menu.exit.renderer.draw(screen);
    