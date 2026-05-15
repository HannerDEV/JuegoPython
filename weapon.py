import pygame

class shotgun():
    def __init__(self, image):
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.shape = self.image.get_rect()

    def update(self, player):
        self.shape.center = player.shape.center
        
        if player.flip:
            self.shape.x -= player.shape.width/2
            self.rotar_arma(True)

        else:
            self.shape.x += player.shape.width/2
            self.rotar_arma(False)

    def rotar_arma(self, rotar):
        imagen_flip = pygame.transform.flip(self.original_image,
                                            rotar, False)
        self.image = pygame.transform.rotate(imagen_flip, self.angle)


    def draw(self, interface):
        interface.blit(self.image, self.shape)
        #pygame.draw.rect(interface, constants.DOG_COLOR , self.shape, 1)