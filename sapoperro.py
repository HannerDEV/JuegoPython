import pygame
import constants
from characters import Character
import characters
from items import Item
import pytmx
import map
from enemies import GroundEnemy
from enemies import FlyingEnemy
from enemies import WaterEnemy

pygame.init()
pygame.mixer.init()

print(pygame.sprite)

window = pygame.display.set_mode(constants.SIZE_WINDOW)
pygame.display.set_caption("SapoPerro")

pygame.mixer.music.load("Assets/Music/Feel Good Inc. [8 Bit Tribute to Gorillaz] - 8 Bit Universe.mp3")
pygame.mixer.music.play(-1)

tmx_data = pytmx.load_pygame("game_maps/mapa.tmx")
collision_rects = map.load_collisions(tmx_data)



font = pygame.font.Font("Assets/Fonts/PixeloidSans-Bold.ttf", constants.FONT_SIZE)


def dibujar_texto(text, font, color, x, y) :
    img = font.render(text, True, color)
    window.blit(img,(x, y))

#Personaje
frames_dog = {
    "Idle":[],
    "Walk":[],
    "Attack":[],
    "Hurt":[],
    "Death":[],
    "Jump":[]
              }

#Cargar animaciones del perro
characters.load_animations(frames_dog, "Assets/Images/Characters/Perro/Attack.png", "Attack", 4)
characters.load_animations(frames_dog, "Assets/Images/Characters/Perro/Death.png", "Death", 4)
characters.load_animations(frames_dog, "Assets/Images/Characters/Perro/Hurt.png", "Hurt", 2)
characters.load_animations(frames_dog, "Assets/Images/Characters/Perro/Idle.png", "Idle", 4)
characters.load_animations(frames_dog, "Assets/Images/Characters/Perro/Walk.png", "Walk", 6)
jump_frame = characters.load_image("Assets/Images/Characters/Perro/Jump.png", constants.PLAYER_SCALE)
frames_dog["Jump"] = [jump_frame]

player = Character(constants.INITIAL_POSITION_X_PLAYER, constants.INITIAL_POSITION_Y_PLAYER, frames_dog, constants.PLAYER_HEALTH)

#Enemigos
frames_sword_fish = {
    "Idle":[],
    "Walk":[],
    "Attack":[],
    "Hurt":[],
    "Death":[]
              }

#Cargar animaciones del pez espada
characters.load_animations(frames_sword_fish , "Assets\Images\Characters\Enemies\SwordFish\Attack.png", "Attack", 6)
characters.load_animations(frames_sword_fish , "Assets\Images\Characters\Enemies\SwordFish\Death.png", "Death", 6)
characters.load_animations(frames_sword_fish , "Assets\Images\Characters\Enemies\SwordFish\Hurt.png", "Hurt", 2)
characters.load_animations(frames_sword_fish , "Assets\Images\Characters\Enemies\SwordFish\Idle.png", "Idle", 4)
characters.load_animations(frames_sword_fish , "Assets\Images\Characters\Enemies\SwordFish\Walk.png", "Walk", 4)

#Se crea grupo de enemigos
enemies_group = pygame.sprite.Group()
sword_fish = WaterEnemy(10000, 3700, frames_sword_fish)
enemies_group.add(sword_fish)


#Heart
frames_heart = []

full_heart = pygame.image.load("Assets/Images/Items/hearth/corazon_lleno.png").convert_alpha()
full_heart = pygame.transform.scale_by(full_heart, constants.HEART_SCALE)
for i in range(5):
    hurt_heart = pygame.image.load(f"Assets/Images/Items/hearth/corazon_daño{i+1}.png").convert_alpha()
    hurt_heart = pygame.transform.scale_by(hurt_heart, constants.HEART_SCALE)
    frames_heart.append(hurt_heart)

#Coins

coin_images = []
for i in range(9):
    img = pygame.image.load(f"Assets/Images/Items/coin/moneda{i}.png").convert_alpha()
    img = pygame.transform.scale_by(img, constants.SCALE_COIN)
    coin_images.append(img)

#Guaro

schnapp_image = pygame.image.load("Assets/Images/Items/Bebidas/Guaro.png").convert_alpha()
schnapp_image = pygame.transform.scale_by(schnapp_image , constants.SCHNAPSS_SCALE)

#Aguila

