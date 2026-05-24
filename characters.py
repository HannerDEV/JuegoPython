import pygame
import constants
import os

#Puntaje
#enemigos
#gameover
#pantalla de inicio
#sonidos
#colision con pinchos
#bebidas con vida
#Encapsulamiento
#Polimorfismo
#clases abstractas
#documento


def load_animations(animations, png, name, num):
    spritesheet = pygame.image.load(png).convert_alpha()

    frame_width = 48
    frame_height = 25

    cols = spritesheet.get_width() // frame_width

    for i in range(num):


        x = (i % cols) * frame_width

        y =(i // cols) * frame_height

        frame = spritesheet.subsurface(
            (x, y, frame_width, frame_height)
        )

        frame = pygame.transform.scale_by(frame, constants.PLAYER_SCALE)

        animations[name].append(frame)

def load_image(png, scale=1):
    img = pygame.image.load(png).convert_alpha()
    img = pygame.transform.scale_by(img, scale)
    return img


class Character():
    def __init__(self, x, y,frames_dog, health):
        self.animation_speed = 10.0
        self.fall_time = 0
        self.max_health = 100
        self.health = self.max_health
        self.action = "Idle"
        self.invulnerable = False
        self.invulnerability_duration = 0.8 
        self.invulnerable_timer = 0.0
        self.base_speed = 90
        self.current_speed = self.base_speed
        self.max_speed = 180
        self.acceleration = 0.1
        self.friction = 0
        self.jump_hold_time = 0
        self.jump_max_hold = 12  
        self.jump_cut_multiplier = 0.5
        self.jumping = False
        self.step_height = 70
        self.action = "Idle"
        self.velocity_y = 0
        self.gravity = 20
        self.jump_force = -120
        self.on_ground = False
        self.score = 0
        self.is_alive = True
        self.health = health
        self.flip = False
        self.animations = frames_dog
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animations[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.rect.width -= 30

        self.rect.height -= 10

    def move(self, collision_rects, dt):
        dx = 0
        attacking = False
        moving = False


        if self.invulnerable and self.action == "Hurt":

            if not hasattr(self, 'knockback_dir'):
                self.knockback_dir = 1 
            
            dx = self.knockback_dir * 8 
            
            self.rect.x += dx
            for tile in collision_rects:
                if self.rect.colliderect(tile):
                    if dx > 0:
                        self.rect.right = tile.left
                    elif dx < 0:
                        self.rect.left = tile.right
            
            return dx, moving, attacking

        if self.action != "Death":
            keys = pygame.key.get_pressed()

            if keys[pygame.K_j]:
                attacking = True

            if keys[pygame.K_a]:
                moving = True
                self.flip = True
                if self.on_ground:
                    self.current_speed = min(self.max_speed, self.current_speed + self.acceleration)
                dx = -self.current_speed
            elif keys[pygame.K_d]:
                moving = True
                self.flip = False
                if self.on_ground:
                    self.current_speed = min(self.max_speed, self.current_speed + self.acceleration)
                dx = self.current_speed
            else:
                if self.on_ground:
                    self.current_speed = max(self.base_speed, self.current_speed - self.friction)
                else:
                    self.current_speed = max(self.base_speed, self.current_speed - (self.friction * 0.5))

            if keys[pygame.K_SPACE] and self.on_ground:
                self.velocity_y = self.jump_force
                self.on_ground = False
                self.jumping = True
                self.jump_hold_time = 0

            if self.jumping:
                if keys[pygame.K_SPACE] and self.jump_hold_time < self.jump_max_hold:
                    self.velocity_y += -0.6
                    self.jump_hold_time += 1
                else:
                    if self.velocity_y < 0:
                        self.velocity_y *= self.jump_cut_multiplier
                    self.jumping = False

        if not self.on_ground and self.velocity_y > 1:
            self.fall_time += 1
        else:
            self.fall_time = 0

        if not self.on_ground and self.velocity_y > 0:
            self.velocity_y += self.gravity * 3.5
        else:
            self.velocity_y += self.gravity

        if self.velocity_y > 45:
            self.velocity_y = 45

        # Movimiento y colisión en X
        self.rect.x += dx
        for tile in collision_rects:
            if self.rect.colliderect(tile):
                original_y = self.rect.y
                self.rect.y -= self.step_height
                
                subida_bloqueada = False
                for other_tile in collision_rects:
                    if self.rect.colliderect(other_tile):
                        subida_bloqueada = True
                        break
                
                if subida_bloqueada:
                    self.rect.y = original_y
                    if dx > 0:
                        self.rect.right = tile.left
                    elif dx < 0:
                        self.rect.left = tile.right
                    self.current_speed = self.base_speed
                else:
                    self.velocity_y = 0
                    self.on_ground = True


        self.rect.y += self.velocity_y

        for tile in collision_rects:
            if self.rect.colliderect(tile):
                if self.velocity_y > 0:

                    if self.fall_time > 35:
                        self.health -= 25
                        self.invulnerable = True
                        self.frame_index = 0
                    
                    self.fall_time = 0  
                    self.rect.bottom = tile.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.rect.top = tile.bottom
                    self.velocity_y = 0

        return dx, moving, attacking
    
    def check_attack(self, enemies_group):
        if self.action == "Attack" and hasattr(self, 'attack_rect') and self.attack_rect is not None:
            for enemy in enemies_group:
                # comprobar colision
                if self.attack_rect.colliderect(enemy.rect):
                    if hasattr(enemy, 'action') and enemy.action != "Hurt" and enemy.action != "Death":
                        enemy.health -= 25 
                        enemy.action = "Hurt"
                        enemy.frame_index = 0
                        
                        if enemy.health <= 0:
                            enemy.action = "Death"
                            enemy.frame_index = 0

    def update(self, dt, moving, attacking):

        if self.invulnerable:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
        if self.health <= 0:
            self.action = "Death"
            self.is_alive = False
        elif self.invulnerable:
            self.action = "Hurt"
        elif attacking:
            self.action = "Attack"
            ancho_ataque = 140
            alto_ataque = self.rect.height
            
            if self.flip:
                self.attack_rect = pygame.Rect(self.rect.left - ancho_ataque, self.rect.y, ancho_ataque, alto_ataque)
            else: 
                self.attack_rect = pygame.Rect(self.rect.right, self.rect.y, ancho_ataque, alto_ataque)

        elif not self.on_ground:
            self.action = "Jump"
        elif moving:
            self.action = "Walk"
        else:
            self.action = "Idle"

        self.frame_index += self.animation_speed * dt
        current_frames = self.animations[self.action]

        if self.frame_index >= len(current_frames):
            if self.action == "Death" or self.action == "Hurt":
                self.frame_index = len(current_frames) - 1
            else:
                self.frame_index = 0

        self.image = current_frames[int(self.frame_index)]
        if self.flip:
            self.image = pygame.transform.flip(self.image, False, False)
    def take_damage(self, amount):
        if self.invulnerable or self.action == "Death":
            return

        
        self.health -= amount
        
        if self.health <= 0:
            self.health = 0
            self.action = "Death"
        else:
            self.action = "Hurt"
            self.invulnerable = True
            self.invulnerable_timer = self.invulnerability_duration


    def draw(self, interface, camera_x, camera_y):
        
        image_flip = pygame.transform.flip(self.image, self.flip, False)
        interface.blit(
            image_flip,
            (
            self.rect.x - camera_x,
            self.rect.y - camera_y
            )
        )


        '''pygame.draw.rect(
            interface,
            constants.DOG_COLOR,
            pygame.Rect(
                self.rect.x - camera_x,
                self.rect.y - camera_y,
                self.rect.width,
                self.rect.height
            ),
            1
        )'''
