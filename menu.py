import settings;
import pygame;
import render;
import load;
import pickle;

class Button:
    '''
    Lớp nút nhấn trò chơi.
    
    Attributes:
        name (string): tên của nút.
        left (int): tọa độ bên trái của nút.
        top (int): tọa độ trên của nút.
        width (int): chiều ngang của nút.
        height (int): chiều cao của nút.
        is_pressed (bool): boolean mô tả trạng thái được nhấn của nút.
        renderer (ButtonRenderer): đối tượng xử lí đồ họa cho nút.
    '''
    
    def __init__(self, name, left, top, width, height):
        self.name = name;
        self.top = top;
        self.left = left;
        self.width = width;
        self.height = height;
        self.is_pressed = False;
        self.renderer = render.ButtonRenderer(self);
        
    def check_pressed(self):
        '''
        Hàm kiểm tra trạng thái được nhấn của nút.
        
        Returns:
            bool: giá trị boolean trạng thái.
        '''
        
        self.get_just_pressed();
        if self.get_just_released():
            return True;
        
        return False;
        
    def get_just_pressed(self):
        '''
        Hàm kiểm tra nút vừa được nhấn.
        '''
        
        mouse = pygame.mouse;
        if not mouse.get_just_pressed()[0]:
            return
        
        if not self.left <= mouse.get_pos()[0] < self.left + self.width:
            return
        
        if not self.top <= mouse.get_pos()[1] < self.top + self.height:
            return
        
        self.is_pressed = True;
        
    def get_just_released(self):
        '''
        Hàm kiểm tra nút vừa được thả.
        '''
        
        if not self.is_pressed:
            return False;
        
        if not pygame.mouse.get_just_released()[0]:
            return False;
        
        self.is_pressed = False;
        return True;
    
class PlayButton(Button):
    '''
    Lớp các nút được hiển thị trong lúc chơi.
    
    (Các nút tua nhanh, tua chậm và mở menu).
    
    Attributes:
        name (string): tên của nút.
        left (int): tọa độ bên trái của nút.
        top (int): tọa độ trên của nút.
        width (int): chiều ngang của nút.
        height (int): chiều cao của nút.
        is_pressed (bool): boolean mô tả trạng thái được nhấn của nút.
        renderer (PlayButtonRenderer): đối tượng xử lí đồ họa cho nút.
    '''
    
    def __init__(self, name, left, top, width, height):
        super().__init__(name, left, top, width, height);
        self.renderer = render.PlayButtonRenderer(self);
    
class TextBox:
    '''
    Lớp hộp chữ.
    
    Dùng lớp này để nhập tên để lưu vào bảng xếp hạng.
    
    Attributes:
        name (string): tên hộp.
        current_text (string): chuỗi kí tự hiện tại.
        text_limit (int): giới hạn độ lớn của chuỗi kí tự.
        left (int): tọa độ bên trái của hộp.
        top (int): tọa độ trên của hộp.
        width (int): chiều ngang của hộp.
        height (int): chiều cao của hộp.
        renderer (TextBoxRenderer): đối tượng xử lí đồ họa của hộp
    '''
    
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
        '''
        Hàm thêm kí tự vào chuỗi.
        
        Dự vào đối tượng sự kiện của pygame sẽ thêm kí tự vào chuỗi hiện tại.
        
        Args:
            event (Event): sự kiện của pygame.
        '''
        
        if event.key == pygame.K_BACKSPACE:
            self.current_text = self.current_text[:-1];
        elif event.key == pygame.K_RETURN:
            pass;
        elif len(self.current_text) < self.text_limit:
            self.current_text += event.unicode;
        
