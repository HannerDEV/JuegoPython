import math
import random
from abc import ABC, abstractmethod
import pygame


class Enemy(pygame.sprite.Sprite, ABC):

    def __init__(self, x, y, width, height, health, damage, speed, detection_radius):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.inflate(-width * 0.2, -height * 0.1)
        self.max_health = health
        self.health = health
        self.damage_value = damage
        self.speed = speed
        self.detection_radius = detection_radius

        self.direction = 1
        self.state = "Idle"
        self.state_timer = 0.0

        self.animations = {
            "Idle": [self.image],
            "Walk": [self.image],
            "Attack": [self.image],
            "Hurt": [self.image],
            "Death": [self.image],
        }
        self.animation_index = 0.0
        self.animation_speed = 10.0

    def update(self, dt, player_rect, collision_rects, player):
        self.state_timer -= dt
        if self.state_timer <= 0 and self.state in ["Hurt", "Attack"]:
            self.state = "Walk"

        if self.state != "Dead":
            self.handle_states(player_rect)
            self.move(dt, collision_rects)
            self.hitbox.center = self.rect.center
            self.check_player_collision(player)

        self.animate(dt)

    def check_player_collision(self, player):
        if self.rect.colliderect(player.rect):
            if not player.invulnerable and player.action != "Death":
                if self.rect.centerx < player.rect.centerx:
                    player.knockback_dir = 1
                else:
                    player.knockback_dir = -1
                
                player.take_damage(self.damage_value)

    def handle_states(self, player_rect):
        if self.check_player_detection(player_rect):
            self.state = "Attack"
        elif self.state not in ["Hurt", "Attack"]:
            self.state = "Walk"

    @abstractmethod
    def move(self, dt, collision_rects):
        pass

    def animate(self, dt):
        self.animation_index += self.animation_speed * dt
        current_frames = self.animations[self.state]

        if self.animation_index >= len(current_frames):
            if self.state == "Dead":
                self.animation_index = len(current_frames) - 1
            else:
                self.animation_index = 0

        self.image = current_frames[int(self.animation_index)]
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def check_player_detection(self, player_rect):
        enemy_center = pygame.Vector2(self.hitbox.center)
        player_center = pygame.Vector2(player_rect.center)
        return enemy_center.distance_to(player_center) <= self.detection_radius

    def take_damage(self, amount):
        if self.state == "Dead":
            return

        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.state = "Dead"
            self.animation_index = 0
        else:
            self.state = "Hurt"
            self.state_timer = 0.3
            self.animation_index = 0


class GroundEnemy(Enemy):

    def __init__(self, x, y, width=32, height=48):
        super().__init__(
            x, y, width, height, health=100, damage=15, speed=80, detection_radius=120
        )
        self.image.fill((220, 60, 60))
        self.gravity = 500
        self.velocity_y = 0

    def move(self, dt, collision_rects):
        self.velocity_y += self.gravity * dt
        if self.velocity_y > 400:
            self.velocity_y = 400

        self.hitbox.x += self.direction * self.speed * dt
        self.rect.centerx = self.hitbox.centerx

        for tile in collision_rects:
            if self.hitbox.colliderect(tile):
                if self.direction > 0:
                    self.hitbox.right = tile.left
                elif self.direction < 0:
                    self.hitbox.left = tile.right
                self.direction *= -1
                self.rect.centerx = self.hitbox.centerx
                break

        self.hitbox.y += self.velocity_y * dt
        self.rect.centery = self.hitbox.centery

        for tile in collision_rects:
            if self.hitbox.colliderect(tile):
                if self.velocity_y > 0:
                    self.hitbox.bottom = tile.top
                    self.velocity_y = 0
                elif self.velocity_y < 0:
                    self.hitbox.top = tile.bottom
                    self.velocity_y = 0
                self.rect.centery = self.hitbox.centery


class FlyingEnemy(Enemy):

    def __init__(self, x, y, width=32, height=32):
        super().__init__(
            x, y, width, height, health=50, damage=10, speed=100, detection_radius=200
        )
        self.image.fill((60, 180, 220))
        self.start_y = y
        self.time_passed = random.uniform(0, 100)

    def move(self, dt, collision_rects):
        self.time_passed += dt
        self.hitbox.x += self.direction * self.speed * dt

        if random.random() < 0.01:
            self.direction *= -1

        self.hitbox.y = self.start_y + math.sin(self.time_passed * 3) * 25
        self.rect.center = self.hitbox.center


class WaterEnemy(Enemy):

    def __init__(self, x, y, animations, width=40, height=24):

        super().__init__(
            x, y, width, height,
            health=75,
            damage=12,
            speed=50,
            detection_radius=100
        )

        self.animations = animations

        self.image = self.animations["Idle"][0]

        self.rect = self.image.get_rect(topleft=(x, y))

        self.hitbox = self.rect.inflate(-width * 0.2, -height * 0.1)

        self.start_x = x
        self.time_passed = random.uniform(0, 100)

    def move(self, dt, collision_rects):
        self.time_passed += dt
        self.hitbox.x = self.start_x + math.sin(self.time_passed * 1.5) * 60

        next_x = self.start_x + math.sin((self.time_passed + dt) * 1.5) * 60
        self.direction = 1 if next_x > self.hitbox.x else -1

        self.hitbox.y += math.cos(self.time_passed * 4) * 10 * dt
        self.rect.center = self.hitbox.center