import glob

import pygame


class ExplosionList:
    def __init__(self, file_path):
        super().__init__()
        self.image_glob = glob.glob(file_path)
        self.images = []

    def image_list(self):
        for img in self.image_glob:
            self.images.append(pygame.image.load(img).convert_alpha())
        return self.images


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, image_list):
        super().__init__()
        self.images = image_list
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.counter = 0

    def update(self):
        explosion_speed = 4
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()
