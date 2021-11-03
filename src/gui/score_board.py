import pygame
import pygame.ftfont

class ScoreBoard:

    def __init__(self, game, score, lvl):
  
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.width = self.screen.get_width()
        self.height = 96
      
        self.background_color = None
        self.text_color = (0, 0, 0)
        self.small_font = pygame.ftfont.SysFont(None, 30)
        self.fat_font = pygame.ftfont.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen.get_rect().centerx

        self.update(score, lvl)

    def update(self, score, lvl):
        self.score_img = self.fat_font.render(str(score), True, self.text_color)
        self.score_img_rect = self.score_img.get_rect(center=self.rect.center)

        self.lvl_img = self.small_font.render(str(lvl), True, self.text_color)
        self.lvl_img_rect = self.lvl_img.get_rect(centerx=self.rect.centerx, centery=self.rect.centery + 30)

    def render(self):
        self.screen.blit(self.score_img, self.score_img_rect)
        self.screen.blit(self.lvl_img, self.lvl_img_rect)

# self.play_button = PlayButton(self, "Play")
# self.play_button.render()
# button_clicked = self.play_button.rect.collidepoint(mouse_pos)