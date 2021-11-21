import math

import pygame

def resize_to_width(raw_img, width):
    new_height = math.floor(raw_img.get_height() * (width / raw_img.get_width()))
    return pygame.transform.scale(raw_img, (width, new_height)).convert_alpha()

def resize_to_height(raw_img, height):
    new_width = math.floor(raw_img.get_width() * (height/ raw_img.get_height()))
    return pygame.transform.scale(raw_img, (new_width, height)).convert_alpha()

def is_outside_bounds(rect, lower_left_corner, upper_right_corner):

    outside_left = rect.left <= lower_left_corner[0]
    outside_right = rect.right >= upper_right_corner[0]
    outside_bottom = rect.bottom <= lower_left_corner[1]
    outside_top = rect.top >= upper_right_corner[1]

    return (outside_left, outside_right, outside_bottom, outside_top)

def get_magnitude(vector):
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2)

def normalize(vector, target_magnitude=1):
    magnitude = max(get_magnitude(vector), 0.1)
    target_magnitude = max(target_magnitude, 0.1)
    return (vector[0] / (magnitude / target_magnitude), vector[1] / (magnitude / target_magnitude))

def render_around_center(screen, img, rect, angle):

    rotated_img = pygame.transform.rotate(img, angle)
    new_rect = rotated_img.get_rect(center=rect.center)

    screen.blit(rotated_img, new_rect)

def play_sound(dateiname):
    pygame.mixer.find_channel(True).play(pygame.mixer.Sound("game_sounds/" + dateiname))