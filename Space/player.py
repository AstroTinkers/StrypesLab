import pygame

pygame.init()


class PlayerShip(pygame.sprite.Sprite):
    """Main player class, responsible for the player's ship, movement and firing controls"""
    def __init__(self, width, height, image_list):
        super().__init__()
        self.images = image_list
        self.index = 0
        self.image = self.images[self.index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(width/2, height - 50))
        self.player_lives = 3
        self.last_shot = pygame.time.get_ticks()
        self.speed = 500
        self.counter = 0

    def update(self):
        engine_animation_speed = 4
        self.counter += 1

        if self.counter >= engine_animation_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= engine_animation_speed:
            self.index = 0

    def move(self, delta_time, window_limit):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_w] or pressed_key[pygame.K_UP]:
            self.rect.y += -self.speed * delta_time
        if pressed_key[pygame.K_s] or pressed_key[pygame.K_DOWN]:
            self.rect.y += self.speed * delta_time
        if pressed_key[pygame.K_a] or pressed_key[pygame.K_LEFT]:
            self.rect.x += -self.speed * delta_time
        if pressed_key[pygame.K_d] or pressed_key[pygame.K_RIGHT]:
            self.rect.x += self.speed * delta_time
        self.rect.clamp_ip(window_limit)

    def create_projectile(self, w_type, image_laser, image_torpedo, delta_time):
        self.last_shot = pygame.time.get_ticks()
        return PlayerProjectile(self.rect[0], self.rect[1], w_type, image_laser, image_torpedo, delta_time)


class PlayerProjectile(pygame.sprite.Sprite):
    """A class to handle lasers and torpedoes"""

    fire_left = True

    def __init__(self, x, y, w_type, image_laser, image_torpedo, delta_time):
        super().__init__()
        self.type = w_type
        if self.type == "laser":
            self.image = image_laser

            # Alternate fire between left and right laser on the ship
            if PlayerProjectile.fire_left:
                self.rect = self.image.get_rect(center=(x + 9, y))
                PlayerProjectile.fire_left = False
            else:
                self.rect = self.image.get_rect(center=(x + 129, y))
                PlayerProjectile.fire_left = True
        else:
            self.image = image_torpedo
            self.rect = self.image.get_rect(center=(x + 70, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 1500
        self.delta_time = delta_time

    def update(self):
        self.rect.y -= self.speed * self.delta_time

        if self.rect.y < 0:
            self.kill()


FPS = 60
FramesPerSec = pygame.time.Clock()
DeltaTime = FramesPerSec.tick(FPS) / 1000
