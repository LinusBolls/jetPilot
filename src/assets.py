textures = {}
sounds = {}

def load(screen_height):
    import pygame

    from util import resize_to_height

    ASSET_PATH = "../assets/"
  
    global textures
    global sounds

    def load_texture(name, height, path=None):
        if path is None:
            path = name + ".png"
        path = ASSET_PATH + "textures/" + path
        textures[name] = resize_to_height(pygame.image.load(path), height)

    def load_sound(name, path=None):
        if path is None:
            path = name + ".mp3"
        path = ASSET_PATH + "sounds/" + path
        sounds[name] = pygame.mixer.Sound(path)

    load_texture("player", 100, "jet.png")
    load_texture("enemy", 50, "alien.png")
    load_texture("bullet", 20)
    load_texture("missile", 50)
    load_texture("torpedo", 30)
    load_texture("speed_goodie", 50, "game_icon.png")
    load_texture("crosshair", 20)
    load_texture("explosion_0", 500)
    load_texture("explosion_1", 20)
    load_texture("background", 2000, "background.jpg")

    load_sound("bullet")
    load_sound("torpedo")
    load_sound("missile")
    load_sound("pickup_ammo")
    load_sound("pickup_goodie")