from random import randint

import pygame

from util import resize_to_height

def spawn_sand_img(game, img, pos, lifespan=10):
    for x in range(4):
        for y in range(4):
            r, g, b, a = img.get_at((x * game.small_block_size, y * game.small_block_size))
            if a != 0:  #  if pixel is opaque
                px_pos = (x + pos[0], y + pos[1])
                grain = Grain(game, px_pos, (r, g, b), lifespan)
                game.grid[px_pos] = grain
                game.objects.add(grain)

def get_next_pos(pos, grid, preferred_direction):  
    pos_x, pos_y = pos
    if preferred_direction:
        if (pos_x, pos_y + 1) not in grid:
            return (pos_x, pos_y + 1)
        elif (pos_x + 1, pos_y + 1) not in grid:
            return (pos_x + 1, pos_y + 1)
        elif (pos_x - 1, pos_y + 1) not in grid:
            return (pos_x - 1, pos_y + 1)
    else:
        if (pos_x, pos_y + 1) not in grid:
            return (pos_x, pos_y + 1)
        elif (pos_x - 1, pos_y + 1) not in grid:
            return (pos_x - 1, pos_y + 1)
        elif (pos_x + 1, pos_y + 1) not in grid:
            return (pos_x + 1, pos_y + 1)
    return pos

class Grain(pygame.sprite.Sprite):
    def __init__(self, game, spawn_point, color, lifespan=10):

        super().__init__()

        self.screen = game.screen
        self.x, self.y = spawn_point
        self.color = color
        self.small_block_size = game.small_block_size
        self.lifespan=lifespan

    def update(self, game):

        if self.lifespan is not None and randint(0, self.lifespan) == 0:
            del game.grid[(self.x, self.y)]
            game.objects.remove(self)
            return

        next_pos = get_next_pos((self.x, self.y), game.grid, game.preferred_sim_direction)

        if next_pos[1] > game.floor:
            return

        if (self.x, self.y) != next_pos:
            del game.grid[(self.x, self.y)]
            game.grid[next_pos] = self
            self.x, self.y = next_pos

    def render(self, game):
        pygame.draw.rect(self.screen, self.color,(self.x * self.small_block_size, self.y * self.small_block_size, self.small_block_size, self.small_block_size))

class Block(pygame.sprite.Sprite):
    def __init__(self, game, spawn_point, texture):
        
        super().__init__()

        self.screen = game.screen
        self.img = resize_to_height(texture, game.large_block_size)
        self.rect = self.img.get_rect(left=spawn_point[0], top=spawn_point[1])
        self.spawn_point = spawn_point

        game.objects.add(self)

        for x in range(4):
            for y in range(4):
                game.grid[(x + self.spawn_point[0], y + self.spawn_point[1])] = self
    
    def render(self, game):
        self.screen.blit(self.img, self.img.get_rect(left=self.rect.x * game.small_block_size, top=self.rect.y * game.small_block_size))

    def remove(self, game):
        game.objects.remove(self)

        for x in range(4):
            for y in range(4):
                del game.grid[(x + self.spawn_point[0], y + self.spawn_point[1])]
    
    def destroy(self, game, lifespan=10):
        self.remove(game)
        spawn_sand_img(game, self.img, self.rect.topleft, lifespan)