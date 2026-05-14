import pygame
import constants
from personajes import Perro

player = Perro(750, 50)

pygame.init()

window = pygame.display.set_mode(constants.SIZE_VENTANA)
pygame.display.set_caption("SapoPerro")

move_left = False
move_right = False
move_up = False
move_down = False


#controla famerate
clock = pygame.time.Clock()


run = True 

while run:
    clock.tick(constants.FPS)

    window.fill(constants.BG_COLOR)

    for event in pygame.event.get():

        #cerrar el juego
        if event.type == pygame.QUIT:
            run = False

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



    #calcular el movimiento del jugador
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


    player.draw(window)

    
    pygame.display.update()


pygame.quit()