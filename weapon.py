import pygame
import constants
import math


class shotgun():
    def __init__(self, image, bullet_image):
        self.original_image = image
        self.bullet_image = bullet_image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.shape = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks()


    def update(self, player):
        
        shot_cooldown = constants.COOLDOWN_BULLETS
        bullet = None
        self.shape.center = player.shape.center
        
        if player.flip:
            self.shape.x -= player.shape.width/2
            self.rotar_arma(True)

        else:
            self.shape.x += player.shape.width/2
            self.rotar_arma(False)

        mouse_position = pygame.mouse.get_pos()
        distancia_x = mouse_position[0] - self.shape.centerx
        distancia_y = -mouse_position[1] + self.shape.centery
        self.angle = math.degrees(math.atan2(distancia_y, distancia_x))

        if pygame.mouse.get_pressed()[0] and self.fired == False and (pygame.time.get_ticks()- self.last_shot >= shot_cooldown):
            bullet = Bullet(self.bullet_image, self.shape.centerx, self.shape.centery, self.angle)
            self.fired = True

        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False
        return bullet
                                  
    def rotar_arma(self, rotar):
        imagen_flip = pygame.transform.flip(self.original_image,
                                            rotar, False)
        self.image = pygame.transform.rotate(imagen_flip, self.angle)

    def draw(self, interface):
        #self.image = pygame.transform.rotate(self.image, self.angle)
        interface.blit(self.image, self.shape)
        #pygame.draw.rect(interface, constants.DOG_COLOR , self.shape, 1)

    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        super().__init__()
        self.image_original = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.image_original, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.delta_x = math.cos(math.radians(self.angle)) * constants.BULLET_SPEED
        self.delta_y = -math.sin(math.radians(self.angle)) * constants.BULLET_SPEED

    def update(self):
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y
        
        if self.rect.right < 0 or self.rect.left > constants.WIDTH_WINDOW or self.rect.bottom < 0 or self.rect.top > constants.HEIGHT_WINDOW:
            self.kill()
            

    def draw(self, interface):
        interface.blit(self.image, (self.rect.centerx,
                       self.rect.centery - self.image.get_height()/2))