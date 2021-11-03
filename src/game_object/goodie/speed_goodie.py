from game_object.goodie.prototype import Goodie

class SpeedGoodie(Goodie):
    def __init__(self, game, spawn_point, spawn_heading, spawn_speed):
        super().__init__(game, spawn_point, spawn_heading, spawn_speed, textures["speed_goodie"], [ "goodie", "speed_goodie" ])

        self.max_speed_boost = 5
        self.accel_force_boost = 0.4
        self.decel_force_boost = 0.2
    
    def activate(self, game):

        game.player.max_speed += self.max_speed_boost
        game.player.accel_force += self.accel_force_boost
        game.player.decel_force += self.decel_force_boost

        super().activate(game)

    def deactivate(self, game):

        game.player.max_speed -= self.max_speed_boost
        game.player.accel_force -= self.accel_force_boost
        game.player.decel_force -= self.decel_force_boost