beverage_image = pygame.image.load("Assets/Images/Items/Bebidas/Aguila.png").convert_alpha()
beverage_image = pygame.transform.scale_by(beverage_image, constants.BEVERAGE_SCALE)







#shotgun = shotgun(shotgun_image, bullet_image, enemy_list)

#Crear un grupo de sprites

text_damage_group = pygame.sprite.Group()
items_group = pygame.sprite.Group()


coin = Item(230, 230, 0, coin_images)
schnapps = Item(400, 260, 1, [schnapp_image])
beverage = Item(600, 280, 2, [beverage_image])
items_group.add(coin)
items_group.add(schnapps)
items_group.add(beverage)

#Funcion de vida

def player_life():
    for i in range(4):

        heart_health = player.health - (i * 25)

        if heart_health >= 25:
            image = full_heart
            image= pygame.transform.scale_by(image, constants.HEART_SCALE)

        elif heart_health > 0:
            damage = 25 - heart_health
            frame = damage // 5
            image = frames_heart[frame]

            image= pygame.transform.scale_by(image, constants.HEART_SCALE)

        else:
            continue

        window.blit(image, (5 + i * constants.HEART_SEPARATION, 5))


#controla framerate
Framerate = pygame.time.Clock()


run = True 

columnas = tmx_data.width
filas = tmx_data.height
tile_size = tmx_data.tilewidth

MAPA_ANCHO = 38400
MAPA_ALTO = 4000   
GROSOR_PARED = 150

pared_izquierda = pygame.Rect(-GROSOR_PARED, 0, GROSOR_PARED, MAPA_ALTO)
pared_derecha   = pygame.Rect(MAPA_ANCHO, 0, GROSOR_PARED, MAPA_ALTO)
techo_invisible = pygame.Rect(0, -GROSOR_PARED, MAPA_ANCHO, GROSOR_PARED)

collision_rects.append(pared_izquierda)
collision_rects.append(pared_derecha)
collision_rects.append(techo_invisible)


while run:

    dt = Framerate.tick(constants.FPS) / 1000.0
    Framerate.tick(constants.FPS)


    for event in pygame.event.get():

        #cerrar el juego
        if event.type == pygame.QUIT:
            run = False


    #mover la camara
    camera_x = int((player.rect.centerx - constants.WIDTH_WINDOW // 2) + 250)
    camera_y = int((player.rect.centery - constants.HEIGHT_WINDOW // 2) - 100)

    window.fill((0, 0, 0))

    #Dibujar mapa, como primera capa
    map.draw_map(tmx_data, window, camera_x, camera_y)
    
    #mover al jugador
    dx, moving, attacking = player.move(collision_rects, dt)

    #actualizar estados

    player.update(dt, moving, attacking)
    player.check_attack(enemies_group)
    enemies_group.update(dt, player.rect, collision_rects, player)
    text_damage_group.update()
    items_group.update(player)

    player.draw(window, camera_x, camera_y)
    
    for ene in enemies_group:
        screen_pos_x = ene.rect.x - camera_x
        screen_pos_y = ene.rect.y - camera_y
        window.blit(ene.image, (screen_pos_x, screen_pos_y))


    text_damage_group.draw(window)
    if player.action == "Attack" and hasattr(player, 'attack_rect') and player.attack_rect is not None:
        pygame.draw.rect(window, (255, 255, 255), (player.attack_rect.x - camera_x, player.attack_rect.y - camera_y, player.attack_rect.width, player.attack_rect.height), 2)


    #items_group.draw(window)

    #map.draw_colliders(collision_rects, window, camera_x, camera_y)

    pygame.draw.rect(window, (0, 0, 0), (pared_izquierda.x - camera_x, pared_izquierda.y - camera_y, pared_izquierda.width, pared_izquierda.height))
    pygame.draw.rect(window, (0, 0, 0), (pared_derecha.x - camera_x, pared_derecha.y - camera_y, pared_derecha.width, pared_derecha.height))
    pygame.draw.rect(window, (0, 0, 0), (techo_invisible.x - camera_x, techo_invisible.y - camera_y, techo_invisible.width, techo_invisible.height))

    
    dibujar_texto(f"Score: {player.score}", font, constants.YELLOW, constants.POSITION_X_SCORE, constants.POSITION_Y_SCORE)

    #Definir la vida del jugador
    player_life()

    pygame.display.update()

    
    
pygame.quit()