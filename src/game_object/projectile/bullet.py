import pygame

from game_object.prototype import GameObject
from assets import textures, sounds
from util import is_outside_bounds

class Bullet(GameObject):
    def __init__(self, game, spawn_point, spawn_heading, spawn_speed):
        super().__init__(game, spawn_point, spawn_heading, spawn_speed, textures["bullet"], [ "bullet", "projectile" ])

        pygame.mixer.find_channel(True).play(sounds["bullet"])
