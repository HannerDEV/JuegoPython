import pygame
import constants

class Perro():
    def __init__(self, x, y):
        self.shape = pygame.Rect(0,0, 
                                 constants.WIDTH_DOG, constants.HEIGHT_DOG )
        self.shape.center = (x,y)

    def movement(self, delta_x, delta_y):
        self.shape.x = self.shape.x + delta_x
        self.shape.y = self.shape.y + delta_y

    def draw(self, interface):
        pygame.draw.rect(interface, constants.DOG_COLOR , self.shape)