from pygame.sprite import Sprite
import pygame.sprite

class Damage_text(Sprite):
    def __init__(self, x, y, damage, font, color):
        Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.contador = 0
    def update(self):
        self.rect.y -= 2
        self.contador += 1
        if self.contador > 30:
            self.kill()