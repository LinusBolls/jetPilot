import math

from game_object.prototype import GameObject
from assets import textures
from util import render_around_center, resize_to_height

class Explosion(GameObject):
    def __init__(self, game, spawn_point, diameter, damage):
        super().__init__(game, spawn_point, (0, -1), (0, 0), textures["explosion_0"], [ "explosion" ])

        self.spawn_point = spawn_point

        self.proto_img = textures["explosion_0"]
        self.rect = self.proto_img.get_rect(center=spawn_point)
        self.x = self.rect.centerx
        self.y = self.rect.centery

        self.damage = damage
        self.diameter = diameter

        self.time_alive = 0
        self.lifespan = 30

    def grow_func(self):
        return math.floor(self.diameter - self.diameter / (self.time_alive + 1))

    def update(self, game):
        super().update(game)

        self.time_alive += 1

        if self.time_alive > self.lifespan:
            self.remove(game)

    def render(self):

        self.img = resize_to_height(self.proto_img, self.grow_func())

        self.rect = self.img.get_rect(center=(self.spawn_point[0], self.spawn_point[1]))
        self.x = self.rect.x
        self.y = self.rect.y

        super().render()