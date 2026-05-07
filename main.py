import pygame;
import tiles;
import spaces;
import units;
import players;
import load;
import settings;
import menu;

pygame.init()

screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT));
clock = pygame.Clock();
main_menu = menu.MainMenu();
pause_menu = menu.PauseMenu();
game_over = menu.GameOverMenu();
current_scene = 'main menu';
fast_forward = 3;

def reload():
    global time_left;
    global gen;
    global grid;
    global space;
    global player_action;
    global current_mode;
    global drag_pos;
    global is_running;
    global is_pause;
    
    time_left = settings.DAY_TIME;
    gen = load.Generator();
    grid = gen.grid;
    space = spaces.Space(grid, gen.base_position);
    player_action = players.PlayerAction(space);
    current_mode = 'select';
    drag_pos = None;
    is_running = True;
    is_pause = False;
    
    for _ in range(20):
        miner = units.Miner('default', ((space.base_position[0] + 0.5) * settings.TILE_SIZE, (space.base_position[1] + 0.5) * settings.TILE_SIZE));
        space.add(miner);

def event_handler():
    global is_running;
    global current_mode;
    global current_scene;
    global drag_pos;
    global is_pause;
    
    if current_scene == 'main menu':
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                is_running = False;
                break;
    
    elif current_scene == 'pause menu':
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                is_running = False;
                break;
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                current_scene = 'play';
                
    elif current_scene == 'game over':
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                is_running = False;
                break;
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                reload();
                current_scene = 'main menu';
    
    elif current_scene == 'play':
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                is_running = False;
                break;
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                current_scene = 'pause menu';
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_1:
                current_mode = 'select';
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_2:
                current_mode = 'build road';
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_3:
                current_mode = 'build bridge';
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_4:
                current_mode = 'build spike';
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_5:
                current_mode = 'build crossbow';

        if current_mode == 'select':
            if pygame.mouse.get_just_pressed()[0]:
                drag_pos = pygame.mouse.get_pos();
            
            if pygame.mouse.get_just_released()[0]:
                left, top = tiles.pixel_to_tile(drag_pos);
                right, bottom = tiles.pixel_to_tile(pygame.mouse.get_pos());
                
                player_action.add_harvest(left, top, right, bottom);
                drag_pos = None;
                    
        if current_mode == 'build road':
            if pygame.mouse.get_pressed()[0]:
                player_action.add_road(tiles.pixel_to_tile(pygame.mouse.get_pos()));
                
        if current_mode == 'build bridge':
            if pygame.mouse.get_pressed()[0]:
                player_action.add_bridge(tiles.pixel_to_tile(pygame.mouse.get_pos()));
                
        if current_mode == 'build spike':
            if pygame.mouse.get_pressed()[0]:
                player_action.add_spike(tiles.pixel_to_tile(pygame.mouse.get_pos()));
                
        if current_mode == 'build crossbow':
            if pygame.mouse.get_pressed()[0]:
                player_action.add_crossbow(tiles.pixel_to_tile(pygame.mouse.get_pos()));
            

def show_text(screen):
    global time_left;
    font = pygame.font.Font(load.path('data/font/Minecraft.ttf'), 18);
    fps_text = font.render(f"FPS: {clock.get_fps():.2f}", True, pygame.Color("white"));
    screen.blit(fps_text, (5, 5));
    
    if space.is_night:
        mode_text = font.render(f"Night {space.day_counter}", True, pygame.Color("white"));
        screen.blit(mode_text, (5, 25));
    else:
        mode_text = font.render(f"Day {space.day_counter}, time left: {int(time_left // 60):02d}:{int(time_left % 60):02d}", True, pygame.Color("white"));
        screen.blit(mode_text, (5, 25));
    
    mode_text = font.render(f"Current mode: {current_mode}", True, pygame.Color("white"));
    screen.blit(mode_text, (5, 45));
    
    for i in range(3):
        tmp = space.base.inventory[i];
        if not tmp.type:
            break;
        res_text = font.render(f"{tmp.type}: {tmp.amount}", True, pygame.Color("white"));
        screen.blit(res_text, (5, 65 + 20 * i));
        
def renderer():
    if current_scene == 'main menu':
        main_menu.renderer.draw(screen);
        
    elif current_scene == 'play' or 'pause menu' or 'game over':
        tiles.draw_tile(screen, grid);
        tiles.draw_structure(screen, grid);
        space.draw_space(screen);
        tiles.draw_fog(screen, grid);
        
        show_text(screen);
        
        if current_scene == 'pause menu':
            pause_menu.renderer.draw(screen);
        elif current_scene == 'game over':
            game_over.renderer.draw(screen);
        elif drag_pos:
            tiles.draw_drag(screen, drag_pos);
        else:
            tiles.draw_hover(screen);
    
    pygame.display.flip();

def run(screen):
    global time_left;
    global current_scene;
    global is_running;
    global is_pause;
    
    while is_running:
        event_handler();
        delta_time = clock.tick(settings.FPS) / 1000;
        
        if current_scene == 'main menu':
            if main_menu.play.check_pressed():
                current_scene = 'play';
            if main_menu.scoreboard.check_pressed():
                pass;
                # current_scene = 'scoreboard';
            if main_menu.exit.check_pressed():
                is_running = False;
                
        elif current_scene == 'pause menu':
            is_pause = True;
            
            if pause_menu.play.check_pressed():
                current_scene = 'play';
            if pause_menu.restart.check_pressed():
                reload();
                current_scene = 'play';
            if pause_menu.exit.check_pressed():
                current_scene = 'main menu';
                
        elif current_scene == 'game over':
            if game_over.restart.check_pressed():
                reload();
                current_scene = 'play';
            if game_over.exit.check_pressed():
                reload();
                current_scene = 'main menu';
                
        elif current_scene == 'play':
            is_pause = False;
            if time_left <= 0:
                time_left = settings.DAY_TIME;
                space.set_night_time();
                
            if space.base.is_destroyed:
                current_scene = 'game over';
            
            if not space.is_night:
                player_action.update();
                time_left -= (delta_time * fast_forward * (not is_pause));
                
            space.step(delta_time * fast_forward * (not is_pause));
            space.update();
        
        renderer();
    pygame.quit();
    
if __name__ == "__main__":
    reload();
    run(screen);