from threading import Timer
import math

import pygame

from util import get_magnitude, normalize, is_outside_bounds, render_around_center
from assets import textures
from game_object.prototype import GameObject
from game_object.projectile.bullet import Bullet
from game_object.projectile.missile import Missile
from game_object.projectile.torpedo import Torpedo

class Player(GameObject):

    def __init__(self, game, spawn_point, spawn_heading, spawn_speed):

        self.deployed_missiles = pygame.sprite.Group()
        self.deployed_torpedos_left = pygame.sprite.Group()
        self.deployed_torpedos_right = pygame.sprite.Group()
        self.is_thrusting = False
        self.is_shooting = False
        self.shooting_time = 0

        self.burst_size = 5
        self.shoot_frequency = 3

        self.max_speed = 5
        self.accel_force = 0.2
        self.decel_force = 0.1
        
        super().__init__(game, spawn_point, spawn_heading, spawn_speed, textures["player"], [ "player" ], False)

    def collide(self, game_obj):
        pass

    def get_front_point(self):
        return self.relative_point(50, 0)

    def get_wing_points(self):
        offset_x = -20 # geradeaus
        offset_y = 25 # away from wing
        return self.relative_point(offset_x, offset_y), self.relative_point(offset_x, -offset_y)
    
    def handle_event(self, game, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.is_thrusting = True
            elif event.key == pygame.K_w:
                self.shooting_time = 0
                self.is_shooting = True
            elif event.key == pygame.K_e:
                if len(self.deployed_missiles) < 2:
                    missile_speed = 5
                    left_missile = Missile(game, self.get_wing_points()[0], (self.heading_x, self.heading_y), (self.heading_x * missile_speed, self.heading_y * missile_speed), self.deployed_missiles, math.pi * 5 / 7, (-self.heading_y, self.heading_x))
                    right_missile = Missile(game, self.get_wing_points()[1], (self.heading_x, self.heading_y), (self.heading_x * missile_speed, self.heading_y * missile_speed), self.deployed_missiles, -math.pi * 5 / 7, (self.heading_y, -self.heading_x))
                    game.objects.add(left_missile, right_missile)
                    self.deployed_missiles.add(left_missile, right_missile)
                else:
                    for missile in self.deployed_missiles:
                        missile.turn()
            elif event.key == pygame.K_a:
                
                if len(self.deployed_torpedos_left) > 0:
                    for torpedo in self.deployed_torpedos_left:
                        torpedo.turn()
                else:
                    self.fire_torpedo_salvo(game, 6, self.deployed_torpedos_left)

            elif event.key == pygame.K_d:
                if len(self.deployed_torpedos_right) > 0:
                    for torpedo in self.deployed_torpedos_right:
                        torpedo.turn()
                else:
                    self.fire_torpedo_salvo(game, -6, self.deployed_torpedos_right)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.is_thrusting = False
            elif event.key == pygame.K_w:
                pass
                # self.is_shooting = False

    def fire_torpedo_salvo(self, game, torpedo_speed, owner_list):
        def fire_torpedo():
            trajectory = (self.heading_y * torpedo_speed, -self.heading_x * torpedo_speed)

            torpedo = Torpedo(game, self.rect.center,(self.heading_x, self.heading_y), trajectory, owner_list)
            game.objects.add(torpedo)
            owner_list.add(torpedo)

        fire_torpedo()
        # Timer(0.1, fire_torpedo).start()
        Timer(0.2, fire_torpedo).start()
        # Timer(0.3, fire_torpedo).start()
        Timer(0.4, fire_torpedo).start()

    def update(self, game):

        # point to mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.heading_x, self.heading_y = normalize((mouse_x - self.rect.centerx, mouse_y - self.rect.centery))

        if self.is_thrusting:
            # accelerate
            self.speed_x += self.heading_x * self.accel_force
            self.speed_y += self.heading_y * self.accel_force

            # enforce speed limit
            total_speed = get_magnitude((self.speed_x, self.speed_y))
            if total_speed > self.max_speed:
                self.speed_x, self.speed_y = normalize((self.speed_x, self.speed_y), self.max_speed)
        else:
            # decelerate
            total_speed = get_magnitude((self.speed_x, self.speed_y))
            if total_speed > 0:
                self.speed_x, self.speed_y = normalize((self.speed_x, self.speed_y), total_speed - self.decel_force)

        # move to new position
        super().update(game)

        # ballern
        if self.is_shooting:
            self.shooting_time += 1
            if self.shooting_time % self.shoot_frequency == 0:
                bullet_speed = 50
                bullet = Bullet(game, self.get_front_point(), (self.heading_x, self.heading_y), (self.heading_x * bullet_speed, self.heading_y * bullet_speed))
                game.objects.add(bullet)
            if self.shooting_time == self.shoot_frequency * self.burst_size:
                self.is_shooting = False
        
        # move to other side if outside border
        border = 0
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        outside_left, outside_right, outside_bottom, outside_top = is_outside_bounds(self.rect, (0, 0), (screen_width, screen_height))

        if outside_left:
            self.x = screen_width - 100
            self.rect.x = self.x
        elif outside_right:
            self.x = border
            self.rect.x = self.x
        elif outside_bottom:
            self.y = screen_height - border
            self.rect.y = self.y
        elif outside_top:
            self.y = border
            self.rect.y = self.y

    def render(self):
        if len(self.deployed_missiles) < 2:
            # draw missiles if they are not deployed
            missile_img = textures["missile"]
            left_missile_point, right_missile_point = self.get_wing_points()
            angle = self.get_angle()
            
            render_around_center(self.screen, missile_img, missile_img.get_rect(center=left_missile_point), angle)
            render_around_center(self.screen, missile_img, missile_img.get_rect(center=right_missile_point), angle)

        super().render()

def second_player_event_handler(self, game, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            self.is_thrusting = True
        elif event.key == pygame.K_w:
            self.shooting_time = 0
            self.is_shooting = True
        elif event.key == pygame.K_e:
            if len(self.deployed_missiles) < 2:
                missile_speed = 5
                left_missile = Missile(game, self.get_wing_points()[0], (self.heading_x, self.heading_y), (self.heading_x * missile_speed, self.heading_y * missile_speed), self.deployed_missiles, 2.0, (-self.heading_y, self.heading_x))
                right_missile = Missile(game, self.get_wing_points()[1], (self.heading_x, self.heading_y), (self.heading_x * missile_speed, self.heading_y * missile_speed), self.deployed_missiles, -2.0, (self.heading_y, -self.heading_x))
                game.objects.add(left_missile, right_missile)
                self.deployed_missiles.add(left_missile, right_missile)
            else:
                for missile in self.deployed_missiles:
                    missile.turn()
        elif event.key == pygame.K_a:
            
            if len(self.deployed_torpedos_left) > 0:
                for torpedo in self.deployed_torpedos_left:
                    torpedo.turn()
            else:
                self.fire_torpedo_salvo(game, 6, self.deployed_torpedos_left)

        elif event.key == pygame.K_d:
            if len(self.deployed_torpedos_right) > 0:
                for torpedo in self.deployed_torpedos_right:
                    torpedo.turn()
            else:
                self.fire_torpedo_salvo(game, -6, self.deployed_torpedos_right)

    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_SPACE:
            self.is_thrusting = False
        elif event.key == pygame.K_w:
            pass
            # self.is_shooting = False