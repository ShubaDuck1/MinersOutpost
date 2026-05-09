import settings;
import pygame;
import render;
import load;
import pickle;

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
    
class PlayButton(Button):
    def __init__(self, name, left, top, width, height):
        super().__init__(name, left, top, width, height);
        self.renderer = render.PlayButtonRenderer(self);
    
class TextBox:
    def __init__(self, name, left, top, width, height, text_limit = 15):
        self.name = name;
        self.current_text = '';
        self.text_limit = text_limit;
        
        self.top = top;
        self.left = left;
        self.width = width;
        self.height = height;
        
        self.renderer = render.TextBoxRenderer(self);
        
    def add(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.current_text = self.current_text[:-1];
        elif event.key == pygame.K_RETURN:
            pass;
        elif len(self.current_text) < self.text_limit:
            self.current_text += event.unicode;
        
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
        
        self.text_box = TextBox('Enter name...', settings.WIDTH // 2 - width // 2, 310, width, height, 20);
        self.restart = Button('Restart', settings.WIDTH // 2 - width // 2, 400, width, height);
        self.scoreboard = Button('Scoreboard', settings.WIDTH // 2 - width // 2, 490, width, height);
        self.exit = Button('Main Menu', settings.WIDTH // 2 - width // 2, 580, width, height);

        self.renderer = render.GameOverMenuRenderer(self);
        
class PlayMenu:
    def __init__(self):
        self.slow_down = PlayButton('slow down', settings.WIDTH - 42 * 4, 10, 32, 32);
        self.default = PlayButton('default', settings.WIDTH - 42 * 3, 10, 32, 32);
        self.speed_up = PlayButton('speed up', settings.WIDTH - 42 * 2, 10, 32, 32);
        self.options = PlayButton('options', settings.WIDTH - 42, 10, 32, 32);
        self.renderer = render.PlayMenuRenderer(self);
        
class Scoreboard:
    def __init__(self, filename = load.path('asset/scoreboard.pkl')):
        self.file = filename;
        self.scores = [];
        self.load_score();
        
        self.board_width = 400;
        self.board_height = 500;
        
        width = 150;
        height = 60;
        self.back = Button('Back', settings.WIDTH // 2 + self.board_width // 2 - width, settings.HEIGHT - 30 - height, width, height);
        self.renderer = render.ScoreboardRenderer(self);
        
    def add(self, data):
        self.scores.append(data);
        self.scores.sort(key=lambda x: x["score"], reverse=True);
        
    def save_score(self, filename = None):
        if not filename:
            filename = self.file;
            
        with open(filename, 'wb') as f:
            pickle.dump(self.scores, f);
            
    def load_score(self, filename = None):
        if not filename:
            filename = self.file;
        
        try:
            with open(filename, 'rb') as f:
                self.scores = pickle.load(f);
        except:
            return;