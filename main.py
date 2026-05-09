import pygame;
import tiles;
import spaces;
import units;
import players;
import load;
import settings;
import menu;
import render;

pygame.init()
pygame.key.set_repeat(500, 20);
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT));

render.load_assets();
clock = pygame.Clock();
main_menu = menu.MainMenu();
pause_menu = menu.PauseMenu();
game_over = menu.GameOverMenu();
scoreboard = menu.Scoreboard();
cursor_renderer = render.CursorRenderer();

pygame.mouse.set_visible(False);
current_scene = 'main menu';
fast_forward = 3;
drag_pos = None;
is_running = True;
is_pause = False;
move_camera_pos = None;
offset = (0, 0);
last_offset = None;

def reload():
    global time_left;
    global time_survived;
    global gen;
    global grid;
    global space;
    global player_action;
    global current_mode;
    global offset;
    
    time_left = settings.DAY_TIME;
    time_survived = 0;
    gen = load.Generator();
    grid = gen.grid;
    space = spaces.Space(grid, gen.base_position);
    player_action = players.PlayerAction(space);
    current_mode = 'select';
    
    x = settings.WIDTH // 2 - space.base_position[0] * settings.TILE_SIZE;
    y = settings.HEIGHT // 2 - space.base_position[1] * settings.TILE_SIZE;
    x = max(x, settings.WIDTH - settings.TILE_SIZE * settings.TILE_WIDTH);
    y = max(y, settings.HEIGHT - settings.TILE_SIZE * settings.TILE_HEIGHT);
    x = min(x, 0);
    y = min(y, 0);
    offset = (x, y);
    
    # for y in range(len(grid)):
    #     for x in range(len(grid[y])):
    #         grid[y][x].is_foggy = False;
    
    for _ in range(20):
        miner = units.Miner('default', ((space.base_position[0] + 0.5) * settings.TILE_SIZE, (space.base_position[1] + 0.5) * settings.TILE_SIZE));
        space.add(miner);

def event_handler():
    global is_running;
    global current_mode;
    global current_scene;
    global drag_pos;
    global is_pause;
    global move_camera_pos;
    global offset;
    global last_offset;
    
    if current_scene == 'main menu':
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                is_running = False;
                break;
            
        if main_menu.play.check_pressed():
            current_scene = 'play';
        elif main_menu.scoreboard.check_pressed():
            current_scene = 'scoreboard';
        elif main_menu.exit.check_pressed():
            is_running = False;
    
    elif current_scene == 'pause menu':
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                is_running = False;
                break;
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                current_scene = 'play';
                
        is_pause = True;
            
        if pause_menu.play.check_pressed():
            current_scene = 'play';
        elif pause_menu.restart.check_pressed():
            reload();
            current_scene = 'play';
        elif pause_menu.exit.check_pressed():
            current_scene = 'main menu';
                
    elif current_scene == 'game over':
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                is_running = False;
                break;
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                reload();
                current_scene = 'main menu';
                
            if ev.type == pygame.KEYDOWN:
                game_over.text_box.add(ev);
                if ev.key == pygame.K_RETURN and game_over.text_box.current_text != '':
                    data = {
                        'name': game_over.text_box.current_text,
                        'score': time_survived
                    }
                    scoreboard.add(data);
                    scoreboard.save_score();
                    current_scene = 'scoreboard';
                
        if game_over.restart.check_pressed():
            reload();
            current_scene = 'play';
        if game_over.scoreboard.check_pressed():
            reload();
            current_scene = 'scoreboard';
        if game_over.exit.check_pressed():
            reload();
            current_scene = 'main menu';
                
    elif current_scene == 'scoreboard':
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                is_running = False;
                break;
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                current_scene = 'main menu';
            elif ev.type == pygame.MOUSEWHEEL:
                scoreboard.renderer.start_line += ev.y * 40;
                
        if scoreboard.back.check_pressed():
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
                
        if pygame.mouse.get_pressed()[2]:
            if move_camera_pos:
                
                x = offset[0] + (pygame.mouse.get_pos()[0] - move_camera_pos[0]);
                y = offset[1] + (pygame.mouse.get_pos()[1] - move_camera_pos[1]);
                
                if not settings.WIDTH - settings.TILE_SIZE * settings.TILE_WIDTH <= x <= 0: 
                    x = max(x, settings.WIDTH - settings.TILE_SIZE * settings.TILE_WIDTH);
                    x = min(x, 0);
                    pygame.mouse.set_pos(move_camera_pos[0], pygame.mouse.get_pos()[1]);
                        
                if not settings.HEIGHT - settings.TILE_SIZE * settings.TILE_HEIGHT <= y <= 0:
                    y = max(y, settings.HEIGHT - settings.TILE_SIZE * settings.TILE_HEIGHT);
                    y = min(y, 0);
                    pygame.mouse.set_pos(pygame.mouse.get_pos()[0], move_camera_pos[1]);
                    
                offset = (x, y);
            move_camera_pos = pygame.mouse.get_pos();
        else:
            move_camera_pos = None;

        if current_mode == 'select':
            if pygame.mouse.get_just_pressed()[0]:
                drag_pos = pygame.mouse.get_pos();
                last_offset = offset;
            
            if pygame.mouse.get_just_released()[0]:
                left, top = tiles.pixel_to_tile((drag_pos[0] - last_offset[0], drag_pos[1] - last_offset[1]));
                pos = pygame.mouse.get_pos();
                right, bottom = tiles.pixel_to_tile((pos[0] - offset[0], pos[1] - offset[1]));
                
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
    font = render.assets['font18'];
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
    screen.fill(pygame.Color('black'));
    if current_scene == 'main menu':
        main_menu.renderer.draw(screen);
        
    elif current_scene == 'scoreboard':
        scoreboard.renderer.draw(screen);
        
    elif current_scene == 'play' or 'pause menu' or 'game over':
        tiles.draw_tile(screen, grid, offset, delta_time);
        # space.draw_space(screen);
        tiles.draw_structure(screen, grid, offset, delta_time);
        tiles.draw_fog(screen, grid, offset);
        
        show_text(screen);

        if current_scene == 'pause menu':
            pause_menu.renderer.draw(screen);
        elif current_scene == 'game over':
            game_over.renderer.draw(screen);
        elif drag_pos:
            tiles.draw_drag(screen, drag_pos, last_offset, offset);
        else:
            tiles.draw_hover(screen, offset);
    
    cursor_renderer.draw(screen);
    
    pygame.display.flip();

def run(screen):
    global time_left;
    global time_survived;
    global current_scene;
    global is_running;
    global is_pause;
    global delta_time;

    while is_running:
        
        event_handler();
        delta_time = clock.tick(settings.FPS) / 1000;

        if current_scene == 'play':
            is_pause = False;
            
            if time_left <= 0:
                time_left = settings.DAY_TIME;
                space.set_night_time();
                
            if space.base.is_destroyed:
                current_scene = 'game over';
            
            if not space.is_night:
                player_action.update();
                time_left -= (delta_time * fast_forward * (not is_pause));
                
            time_survived += (delta_time * fast_forward * (not is_pause));
            space.step(delta_time * fast_forward * (not is_pause));
            space.update();
        
        renderer();
    pygame.quit();
    
if __name__ == "__main__":
    reload();
    run(screen);