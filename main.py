import pygame;
import tiles;
import spaces;
import units;
import players;
import load;
import settings;

pygame.init()

screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT));
clock = pygame.Clock();

time_left = settings.DAY_TIME;
fast_forward = 3;
gen = load.Generator(69696969);
grid = gen.grid;
space = spaces.Space(grid, gen.base_position);
player_action = players.PlayerAction(space);
current_mode = 'select';
drag_pos = None;
is_running = True;

def event_handler():
    global is_running;
    global current_mode;
    global drag_pos;
    
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            is_running = False;
            break;
        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            is_running = False;
            break;
        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_1:
            current_mode = 'select';
        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_2:
            current_mode = 'build road';
        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_3:
            current_mode = 'build spike';
        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_4:
            current_mode = 'build crossbow';

    if current_mode == 'select':
        if pygame.mouse.get_just_pressed()[0]:
            drag_pos = pygame.mouse.get_pos();
        
        if pygame.mouse.get_just_released()[0]:
            left, top = tiles.pixel_to_tile(drag_pos);
            right, bottom = tiles.pixel_to_tile(pygame.mouse.get_pos());
            
            player_action.add_harvest(top, left, bottom, right);
            drag_pos = None;
                
    if current_mode == 'build road':
        if pygame.mouse.get_pressed()[0]:
            player_action.add_road(tiles.pixel_to_tile(pygame.mouse.get_pos()));
            
    if current_mode == 'build spike':
        if pygame.mouse.get_pressed()[0]:
            player_action.add_spike(tiles.pixel_to_tile(pygame.mouse.get_pos()));
            
    if current_mode == 'build crossbow':
        if pygame.mouse.get_pressed()[0]:
            player_action.add_crossbow(tiles.pixel_to_tile(pygame.mouse.get_pos()));
            

def show_text(screen):
    global time_left;
    font = pygame.font.SysFont("Arial", 18, bold=True);
    fps_text = font.render(f"FPS: {clock.get_fps():.2f}", True, pygame.Color("white"));
    screen.blit(fps_text, (5, 5));
    
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
    tiles.draw_tile(screen, grid);
    space.draw_space(screen);
    tiles.draw_structure(screen, grid);
    tiles.draw_fog(screen, grid);
    
    if drag_pos:
        tiles.draw_drag(screen, drag_pos);
    else:
        tiles.draw_hover(screen);
    
    show_text(screen);
    
    pygame.display.flip();


def run(screen):
    global time_left;
    
    for i in range(5):
        miner = units.Miner('default', ((space.base_position[0] + 0.5) * settings.TILE_SIZE, (space.base_position[1] + 0.5) * settings.TILE_SIZE));
        space.add(miner);
    
    while is_running:
        event_handler();
        
        delta_time = clock.tick(settings.FPS) / 1000;
        time_left -= delta_time * fast_forward;
        
        if time_left <= 0:
            time_left = settings.DAY_TIME;
            space.set_night_time();
        if not space.is_night:
            player_action.update();
        space.step(delta_time * fast_forward);
        space.update();
        renderer();
            
    quit();
    
if __name__ == "__main__":
    run(screen);