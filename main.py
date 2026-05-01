import pygame;
import tiles;
import spaces;
import units;
import players;
import structures;

pygame.init()

WIDTH, HEIGHT = 1280, 720;
FPS = 60;

screen = pygame.display.set_mode((WIDTH, HEIGHT));
clock = pygame.Clock();

grid = [[tiles.Tile() for a in range(tiles.TILE_WIDTH)] for b in range(tiles.TILE_HEIGHT)];
space = spaces.Space(grid, (40, 20));
player_action = players.PlayerAction(space);
is_running = True;

def event_handler():
    global is_running;
    
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            is_running = False;
            break;
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            is_running = False;
            break;
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_1:
            x, y = tiles.pixel_to_tile(pygame.mouse.get_pos());
            grid[y][x].set_structure(structures.Tree())
    
    if pygame.mouse.get_just_pressed()[0]:
        space.add(units.Miner('default', pygame.mouse.get_pos()));
    
    if pygame.mouse.get_just_pressed()[2]:
        player_action.add(tiles.pixel_to_tile(pygame.mouse.get_pos()));
        
def show_fps(screen):
    font = pygame.font.SysFont("Arial", 18, bold=True);
    fps_text = font.render(f"FPS: {clock.get_fps():.2f}", True, pygame.Color("white"));
    screen.blit(fps_text, (5, 5));
        
def renderer():
    tiles.draw_tile(screen, grid);
    tiles.draw_hover(screen);
    space.draw_space(screen);
    tiles.draw_structure(screen, grid);
    show_fps(screen);
    
    pygame.display.flip();


def run(screen):
    while is_running:
        event_handler();
        
        delta_time = clock.tick(FPS) / 1000;
        
        player_action.update();
        space.step(delta_time);
        space.update();
        renderer();
            
    quit();
    
if __name__ == "__main__":
    run(screen);