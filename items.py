import pygame.sprite

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, animation_list):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self, player):

        if self.rect.colliderect(player.rect):
            
            if self.item_type == 0:
                player.score += 1

            elif self.item_type == 1:
                player.health += 50
                if player.health > 100:
                    player.health = 100

            elif self.item_type == 2:
                player.health += 50
                if player.health > 100:
                    player.health = 100

            self.kill()
                


        cooldown_animation = 100
        self.image = self.animation_list[self.frame_index]

        if pygame.time.get_ticks() - self.update_time > cooldown_animation:
            self.frame_index+= 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index > len(self.animation_list)-1:
            self.frame_index = 0