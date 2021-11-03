from game_object.prototype import GameObject
from assets import textures
from util import is_outside_bounds

class Enemy(GameObject):
    def __init__(self, game, spawn_point, spawn_heading, spawn_speed):
        super().__init__(game, spawn_point, spawn_heading, spawn_speed, textures["enemy"], [ "enemy" ], False)
        self.health = 5
    
    def hit(self, game, damage):
        self.health -= damage
        if self.health <= 0:
            self.remove(game)
            game.add_score(1)

    def update(self, game):
        super().update(game)
        a, b, c, d = is_outside_bounds(self.rect, (0, 0), (self.screen.get_width(), self.screen.get_height()))
        if a or b  or d:
            self.remove(game)