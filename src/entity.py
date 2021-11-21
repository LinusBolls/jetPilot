import math

import pygame

from util import render_around_center

class Entity(pygame.sprite.Sprite):
    def __init__(self, spawn_point, spawn_heading, spawn_speed, texture, tags):
        super().init()

        self.img = texture
        self.rect = self.img.get_rect(topleft=spawn_point)
        self.speed_x, self.speed_y = spawn_speed
        self.heading_x, self.heading_y = spawn_heading

    def update(self, game):

      self.rect.x += self.speed_x
      self.rect.y += self.speed_y

    def get_angle(self):
        return (math.atan2(-self.heading_y, self.heading_x) * 180 / math.pi) - 90
    
    def relative_point(self, offset_x, offset_y):
        normal_heading_x, normal_heading_y = (-self.heading_y, self.heading_x)
        return (self.rect.centerx + self.heading_x * offset_x + normal_heading_x * offset_y, self.rect.centery + self.heading_y * offset_x + normal_heading_y * offset_y)

    def render(self):
        render_around_center(self.screen, self.img, self.rect, self.get_angle())

    def remove(self, game):
        game.objects.remove(self)