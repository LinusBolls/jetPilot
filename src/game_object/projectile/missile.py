import math
import random

import pygame

from game_object.prototype import GameObject
from game_object.particle import Particle
from assets import textures, sounds
from util import is_outside_bounds, normalize

class Missile(GameObject):

    def __init__(self, game, spawn_point, spawn_heading, spawn_speed, owner_list, offset=random.uniform(-2.0, 2.0), turn_direction=(0, -1)):

        self.hits = 0
        self.time_alive = 0
        self.direction = (0, -1)
        self.turn_direction = turn_direction

        self.is_wacky = True
        self.curve_time = 3
        self.offset = offset
        self.spread = random.uniform(-0.3, 0.3)
        self.min_speed = 5

        self.streckung_x = 0.7 # ye niedriger desto breiter kurven
        self.streckung_y = 10 # ye niedriger desto mehr kurven

        self.owner_list = owner_list

        pygame.mixer.find_channel(True).play(sounds["missile"])

        self.target_x, self.target_y = pygame.mouse.get_pos()

        super().__init__(game, spawn_point, spawn_heading, (0, 0), textures["missile"], [ "missile", "projectile" ])

    def flight_path(self, x):
        return math.sin(x * self.streckung_x) / self.streckung_y

    def flight_path_derivative(self, x):
        return math.cos(x * self.streckung_x) / self.streckung_y * self.streckung_x

    def make_zeropoint_work(self, target_distance):
        return target_distance / math.pi

    def update(self, game):
        self.time_alive += 1

        speed = (self.time_alive ** 2 / 200) + self.min_speed

        # if self.is_wacky:

        #     mouse_x, mouse_y = pygame.mouse.get_pos()

        #     self.heading_x, self.heading_y = normalize((mouse_x - self.x, mouse_y - self.y))

        #     self.speed_x = self.heading_x * speed
        #     self.speed_y = self.heading_y * speed

        if self.is_wacky:
            # if self.time_alive == 60:
            #     self.heading_x, self.heading_y = normalize((self.target_x - self.x, self.target_y - self.y))

            # if self.time_alive < 60:
                # offset used so the missiles start on opposing sides
            rotation_angle = self.flight_path(self.time_alive / 5 + self.offset)

            # rotate the heading vector by the flight path value
            # https://matthew-brett.github.io/teaching/rotation_2d.html
            self.heading_x = math.cos(rotation_angle) * self.heading_x - math.sin(rotation_angle) * self.heading_y
            self.heading_y = math.sin(rotation_angle) * self.heading_x + math.cos(rotation_angle) * self.heading_y

            self.speed_x = self.heading_x * speed
            self.speed_y = self.heading_y * speed
        else:
            speed = (self.time_alive ** 2 / 100) + self.min_speed

            self.x += self.heading_x * speed
            self.y += self.heading_y * speed
        
        particle = Particle(game, self.rect.center, textures["explosion_1"], [ "particle" ], random.randint(30, 90))
        game.objects.add(particle)

            # value = (math.sin(self.time_alive / self.curve_time + self.offset) + self.spread) / 10
            # print(value)

            # strength = 1
            # if value > 0:
            #     value -= strength
            # else:
            #     value += strength
            
            # self.heading_x, self.heading_y = (math.sin(self.time_alive / self.curve_time + self.offset) + self.spread, -1)

        super().update(game)

    def turn(self):
        self.is_wacky = False
        mouse_x, mouse_y = pygame.mouse.get_pos()

        turn_action = 0


        if turn_action == 0:
            self.heading_x, self.heading_y = (self.turn_direction[0], 0)
            self.speed_x, self.speed_y = (self.turn_direction[0], 0)
        
        elif turn_action == 1:
            self.heading_x, self.heading_y = (self.turn_direction[0], 0)
            self.speed_x, self.speed_y = (self.turn_direction[0], self.turn_direction[1])

        elif turn_action == 1:
            self.heading_x, self.heading_y = normalize((mouse_x - self.x, mouse_y - self.y))
            self.speed_x, self.speed_y = (0, 0)

        elif turn_action == 2:
            self.heading_x, self.heading_y = normalize((self.target_x - self.x, self.target_y - self.y))
            self.speed_x, self.speed_y = (0, 0)

    def remove(self, game):
        super().remove(game)
        self.owner_list.remove(self)