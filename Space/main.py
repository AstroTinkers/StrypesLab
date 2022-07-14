import pygame
import random
from sys import exit


class MovingBackground:
    """Create the moving stars in the background, simulating movement"""
    def __init__(self):
        self.bg_small_stars = pygame.image.load("./ASSETS/stars_small.png")
        self.rect_BG_img_small_stars = self.bg_small_stars.get_rect()
        self.bgY1s = 0
        self.bgX1s = 0
        self.bgY2s = self.rect_BG_img_small_stars.height
        self.bgX2s = 0
        self.movingUpSpeed_small_stars = 30 * DeltaTime

        self.bg_big_stars = pygame.image.load("./ASSETS/stars_big.png")
        self.rect_BG_img_big_stars = self.bg_big_stars.get_rect()
        self.bgY1b = 0
        self.bgX1b = 0
        self.bgY2b = self.rect_BG_img_big_stars.height
        self.bgX2b = 0
        self.movingUpSpeed_big_stars = 120 * DeltaTime

    def update(self):
        self.bgY1s += self.movingUpSpeed_small_stars
        self.bgY2s += self.movingUpSpeed_small_stars
        self.bgY1b += self.movingUpSpeed_big_stars
        self.bgY2b += self.movingUpSpeed_big_stars
        if self.bgY1s >= self.rect_BG_img_small_stars.height:
            self.bgY1s = -self.rect_BG_img_small_stars.height
        if self.bgY2s >= self.rect_BG_img_small_stars.height:
            self.bgY2s = -self.rect_BG_img_small_stars.height
        if self.bgY1b >= self.rect_BG_img_big_stars.height:
            self.bgY1b = -self.rect_BG_img_big_stars.height
        if self.bgY2b >= self.rect_BG_img_big_stars.height:
            self.bgY2b = -self.rect_BG_img_big_stars.height

    def render(self):
        WINDOW.blit(self.bg_small_stars, (self.bgX1s, self.bgY1s))
        WINDOW.blit(self.bg_small_stars, (self.bgX2s, self.bgY2s))
        WINDOW.blit(self.bg_big_stars, (self.bgX1b, self.bgY1b))
        WINDOW.blit(self.bg_big_stars, (self.bgX2b, self.bgY2b))


class Player(pygame.sprite.Sprite):
    """Main player class, responsible for the player's ship, movement and firing controls"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./ASSETS/player.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(480, 540))
        self.last_shot = pygame.time.get_ticks()
        self.speed = 750

    def move(self, datetime):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_w]:
            self.rect.y += -self.speed * datetime
        if pressed_key[pygame.K_s]:
            self.rect.y += self.speed * datetime
        if pressed_key[pygame.K_a]:
            self.rect.x += -self.speed * datetime
        if pressed_key[pygame.K_d]:
            self.rect.x += self.speed * datetime
        self.rect.clamp_ip(WINDOW_LIMIT)

    def create_projectile(self, w_type):
        self.last_shot = pygame.time.get_ticks()
        return Projectiles(self.rect[0], self.rect[1], w_type)


class Enemy(pygame.sprite.Sprite):  # FIX THIS
    """Enemy class, responsible for creating the enemies the player has to fight"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./ASSETS/player.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(random.randint(0, 1000), random.randint(0, 200)))
        # self.last_shot = pygame.time.get_ticks()


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
        self.speed = 1000

    def update(self):
        self.rect.y -= self.speed * DeltaTime

        if self.rect.y < 0:
            self.kill()


class Game:
    """Main game class - everything runs from here"""
    def __init__(self):
        self.bg_animated = MovingBackground()
        self.font = pygame.font.Font("./ASSETS/crystal.ttf", 32)

        # Pilot
        self.pilot = Player()
        self.pilot_group = pygame.sprite.Group()
        self.pilot_group.add(self.pilot)
        self.player_lives = 3
        self.text_player_lives = self.font.render(str(self.player_lives), True, "green", None)

        # Projectiles
        self.lasers_group = pygame.sprite.Group()
        self.torpedoes_group = pygame.sprite.Group()
        self.torpedoes = 3
        self.text_torpedoes = self.font.render(str(self.torpedoes), True, "green", None)

        # Enemies
        self.enemies_group = pygame.sprite.Group()
        self.enemy_kill = pygame.sprite.groupcollide(self.lasers_group, self.enemies_group, True, True)
        self.enemy_spawn_time = pygame.time.get_ticks()
        self.crash = pygame.sprite.groupcollide(self.pilot_group, self.enemies_group, True, True)
        self.torpedo_hit = pygame.sprite.groupcollide(self.torpedoes_group, self.enemies_group, True, True)


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Firing projectiles
                if event.type == pygame.KEYDOWN:
                    if self.pilot_group:
                        current_time = pygame.time.get_ticks()
                        if event.key == pygame.K_SPACE and current_time - self.pilot.last_shot > 150:
                            self.lasers_group.add(self.pilot.create_projectile("laser"))
                        if event.key == pygame.K_RCTRL and self.torpedoes > 0:
                            self.torpedoes_group.add(self.pilot.create_projectile(""))
                            self.torpedoes -= 1
                            self.text_torpedoes = self.font.render(str(self.torpedoes), True, "green", None)

            # Draw and animate the background
            WINDOW.blit(BACKGROUND, (0, 0))
            WINDOW.blit(TORPEDO_ICON, (40, 503))
            WINDOW.blit(self.text_torpedoes, (10, 500))
            WINDOW.blit(self.text_player_lives, (900, 500))
            self.bg_animated.update()
            self.bg_animated.render()

            # Draw projectiles
            self.lasers_group.draw(WINDOW)
            self.torpedoes_group.draw(WINDOW)
            self.torpedoes_group.update()
            self.lasers_group.update()

            # Draw ship
            self.pilot_group.draw(WINDOW)
            self.pilot.move(DeltaTime)

            self.enemies_group.draw(WINDOW)  # Draw enemies

            # Check if enemy is hit by laser
            self.enemy_kill = pygame.sprite.groupcollide(self.lasers_group, self.enemies_group, True, True)

            # Check if enemy is hit by torpedo
            self.torpedo_hit = pygame.sprite.groupcollide(self.torpedoes_group, self.enemies_group, True, True)
            if self.torpedo_hit:
                self.enemies_group.empty()

            # Check if enemy collided with player
            self.crash = pygame.sprite.groupcollide(self.pilot_group, self.enemies_group, True, True)
            if self.crash:
                self.player_lives -= 1
                self.text_player_lives = self.font.render(str(self.player_lives), True, "green", None)
                self.pilot.kill()
                if self.player_lives > 0:
                    self.pilot = Player()
                    self.pilot_group.add(self.pilot)

            # Check if enemies are less than 10 and add more
            kill_time = pygame.time.get_ticks()
            if 10 > len(self.enemies_group) >= 0 and kill_time - self.enemy_spawn_time > 1000:
                self.enemies_group.add(Enemy())
                self.enemy_spawn_time = pygame.time.get_ticks()

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
DeltaTime = FramesPerSec.tick(FPS) / 1000
game = Game()

if __name__ == "__main__":
    game.run()
