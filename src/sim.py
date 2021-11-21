import random

import pygame

from sand import Block

class Game:

    def __init__(self):
  
        pygame.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.preferred_sim_direction = True
        self.small_block_size = 7
        self.large_block_size = 4 * self.small_block_size

        self.clock = pygame.time.Clock()

        self.is_running = False
        self.floor = 50

        self.start()
        
    def start(self):
        self.grid = {}
        self.objects = pygame.sprite.Group()

        # spawn_sand_img(self, self.grid, "../ding.png", (10, 0))
        # spawn_sand_img(self, self.grid, "../mc_grass.png", (100, 0))
        # spawn_sand_img(self, self.grid, "../mc_grass.png", (116, 0))
        # spawn_sand_img(self, self.grid, "../mc_grass.png", (132, 0))
        # spawn_sand_img(self, self.grid, "../mc_grass.png", (100, 16))
        # spawn_sand_img(self, self.grid, "../mc_grass.png", (116, 16))
        # spawn_sand_img(self, self.grid, "../grass.png", (136, 32))
        # spawn_sand_img(self, self.grid, "../grass.png", (140, 32))
        # spawn_sand_img(self, self.grid, "../grass.png", (144, 32))
        # spawn_sand_img(self, self.grid, "../grass.png", (148, 32))
        # spawn_sand_img(self, self.grid, "../grass.png", (152, 32))
        Block(self, (132, 32), pygame.image.load("../grass.png"))
        Block(self, (132, 36), pygame.image.load("../dirt.png"))
        Block(self, (136, 32), pygame.image.load("../grass.png"))
        Block(self, (136, 36), pygame.image.load("../dirt.png"))
        Block(self, (140, 32), pygame.image.load("../grass.png"))
        Block(self, (140, 36), pygame.image.load("../dirt.png"))
        Block(self, (144, 32), pygame.image.load("../grass.png"))
        Block(self, (144, 36), pygame.image.load("../dirt.png"))
        Block(self, (148, 32), pygame.image.load("../grass.png"))
        Block(self, (148, 36), pygame.image.load("../dirt.png"))
        Block(self, (152, 32), pygame.image.load("../grass.png"))
        Block(self, (152, 36), pygame.image.load("../dirt.png"))
        Block(self, (156, 32), pygame.image.load("../grass.png"))
        Block(self, (156, 36), pygame.image.load("../dirt.png"))

        self.run_game()

    def run_game(self):
        while True:

            for event in pygame.event.get():
                enter_pressed = event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN
                s_pressed = event.type == pygame.KEYDOWN and event.key == pygame.K_s
                if enter_pressed:
                    self.start()
                if s_pressed:
                    self.is_running = not self.is_running
                    for object in self.objects:
                        object.destroy(self, None)
  
            self.screen.fill((255, 255, 255))

            self.preferred_sim_direction = bool(random.randint(0, 1))

            for object in self.objects:
                if self.is_running:
                    object.update(self)
                object.render(self)

            pygame.display.flip()

            self.clock.tick(20)

if __name__ == "__main__":
    Game()