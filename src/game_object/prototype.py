import math

import pygame

from util import render_around_center, is_outside_bounds

class GameObject(pygame.sprite.Sprite):

    def __init__(self, game, spawn_point, spawn_heading, spawn_speed, texture, tags, remove_off_screen=True):

        super().__init__()

        self.is_debug_mode = False

        self.tags = tags
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        self.img = texture
        self.rect = self.img.get_rect()

        
        self.rect.center= spawn_point
        self.x, self.y = self.rect.center

        self.heading_x, self.heading_y = spawn_heading
        self.speed_x, self.speed_y = spawn_speed

        self.remove_off_screen = remove_off_screen

    def update(self, game):
        if self.is_debug_mode:
            pygame.draw.rect(self.screen, (0, 255, 0),(self.x, self.y, 10, 10))
            pygame.draw.rect(self.screen, (0, 0, 255),(self.rect.centerx, self.rect.centery, 10, 10))

        self.x = self.x + self.speed_x
        self.y = self.y + self.speed_y
        self.rect.x, self.rect.y = self.x, self.y

        if self.remove_off_screen:
            a, b, c, d = is_outside_bounds(self.rect, (0, 0), (self.screen.get_width(), self.screen.get_height()))
            if a or b or c or d:
                self.remove(game)
    
    def get_angle(self):
        return (math.atan2(-self.heading_y, self.heading_x) * 180 / math.pi) - 90
    
    def relative_point(self, offset_x, offset_y):
        normal_heading_x, normal_heading_y = (-self.heading_y, self.heading_x)
        return (self.rect.centerx + self.heading_x * offset_x + normal_heading_x * offset_y, self.rect.centery + self.heading_y * offset_x + normal_heading_y * offset_y)

    def render(self):
        render_around_center(self.screen, self.img, self.rect, self.get_angle())

    def remove(self, game):
        game.objects.remove(self)