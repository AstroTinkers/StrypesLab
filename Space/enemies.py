import pygame
import random

pygame.init()


class EnemyShip(pygame.sprite.Sprite):  # FIX THIS
    """Enemy class, responsible for creating the enemies the player has to fight"""
    def __init__(self, width, height, image):
        super().__init__()
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(random.randint(0, width), random.randint(0, height)))
        self.last_shot = pygame.time.get_ticks()

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
