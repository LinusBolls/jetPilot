import random
from game_object.prototype import GameObject

class Particle(GameObject):
    def __init__(self, game, spawn_point, texture, tags, lifespan):
        super().__init__(game, spawn_point, (1, 0), (0, 0), texture, tags)
        self.time_alive = 0
        self.lifespan = lifespan
    
    def update(self, game):
        super().update(game)
        self.time_alive += 1
        if self.time_alive > self.lifespan:
            self.remove(game)