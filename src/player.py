from entity import Entity


class Player(Entity):
    def __init__(self, game, spawn_point, spawn_speed, spawn_heading):
        super().__init__(game, spawn_point, spawn_speed, spawn_heading, thing, [ "player", "gravity", "solid" ])