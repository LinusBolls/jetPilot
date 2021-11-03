from threading import Timer
from random import randint
import math
import sys

import pygame

import assets
from game_object.player import Player, second_player_event_handler
from game_object.enemy.enemy import Enemy
from game_object.goodie.goodie import Goodie
from game_object.projectile.missile import Missile
from game_object.explosion.explosion import Explosion
from gui.play_button import PlayButton
from gui.score_board import ScoreBoard

def resize_to_height(raw_img, height):
    new_width = math.floor(raw_img.get_width() * (height/ raw_img.get_height()))
    return pygame.transform.scale(raw_img, (new_width, height)).convert_alpha()

def collide_enemy_bullet(game, enemy, bullet):
    bullet.remove(game)
    enemy.hit(game, 1)

def collide_enemy_explosion(game, enemy, explosion):
    enemy.hit(game, explosion.damage)

def collide_enemy_missile(game, enemy, missile):
    missile.remove(game)
    enemy.hit(game, 5)

def collide_enemy_torpedo(game, enemy, torpedo):
    torpedo.remove(game)
    explosion = Explosion(game, torpedo.rect.center, 300, 10)
    game.objects.add(explosion)

def collide_player_enemy(game, player, enemy):
    game.is_running = False
    game.play_button.set_text("Wasted (3)")
    Timer(1.0, game.play_button.set_text, ["Wasted (2)"]).start()
    Timer(2.0, game.play_button.set_text, ["Wasted (1)"]).start()
    Timer(3.0, game.start).start()

def collide_player_goodie(game, player, goodie):
    goodie.remove(game)
    goodie.activate(game)
    pygame.mixer.find_channel(True).play(assets.sounds["pickup_goodie"])

def collide(game, obj_1, obj_2, tag_1, tag_2, func):
    if tag_1 in obj_1.tags and tag_2 in obj_2.tags:
        func(game, obj_1, obj_2)
        return True
    elif tag_1 in obj_2.tags and tag_2 in obj_1.tags:
        func(game, obj_2, obj_1)
        return True
    return False

class Game:

    def spawn_structure(self, spawn_point, structure):
        for row_num, row in enumerate(structure):
            for type_num, type in enumerate(row):
                if type == 1:
                    enemy = Enemy(self, (spawn_point[0] + type_num * 100, spawn_point[1] + row_num * 100), (0, -1), (0, 0))
                    self.objects.add(enemy)

    def start(self):
        self.camera_speed = 4
        self.score = 0
        self.lvl = 0

        self.objects.empty()
        self.has_two_players = False

        self.player = Player(self, (self.screen.get_width() / 2, self.screen.get_height() / 4 * 3), (0, -1), (0, -12))
        self.objects.add(self.player)

        if self.has_two_players:
            self.player2 = Player(self, (self.screen.get_width() / 4 * 3, self.screen.get_height() / 4 * 3), (0, -1), (0, -12))
            self.player2.handle_event = lambda game, event : second_player_event_handler(self.player2, game, event)
            self.objects.add(self.player2)
        
        self.play_button.set_text("Play [Enter]")
        self.score_board.update(0, 0)

    def __init__(self):

        self.is_running = False
        self.is_debug_mode = True

        self.current_collisions = []
  
        pygame.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.objects = pygame.sprite.Group()

        assets.load(self.screen.get_height())

        pygame.display.set_caption("Jet")
        pygame.display.set_icon(pygame.image.load("../assets/textures/game_icon.png"))

        self.clock = pygame.time.Clock()

        self.play_button = PlayButton(self, "Play [Enter]")
        self.score_board = ScoreBoard(self, 0, 0)

        pygame.mouse.set_visible(False)

        self.start()

    def spawn_smth(self, smth):
        enemy = smth(self, (randint(0, self.screen.get_width()), -50), (0, -1), (0, 0))
        self.objects.add(enemy)

    def add_score(self, score):
        this_lvl = math.floor(self.score / 20)
        self.score += score
        next_lvl = math.floor(self.score / 20)

        if this_lvl != next_lvl:
            self.lvl += 1
            self.player.max_speed += 1
            if self.has_two_players:
                self.player2.max_speed += 1
            self.camera_speed += 1
        
        self.score_board.update(self.score, self.lvl)

    def run_game(self):

        while True:

            if self.is_running:

                camera_movement = (0, self.camera_speed)
                # camera_movement = (0, 0)

                if randint(0, 60) == 0:
                    self.spawn_smth(Enemy)
                if randint(0, 600) == 0:
                    structure = [[1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1]]
                    self.spawn_structure((randint(1, self.screen.get_width() - len(structure[0]) * 100 - 1), 0 - len(structure) * 100), structure)
                elif randint(0, 600) == 0:
                    self.spawn_smth(Goodie)

                for obj in self.objects:
                    obj.y += camera_movement[1]
                    obj.rect.y += camera_movement[1]
                    obj.update(self)

            for event in pygame.event.get():
                enter_pressed = event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN
                play_button_pressed = event.type == pygame.MOUSEBUTTONDOWN and self.play_button.rect.collidepoint(pygame.mouse.get_pos())

                if enter_pressed or play_button_pressed:
                    self.is_running = True

                if self.is_running:
                    self.player.handle_event(self, event)
                    if self.has_two_players:
                        self.player2.handle_event(self, event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        Missile.streckung_x += 0.1
                    elif event.key == pygame.K_RIGHT:
                        Missile.streckung_x -= 0.1
                    elif event.key == pygame.K_UP:
                        Missile.streckung_y += 0.1
                    elif event.key == pygame.K_DOWN:
                        Missile.streckung_y -= 0.1
                    elif event.key == pygame.K_q:
                        sys.exit(0)

            if self.is_running:
                for obj_1 in self.objects:
                    obj_2 = pygame.sprite.spritecollideany(obj_1, self.objects)
                    if obj_2 and obj_2 != obj_1: # and {obj_1, obj_2} not in self.current_collisions

                        # print(f"{ obj_1 } - { obj_2 }")

                        self.current_collisions.append({obj_1, obj_2})

                        collide(self, obj_1, obj_2, "enemy", "bullet", collide_enemy_bullet)
                        collide(self, obj_1, obj_2, "enemy", "missile", collide_enemy_missile)
                        collide(self, obj_1, obj_2, "enemy", "torpedo", collide_enemy_torpedo)
                        collide(self, obj_1, obj_2, "player", "enemy", collide_player_enemy)
                        collide(self, obj_1, obj_2, "player", "goodie", collide_player_goodie)
                        collide(self, obj_1, obj_2, "enemy", "explosion", collide_enemy_explosion)

            self.screen.fill((255, 255, 255))

            for obj in self.objects:
                obj.render()

            if not self.is_running:
                self.play_button.render()
            self.score_board.render()

            self.screen.blit(assets.textures["crosshair"], assets.textures["crosshair"].get_rect(center=pygame.mouse.get_pos()))

            pygame.display.flip()

            self.clock.tick(60)

if __name__ == "__main__":
    Game().run_game()

# hitbox masks
# hitbox centering
# fix jet twitching when mouse directly over it

# explosions
# fix missiles
# give torpedo forward speed


