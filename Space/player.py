import pygame

pygame.init()


class PlayerShip(pygame.sprite.Sprite):
    """Main player class, responsible for the player's ship, movement and firing controls"""
    def __init__(self, width, height, image):
        super().__init__()
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(width/2, height - 50))
        self.player_lives = 3
        self.last_shot = pygame.time.get_ticks()
        self.speed = 500

    def move(self, delta_time, window_limit):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_w]:
            self.rect.y += -self.speed * delta_time
        if pressed_key[pygame.K_s]:
            self.rect.y += self.speed * delta_time
        if pressed_key[pygame.K_a]:
            self.rect.x += -self.speed * delta_time
        if pressed_key[pygame.K_d]:
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
            if PlayerProjectile.fire_left:  # Alternate fire between left and right laser on the ship
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
