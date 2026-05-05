import tiles;
import settings;
import structures;
import random;
import numpy as np
from perlin_numpy import generate_perlin_noise_2d

class Generator:
    def __init__(self, seed = None):
        self.seed = seed;
        self.grid = [[tiles.Tile() for a in range(settings.TILE_WIDTH)] for b in range(settings.TILE_HEIGHT)];
        
        self.generate_grid();
        self.generate_base();
        self.generate_resource();
    
    def generate_grid(self):
        if self.seed:
            np.random.seed(self.seed);
        
        res = 5;
        shape = (settings.TILE_HEIGHT, settings.TILE_WIDTH);
        resolution = (res, res);
        
        noise = generate_perlin_noise_2d(shape, resolution);
        noise = (noise - noise.min()) / (noise.max() - noise.min())
        
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if noise[y, x] < 0.4:
                    self.grid[y][x].type = 'water';
                    
    def generate_resource(self):
        seed = self.seed;
        if seed:
            random.seed(seed);
            
        tree_amount = random.randint(1000, 1500);
        
        for i in range(tree_amount):
            seed = random.randint(0, 10 ** 31);
            random.seed(seed);
            
            x = random.randint(0, settings.TILE_WIDTH - 1);
            y = random.randint(0, settings.TILE_HEIGHT - 1);
            if not self.grid[y][x].type == 'water':
                self.grid[y][x].set_structure(structures.Tree());
                
        stone_amount = random.randint(300, 400);
        
        for i in range(stone_amount):
            seed = random.randint(0, 10 ** 31);
            random.seed(seed);
            
            x = random.randint(0, settings.TILE_WIDTH - 1);
            y = random.randint(0, settings.TILE_HEIGHT - 1);
            if not self.grid[y][x].type == 'water':
                self.grid[y][x].set_structure(structures.Stone());
                
    def generate_base(self):
        if self.seed:
            random.seed(self.seed);

        x = random.randint(0, settings.TILE_WIDTH - 1);
        y = random.randint(0, settings.TILE_HEIGHT - 1);
        while self.grid[y][x].type == 'water':
            x = random.randint(0, settings.TILE_WIDTH - 1);
            y = random.randint(0, settings.TILE_HEIGHT - 1);
            
        self.base_position = (x, y);
        
    