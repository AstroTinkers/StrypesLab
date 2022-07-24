import glob
import os
import pygame


def load_sprite_animations():
    sprites = {}
    for dirpath, dirnames, filenames in os.walk("./ASSETS/SPRITE_ANIMATIONS"):
        for name in dirnames:
            key = name
            path = str(os.path.join(dirpath, name))
            sprites[key] = [pygame.image.load(img).convert_alpha() for img in glob.glob(f"{path}/*.png")]
    return sprites


class MovingBackground:
    """Create the moving stars in the background, simulating movement"""
    def __init__(self, game_window, img_back, img_front, speed_back_img, speed_front_img, delta_time):
        self.game_window = game_window
        self.img_back = img_back
        self.delta_time = delta_time
        self.rect_img_back = self.img_back.get_rect()
        self.img_back_XY1 = (0, 0)
        # self.img_back_X1 = 0
        self.img_back_XY2 = (0, self.rect_img_back.height)
        # self.img_back_X2 = 0
        self.mov_speed_img_back = speed_back_img * self.delta_time

        self.img_front = img_front
        self.rect_img_front = self.img_front.get_rect()
        self.img_front_XY1 = (0, 0)
        # self.img_front_X1 = 0
        self.img_front_XY2 = (0, self.rect_img_front.height)
        # self.img_front_X2 = 0
        self.mov_speed_img_front = speed_front_img * self.delta_time

    def update(self):
        self.img_back_XY1 = (0, self.img_back_XY1[1] + self.mov_speed_img_back)
        self.img_back_XY2 = (0, self.img_back_XY2[1] + self.mov_speed_img_back)
        self.img_front_XY1 = (0, self.img_back_XY1[1] + self.mov_speed_img_front)
        self.img_front_XY2 = (0, self.img_back_XY2[1] + self.mov_speed_img_front)
        if self.img_back_XY1[1] >= self.rect_img_back.height:
            self.img_back_XY1 = (0, -self.rect_img_back.height)
        if self.img_back_XY2[1] >= self.rect_img_back.height:
            self.img_back_XY2 = (0, -self.rect_img_back.height)
        if self.img_front_XY1[1] >= self.rect_img_front.height:
            self.img_front_XY1 = (0, -self.rect_img_front.height)
        if self.img_front_XY2[1] >= self.rect_img_front.height:
            self.img_front_XY2 = (0, -self.rect_img_front.height)

    def render(self):
        self.game_window.blit(self.img_back, self.img_back_XY1)
        self.game_window.blit(self.img_back, self.img_back_XY2)
        self.game_window.blit(self.img_front, self.img_front_XY1)
        self.game_window.blit(self.img_front, self.img_front_XY2)


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
