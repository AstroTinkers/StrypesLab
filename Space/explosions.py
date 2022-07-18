import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, filepath, frames, width, height):
        super().__init__()
        self.images = []
        for num in range(1, frames):
            try:
                img = pygame.image.load(f"{filepath}{num}.png").convert_alpha()
                img = pygame.transform.scale(img, (width, height))
                self.images.append(img)
            except:
                break
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.counter = 0

    def explosion_occurs_at(self, x, y):
        self.rect.center = [x, y]

    def update(self):
        explosion_speed = 20
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # reset animation index

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()