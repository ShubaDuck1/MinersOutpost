import settings;
import pygame;
import render;

class Button:
    def __init__(self, name, left, top, width, height):
        self.name = name;
        self.top = top;
        self.left = left;
        self.width = width;
        self.height = height;
        self.is_pressed = False;
        self.renderer = render.ButtonRenderer(self);
        
    def check_pressed(self):
        self.get_just_pressed();
        if self.get_just_released():
            return True;
        
        return False;
        
    def get_just_pressed(self):
        mouse = pygame.mouse;
        if not mouse.get_just_pressed()[0]:
            return
        
        if not self.left <= mouse.get_pos()[0] < self.left + self.width:
            return
        
        if not self.top <= mouse.get_pos()[1] < self.top + self.height:
            return
        
        self.is_pressed = True;
        
    def get_just_released(self):
        if not self.is_pressed:
            return False;
        
        if not pygame.mouse.get_just_released()[0]:
            return False;
        
        self.is_pressed = False;
        return True;

class MainMenu:
    def __init__(self):
        width = 300;
        height = 60;
        self.play = Button('Play', settings.WIDTH // 2 - width // 2, 420, width, height);
        self.scoreboard = Button('Scoreboard', settings.WIDTH // 2 - width // 2, 510, width, height);
        self.exit = Button('Exit', settings.WIDTH // 2 - width // 2, 600, width, height);

        self.renderer = render.MainMenuRenderer(self);
        
class PauseMenu:
    def __init__(self):
        width = 300;
        height = 60;
        self.play = Button('Resume', settings.WIDTH // 2 - width // 2, 220, width, height);
        self.restart = Button('Restart', settings.WIDTH // 2 - width // 2, 310, width, height);
        self.exit = Button('Main Menu', settings.WIDTH // 2 - width // 2, 400, width, height);

        self.renderer = render.PauseMenuRenderer(self);
        
class GameOverMenu:
    def __init__(self):
        width = 300;
        height = 60;
        self.restart = Button('Restart', settings.WIDTH // 2 - width // 2, 310, width, height);
        self.exit = Button('Main Menu', settings.WIDTH // 2 - width // 2, 400, width, height);

        self.renderer = render.GameOverMenuRenderer(self);