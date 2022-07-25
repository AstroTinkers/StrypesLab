import pygame
import random

pygame.init()


class EnemyShip(pygame.sprite.Sprite):
    """Enemy class, responsible for creating the enemies the player has to fight"""
    def __init__(self, width, image_list):
        super().__init__()
        self.width = width
        self.images = image_list
        self.index = 0
        self.image = self.images[self.index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(random.randint(0, self.width), -100))
        self.last_shot = pygame.time.get_ticks()
        self.speed = 200
        self.counter = 0
        self.last_move = 0

    def update(self):
        engine_animation_speed = 2
        self.counter += 1

        if self.counter >= engine_animation_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= engine_animation_speed:
            self.index = 0

    def move(self, delta_time, height):
        if self.last_move <= 100:
            self.rect.y += self.speed * delta_time
            self.rect.x += -self.speed * delta_time
            self.last_move += 1
        else:
            self.rect.y += self.speed * delta_time
            self.rect.x += self.speed * delta_time
            self.last_move += 1
        if self.last_move >= 200:
            self.last_move = 0
        if self.rect.y > height + 200:
            self.rect = self.image.get_rect(center=(random.randint(0, self.width), -100))

    def create_projectile(self, image_laser, delta_time, height):
        self.last_shot = pygame.time.get_ticks()
        return EnemyProjectile(self.rect[0], self.rect[1], image_laser, delta_time, height)


class EnemyProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, image_laser, delta_time, height):
        super().__init__()
        self.image = image_laser
        self.rect = self.image.get_rect(center=(x + 59, y + 160))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 1000
        self.delta_time = delta_time
        self.height = height

    def update(self):
        self.rect.y += self.speed * self.delta_time

        if self.rect.y > self.height:
            self.kill()


class EnemyShipAdvanced(EnemyShip):
    """Enemy class, responsible for creating advanced enemies the player has to fight"""
    def __init__(self, width, image_list):
        super().__init__(width, image_list)
        self.width = width
        self.images = image_list
        self.index = 0
        self.image = self.images[self.index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(random.randint(0, self.width - 200), -100))
        self.last_shot = pygame.time.get_ticks()
        self.speed = 200
        self.target = 0

    def move(self, delta_time, height):
        if self.rect.y < height / 8:
            self.rect.y += self.speed * delta_time
        if self.rect.x < self.target:
            self.rect.x = self.rect.x + self.speed * delta_time
            self.target = self.width - 230
        else:
            self.rect.x = self.rect.x - self.speed * delta_time
            self.target = 0

    def create_projectile(self, image_laser, delta_time, height):
        self.last_shot = pygame.time.get_ticks()
        return EnemyAdvancedProjectile(self.rect[0], self.rect[1], image_laser, delta_time, height)


class EnemyAdvancedProjectile(EnemyProjectile):
    def __init__(self, x, y, image_laser, delta_time, height):
        super().__init__(x, y, image_laser, delta_time, height)
        self.image = image_laser
        self.rect = self.image.get_rect(center=(x + 120, y + 381))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 1000
        self.delta_time = delta_time
        self.height = height


class EnemyBoss(EnemyShip):
    def __init__(self, width, image_list):
        super().__init__(width, image_list)
        self.width = width
        self.images = image_list
        self.index = 0
        self.image = self.images[self.index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(random.randint(0, self.width - 300), -200))
        self.last_shot = pygame.time.get_ticks()
        self.speed = 150
        self.move_counter = 0
        self.target = 0
        self.life = 100

    def move(self, delta_time, height):
        if self.rect.y < height - (height - 50):
            self.rect.y += self.speed * delta_time
        if self.rect.x < self.target:
            self.rect.x = self.rect.x + self.speed * delta_time
            self.target = self.width - 372
            self.move_counter += 1
        else:
            self.rect.x = self.rect.x - self.speed * delta_time
            self.target = 0
            self.move_counter += 1
        if 620 > self.move_counter >= 500:
            self.rect.y += (self.speed*4) * delta_time
            self.move_counter += 1
        if 1100 > self.move_counter >= 620:
            self.rect.y -= self.speed * delta_time
            self.move_counter += 1
        if self.move_counter == 1100:
            self.move_counter = 0

    def create_projectiles(self, image_laser, delta_time, height, laser_type):
        self.last_shot = pygame.time.get_ticks()
        return EnemyBossProjectile(self.rect[0], self.rect[1], image_laser, delta_time, height, laser_type)


class EnemyBossProjectile(EnemyProjectile):
    def __init__(self, x, y, image_laser, delta_time, height, laser_type):
        super().__init__(x, y, image_laser, delta_time, height)
        self.image = image_laser
        if laser_type == "narrow":
            self.rect = self.image.get_rect(center=(x + 187, y + 473))
        else:
            self.rect = self.image.get_rect(center=(x + 187, y + 300))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 1000
        self.delta_time = delta_time
        self.height = height
