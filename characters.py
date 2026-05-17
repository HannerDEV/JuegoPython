import pygame
import constants

class Character():
    def __init__(self, x, y,frames_dog):
        self.flip = False
        self.animations = frames_dog
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = frames_dog[self.frame_index]
        self.shape = self.image.get_rect()
        self.shape.center = (x,y)

    def movement(self, delta_x, delta_y):

        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False 

        self.shape.x += delta_x
        self.shape.y += delta_y
    
    def update(self):
        cooldown_animation = 100
        self.image = self.animations[self.frame_index]

        if pygame.time.get_ticks() - self.update_time >= cooldown_animation:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animations):
            self.frame_index = 0

    def draw(self, interface):
        image_flip = pygame.transform.flip(self.image, self.flip, False)
        interface.blit(image_flip,self.shape)
        #pygame.draw.rect(interface, constants.DOG_COLOR , self.shape, 1)