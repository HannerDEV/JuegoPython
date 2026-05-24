import pygame
import constants
import math
import random


class shotgun():
    def __init__(self, image, bullet_image, lista_enemigos):
        self.lista_enemigos = lista_enemigos
        self.original_image = image
        self.bullet_image = bullet_image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks()


    def update(self, player):
        
        shot_cooldown = constants.COOLDOWN_BULLETS
        bullet = None
        self.rect.center = player.rect.center
        
        if player.flip:
            self.rect.x -= player.rect.width/2
            self.rotar_arma(True)

        else:
            self.rect.x += player.rect.width/2
            self.rotar_arma(False)

        mouse_position = pygame.mouse.get_pos()
        distancia_x = mouse_position[0] - self.rect.centerx
        distancia_y = -mouse_position[1] + self.rect.centery
        self.angle = math.degrees(math.atan2(distancia_y, distancia_x))

        if pygame.mouse.get_pressed()[0] and self.fired == False and (pygame.time.get_ticks()- self.last_shot >= shot_cooldown):
            bullet = Bullet(self.bullet_image, self.rect.centerx, self.rect.centery, self.angle, self.lista_enemigos)
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
        interface.blit(self.image, self.rect)
        #pygame.draw.rect(interface, constants.DOG_COLOR , self.shape, 1)

    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle, lista_enemigos):
        self.lista_enemigos = lista_enemigos
        super().__init__()
        self.image_original = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.image_original, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.delta_x = math.cos(math.radians(self.angle)) * constants.BULLET_SPEED
        self.delta_y = -math.sin(math.radians(self.angle)) * constants.BULLET_SPEED

    def update(self):
        damage = 0
        pos_damage = None
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y

        #verificar salida de la pantalla
        if self.rect.right < 0 or self.rect.left > constants.WIDTH_WINDOW or self.rect.bottom < 0 or self.rect.top > constants.HEIGHT_WINDOW:
            self.kill()

        #verificar colisiones
        for ene in self.lista_enemigos:
            if ene.rect.colliderect(self.rect):
                damage = constants.BASE_DAMAGE + random.randint(-constants.RANDOM_VARIATION, constants.RANDOM_VARIATION)
                pos_damage = ene.rect
                ene.health -= damage
                self.kill()
                break
        return damage, pos_damage

            

    def draw(self, interface):
        interface.blit(self.image, (self.rect.centerx,
                       self.rect.centery - self.image.get_height()/2))