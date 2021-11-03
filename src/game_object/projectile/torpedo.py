import pygame

from game_object.prototype import GameObject
from assets import textures, sounds
from util import is_outside_bounds

class Torpedo(GameObject):
    def __init__(self, game, spawn_point, spawn_heading, spawn_speed, owner_list):
        super().__init__(game, spawn_point, spawn_heading, spawn_speed, textures["torpedo"], [ "torpedo", "projectile" ])

        pygame.mixer.find_channel(True).play(sounds["torpedo"])

        self.owner_list = owner_list
        self.player_speed = game.player.max_speed
    
    def turn(self):
        self.heading_x, self.heading_y = (0, -1)
        self.speed_x, self.speed_y = (0, -self.player_speed - 5)

    def remove(self, game):
        super().remove(game)
        self.owner_list.remove(self)