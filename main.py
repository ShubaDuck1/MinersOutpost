import pygame;
import tiles;
import spaces;
import units;

pygame.init()

WIDTH, HEIGHT = 1280, 720;
FPS = 60;

clock = pygame.Clock();
space = spaces.Space();
is_running = True;

screen = pygame.display.set_mode((WIDTH, HEIGHT));
grid = [[tiles.Tile() for a in range(tiles.TILE_WIDTH)] for b in range(tiles.TILE_HEIGHT)];

def event_handler():
    global is_running;
    
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            is_running = False;
            break;
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            is_running = False;
            break;
    
    if pygame.mouse.get_just_pressed()[0]:
        space.add(units.Unit(tiles.TILE_SIZE * 2, pygame.mouse.get_pos(), 5));
    
    if pygame.mouse.get_just_pressed()[2]:
        space.find_path(grid, tiles.pixel_to_tile(pygame.mouse.get_pos()))
        
def show_fps(screen):
    font = pygame.font.SysFont("Arial", 18, bold=True);
    fps_text = font.render(f"FPS: {clock.get_fps():.2f}", True, pygame.Color("white"));
    screen.blit(fps_text, (5, 5));
        
def renderer():
    tiles.draw_tile(screen, grid);
    space.draw_space(screen);
    show_fps(screen);
    
    pygame.display.flip();


def run(screen):
    while is_running:
        event_handler();
        
        delta_time = clock.tick(FPS) / 1000;
        
        space.step(delta_time);
        renderer();
            
    quit();
    
if __name__ == "__main__":
    run(screen);