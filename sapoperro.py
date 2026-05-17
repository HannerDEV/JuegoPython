import pygame
import constants
from characters import Character
from weapon import shotgun
import os

pygame.init()

print(pygame.sprite)


window = pygame.display.set_mode(constants.SIZE_WINDOW)
pygame.display.set_caption("SapoPerro")

def scale_image(image, scale):
    w = image.get_width()*scale
    h = image.get_height()*scale
    new_image = pygame.transform.scale(image,(w*scale, h*scale))
    return new_image

def count_elements(directory):
    return len(os.listdir(directory))

def listar_nombres_carpetas(directory):
    return os.listdir(directory)

#Personaje
frames_dog = []


for i in range (6):
    dog = pygame.image.load(f"Assets/Images/Characters/Perro/image{i}.png").convert_alpha()
    dog = scale_image(dog, constants.PLAYER_SCALE)
    frames_dog.append(dog)

#Arma
shotgun_image = pygame.image.load("Assets/Images/Weapons/escopeta.png").convert_alpha()
shotgun_image = scale_image(shotgun_image, constants.SHOTGUN_SCALE)

#Bala
bullet_image = pygame.image.load("Assets/Images/Weapons/bullet.png").convert_alpha()
bullet_image = scale_image(bullet_image, constants.BULLET_SCALE)

#Enemigo
enemy_directory = "Assets/Images/Characters/Enemies"
enemy_type = listar_nombres_carpetas(enemy_directory)
enemy_animation = []

for eni in enemy_type:
    lista_temp = []
    temp_root = f"Assets/Images/Characters/Enemies/{eni}"
    num_animations = count_elements(temp_root)
    for i in range(num_animations):
        enemy_image = pygame.image.load(f"{temp_root}/{eni}{i}.png").convert_alpha()
        enemy_image = scale_image(enemy_image, constants.DOG_BARK_SCALE)
        lista_temp.append(enemy_image)
    enemy_animation.append(lista_temp)

player = Character(constants.INITIAL_POSITION_X, constants.INITIAL_POSITION_Y, frames_dog)
shotgun = shotgun(shotgun_image, bullet_image)
enemy_one = Character(400, 400, enemy_animation[0])
enemy_two = Character(300, 200, enemy_animation[0])

#lista de enemigos

enemy_list = []
enemy_list.append(enemy_one)
enemy_list.append(enemy_two)

#Crear un grupo de sprites

bullets_group = pygame.sprite.Group()

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
        delta_x = constants.SPEED
    if move_left:
        delta_x = -constants.SPEED
    if move_up:
        delta_y = -constants.SPEED
    if move_down:
        delta_y = constants.SPEED

    #mover al jugador

    player.movement(delta_x, delta_y)

    #actualizar estados
    player.update()
    bullet = shotgun.update(player)
    for ene in enemy_list:
        ene.update()
        

    if bullet:
        bullets_group.add(bullet)
    for bullet in bullets_group:
        bullet.update()

    #Dibujar elementos
    player.draw(window)
    shotgun.draw(window)
    for bullet in bullets_group:
        bullet.draw(window)
    for ene in enemy_list:
        ene.draw(window)

    
    pygame.display.update()
    
pygame.quit()