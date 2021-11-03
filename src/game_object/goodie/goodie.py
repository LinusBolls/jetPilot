from threading import Timer

from assets import textures
from game_object.prototype import GameObject

class Goodie(GameObject):
    def __init__(self, game, spawn_point, spawn_heading, spawn_speed):
        super().__init__(game, spawn_point, spawn_heading, spawn_speed, textures["speed_goodie"], [ "goodie", "speed_goodie" ])

        self.duration = 5.0
    
    def activate(self, game):

        max_speed_boost = 5
        accel_force_boost = 0.4
        decel_force_boost = 0.2

        game.player.max_speed += max_speed_boost
        game.player.accel_force += accel_force_boost
        game.player.decel_force += decel_force_boost

        def reset_goodie_effect():
            game.player.max_speed -= max_speed_boost
            game.player.accel_force -= accel_force_boost
            game.player.decel_force -= decel_force_boost
          
        Timer(self.duration, reset_goodie_effect).start()