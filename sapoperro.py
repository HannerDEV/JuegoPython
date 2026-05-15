import pygame
import constants
from characters import Dog
from weapon import shotgun

pygame.init()

window = pygame.display.set_mode(constants.SIZE_VENTANA)
pygame.display.set_caption("SapoPerro")

def scale_image(image, scale):
    w = image.get_width()*constants.PLAYER_SCALE
    h = image.get_height()*constants.PLAYER_SCALE
    new_image = pygame.transform.scale(image,(w*scale, h*scale))
    return new_image

#Personaje
frames_dog = []

for i in range (2):
    dog = pygame.image.load(f"Assets/Images/Characters/Perro/image{i}.png")
    dog = scale_image(dog, constants.PLAYER_SCALE)
    frames_dog.append(dog)

#Arma
shotgun_image = pygame.image.load("Assets/Images/Weapons/escopeta.png")
shotgun_image = scale_image(shotgun_image, constants.SHOTGUN_SCALE)

player = Dog(constants.POSICION_INICIAL_X, constants.POSICION_INICIAL_Y, dog, frames_dog)
shotgun = shotgun(shotgun_image)

#Define variables de movimiento
move_left = False
move_right = False
move_up = False
move_down = False


#controla framerate
Framerate = pygame.time.Clock()


run = True 

while run:
    Framerate.tick(constants.FPS)

    window.fill(constants.BG_COLOR)

    for event in pygame.event.get():

        #cerrar el juego
        if event.type == pygame.QUIT:
            run = False

        #tecla oprimida
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_w:
                move_up = True
            if event.key == pygame.K_s: 
                move_down = True

        #tecla soltada
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False
            if event.key == pygame.K_w:
                move_up = False
            if event.key == pygame.K_s: 
                move_down = False



    #movimiento del jugador
    delta_x = 0
    delta_y = 0

    if move_right:
        delta_x = constants.VELOCIDAD
    if move_left:
        delta_x = -constants.VELOCIDAD
    if move_up:
        delta_y = -constants.VELOCIDAD
    if move_down:
        delta_y = constants.VELOCIDAD

    #mover al jugador

    player.movement(delta_x, delta_y)

    #actualizar estados
    player.update()
    shotgun.update(player)

    #Dibujar elementos
    player.draw(window)
    shotgun.draw(window)

    
    pygame.display.update()
    
pygame.quit()