class MainMenu:
    '''
    Lớp Menu chính.
    
    Attributes:
        play (Button): nút chơi.
        scoreboard (Button): nút xem bảng xếp hạng.
        exit (Button): nút tắt trò chơi.
        renderer (MainMenuRenderer): xử lí đồ họa.
    '''
    
    def __init__(self):
        width = 300;
        height = 60;
        self.play = Button('Play', settings.WIDTH // 2 - width // 2, 420, width, height);
        self.scoreboard = Button('Scoreboard', settings.WIDTH // 2 - width // 2, 510, width, height);
        self.exit = Button('Exit', settings.WIDTH // 2 - width // 2, 600, width, height);

        self.renderer = render.MainMenuRenderer(self);
        
class PauseMenu:
    '''
    Lớp menu phụ khi dừng trò chơi.
    
    Attributes:
        play (Button): nút tiếp tục trò chơi sau khi dừng.
        restart (Button): nút chơi lại.
        exit (Button): nút tắt trò chơi.
        renderer (PauseMenuRenderer): xử lí đồ họa.
    '''
    
    def __init__(self):
        width = 300;
        height = 60;
        self.play = Button('Resume', settings.WIDTH // 2 - width // 2, 220, width, height);
        self.restart = Button('Restart', settings.WIDTH // 2 - width // 2, 310, width, height);
        self.exit = Button('Main Menu', settings.WIDTH // 2 - width // 2, 400, width, height);

        self.renderer = render.PauseMenuRenderer(self);
        
class GameOverMenu:
    '''
    Lớp menu phụ khi kết thúc trò chơi.
    
    Attributes:
        text_box (TextBox): hộp chữ để nhập và lưu vào bảng xếp hạng.
        restart (Button): nút chơi lại.
        scoreboard (Button): nút mở bảng xếp hạng.
        exit (Button): nút thoát trò chơi.
        renderer (GameOverMenuRenderer): xử lí đồ họa
    '''
    
    def __init__(self):
        width = 300;
        height = 60;
        
        self.text_box = TextBox('Enter name...', settings.WIDTH // 2 - width // 2, 310, width, height, 20);
        self.restart = Button('Restart', settings.WIDTH // 2 - width // 2, 400, width, height);
        self.scoreboard = Button('Scoreboard', settings.WIDTH // 2 - width // 2, 490, width, height);
        self.exit = Button('Main Menu', settings.WIDTH // 2 - width // 2, 580, width, height);

        self.renderer = render.GameOverMenuRenderer(self);
        
class PlayMenu:
    '''
    Lớp chứa các nút tua nhanh, tua chậm và dừng trò chơi.
    
    Attributes:
        slow_down (PlayButton): nút tua chậm trò chơi.
        default (PlayButton): nút để trò chơi ở tốc độ bình thường.
        speed_up (PlayButton): nút tua nhanh trò chơi.
        options (PlayButton): nút dừng trò chơi mà mở menu phụ.
        renderer (PlayMenuRenderer): xử lí đồ họa.
    '''
    
    def __init__(self):
        self.slow_down = PlayButton('slow down', settings.WIDTH - 42 * 4, 10, 32, 32);
        self.default = PlayButton('default', settings.WIDTH - 42 * 3, 10, 32, 32);
        self.speed_up = PlayButton('speed up', settings.WIDTH - 42 * 2, 10, 32, 32);
        self.options = PlayButton('options', settings.WIDTH - 42, 10, 32, 32);
        self.renderer = render.PlayMenuRenderer(self);
        
class Scoreboard:
    '''
    Lớp bảng xếp hạng.
    
    Attributes:
        file (Path): đường dẫn đến file chứa dữ liệu bảng xếp hạng.
        scores (list): danh sách bảng xếp hạng được đọc ra.
        board_width (int): độ dài của bảng.
        board_height (int): chiều cao của bảng.
        back (Button): nút quay lại menu chính.
        renderer (ScoreboardRenderer): xử lí đồ họa.
    '''
    
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
        '''
        Hàm thêm dữ liệu vào bảng.
        
        Args:
            data (dict): dữ liệu cần được thêm (gồm có giá trị name và giá trị score).
        '''
        
        self.scores.append(data);
        self.scores.sort(key=lambda x: x["score"], reverse=True);
        
    def save_score(self, filename = None):
        '''
        Hàm lưu bảng điểm:
        
        Args:
            filename (Path, optional): đường dẫn đến thư mục
        '''
        
        if not filename:
            filename = self.file;
            
        with open(filename, 'wb') as f:
            pickle.dump(self.scores, f);
            
    def load_score(self, filename = None):
        '''
        Hàm mở bảng điểm ra danh sách scores.
        
        Args:
            filename (Path, optional): đường dẫn đến thư mục
        '''
        
        if not filename:
            filename = self.file;
        
        try:
            with open(filename, 'rb') as f:
                self.scores = pickle.load(f);
        except:
            return;
        
class Clock:
    '''
    Lớp đồng hồ.
    
    Attributes:
        left (int): tọa độ bên trái.
        right (int): tọa độ bên trên.
        day_counter (int): ngày hiện tại.
        current_time (float): thời gian hiện tại.
        renderer (ClockRenderer): xử lí đồ họa.
    '''
    
    def __init__(self):
        self.left = 1130;
        self.top = 50;
        
        self.is_night = False;
        self.day_counter = 0;
        self.current_time = 0;
        self.renderer = render.ClockRenderer(self);