import pygame
from sys import exit


class MovingBackground:
    """Create the moving stars in the background, simulating movement"""
    def __init__(self):
        self.bg_image = pygame.image.load("./ASSETS/stars.png")
        self.rect_BG_img = self.bg_image.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = self.rect_BG_img.height
        self.bgX2 = 0

        self.movingUpSpeed = 1

    def update(self):
        self.bgY1 += self.movingUpSpeed
        self.bgY2 += self.movingUpSpeed
        if self.bgY1 >= self.rect_BG_img.height:
            self.bgY1 = -self.rect_BG_img.height
        if self.bgY2 >= self.rect_BG_img.height:
            self.bgY2 = -self.rect_BG_img.height

    def render(self):
        WINDOW.blit(self.bg_image, (self.bgX1, self.bgY1))
        WINDOW.blit(self.bg_image, (self.bgX2, self.bgY2))


class Player(pygame.sprite.Sprite):
    """Main player class, responsible for the player's ship, movement and firing controls"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./ASSETS/player.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(480, 540))
        self.last_shot = pygame.time.get_ticks()

    def move(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_w]:
            self.rect.move_ip(0, -15)
        if pressed_key[pygame.K_s]:
            self.rect.move_ip(0, 15)
        if pressed_key[pygame.K_a]:
            self.rect.move_ip(-15, 0)
        if pressed_key[pygame.K_d]:
            self.rect.move_ip(15, 0)
        self.rect.clamp_ip(WINDOW_LIMIT)

    def create_projectile_laser(self, w_type):
        self.last_shot = pygame.time.get_ticks()
        return Projectiles(self.rect[0], self.rect[1], w_type)


class Projectiles(pygame.sprite.Sprite):
    """A class to handle lasers and torpedoes"""

    fire_left = True

    def __init__(self, x, y, w_type):
        super().__init__()
        self.type = w_type
        if self.type == "laser":
            self.image = pygame.image.load("./ASSETS/laser.png")
            if Projectiles.fire_left:  # Alternate fire between left and right laser on the ship
                self.rect = self.image.get_rect(center=(x + 22, y))
                Projectiles.fire_left = False
            else:
                self.rect = self.image.get_rect(center=(x + 28, y))
                Projectiles.fire_left = True
        else:
            self.image = pygame.image.load("./ASSETS/torpedo.png")
            self.rect = self.image.get_rect(center=(x + 25, y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y -= 10

        if self.rect.y < 0:
            self.kill()


class Game:
    """Main game class - everything runs from here"""
    def __init__(self):
        self.bg_animated = MovingBackground()
        self.pilot = Player()
        self.pilot_group = pygame.sprite.Group()
        self.pilot_group.add(self.pilot)
        self.enemies_group = pygame.sprite.Group()
        self.projectiles_group = pygame.sprite.Group()
        self.torpedoes = 3
        self.font = pygame.font.Font("./ASSETS/crystal.ttf", 32)
        self.text = self.font.render(str(self.torpedoes), True, "green", None)

    def shoot(self, projectile_group):
        # add sound
        pygame.sprite.spritecollide([projectile for projectile in projectile_group], self.enemies_group, True)  # FIX THIS

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:  # Firing projectiles
                    current_time = pygame.time.get_ticks()
                    if event.key == pygame.K_SPACE and current_time - self.pilot.last_shot > 150:
                        self.projectiles_group.add(self.pilot.create_projectile_laser("laser"))
                    if event.key == pygame.K_RCTRL and self.torpedoes > 0:
                        self.projectiles_group.add(self.pilot.create_projectile_laser(""))
                        self.torpedoes -= 1
                        self.text = self.font.render(str(self.torpedoes), True, "green", None)

            WINDOW.blit(BACKGROUND, (0, 0))
            WINDOW.blit(TORPEDO_ICON, (40, 503))
            WINDOW.blit(self.text, (10, 500))
            self.bg_animated.update()
            self.bg_animated.render()

            self.projectiles_group.draw(WINDOW)
            self.projectiles_group.update()

            self.pilot_group.draw(WINDOW)
            self.pilot.move()

            pygame.display.update()
            FramesPerSec.tick(FPS)


# Initializing
pygame.init()

# Game global parameters
WIDTH, HEIGHT = 960, 540
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
WINDOW_LIMIT = WINDOW.get_rect()
BACKGROUND = pygame.image.load("./ASSETS/background.png")

TORPEDO_ICON = pygame.image.load("./ASSETS/torpedo_icon.png")
TORPEDO_COUNT = 3

pygame.display.set_caption("Space game!")
pygame.mouse.set_visible(False)
FPS = 60
FramesPerSec = pygame.time.Clock()

game = Game()

if __name__ == "__main__":
    game.run()
