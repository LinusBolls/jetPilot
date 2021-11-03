import pygame
import pygame.ftfont

class PlayButton:

    def __init__(self, game, text):
  
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.width = self.screen.get_width()
        self.height = 96
      
        self.background_color = pygame.Color(0, 0, 0, a=100)
        self.text_color = (255, 255, 255)
        self.font = pygame.ftfont.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen.get_rect().center

        self.set_text(text)

    def set_text(self, text):
        self.text = text
        self.msg_img = self.font.render(text, True, self.text_color, self.background_color)
        self.msg_img_rect = self.msg_img.get_rect(center=self.rect.center)

    def render(self):

        self.screen.fill(self.background_color, self.rect)
        self.screen.blit(self.msg_img, self.msg_img_rect)

# self.play_button = PlayButton(self, "Play")
# self.play_button.render()
# button_clicked = self.play_button.rect.collidepoint(mouse_pos)