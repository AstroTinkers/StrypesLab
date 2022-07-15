import pygame
import random
from screeninfo import get_monitors
from sys import exit


class MovingBackground:
    """Create the moving stars in the background, simulating movement"""
    def __init__(self):
        self.bg_small_stars = pygame.image.load("./ASSETS/stars.png").convert_alpha()
        self.rect_BG_img_small_stars = self.bg_small_stars.get_rect()
        self.bgY1s = 0
        self.bgX1s = 0
        self.bgY2s = self.rect_BG_img_small_stars.height
        self.bgX2s = 0
        self.movingUpSpeed_small_stars = 10 * DeltaTime

        self.bg_big_stars = pygame.image.load("./ASSETS/asteroids.png").convert_alpha()
        self.rect_BG_img_big_stars = self.bg_big_stars.get_rect()
        self.bgY1b = 0
        self.bgX1b = 0
        self.bgY2b = self.rect_BG_img_big_stars.height
        self.bgX2b = 0
        self.movingUpSpeed_big_stars = 160 * DeltaTime

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


class PlayerShip(pygame.sprite.Sprite):
    """Main player class, responsible for the player's ship, movement and firing controls"""
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.image.load("./ASSETS/player.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(width/2, height - 50))
        self.player_lives = 3
        self.last_shot = pygame.time.get_ticks()
        self.speed = 500

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
        return PlayerProjectile(self.rect[0], self.rect[1], w_type)


class EnemyShip(pygame.sprite.Sprite):  # FIX THIS
    """Enemy class, responsible for creating the enemies the player has to fight"""
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.image.load("./ASSETS/enemy_1.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(random.randint(0, width), random.randint(0, height)))
        self.last_shot = pygame.time.get_ticks()

    def create_projectile(self):
        self.last_shot = pygame.time.get_ticks()
        return EnemyProjectile(self.rect[0], self.rect[1])


class EnemyProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("./ASSETS/laser_enemy.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x + 59, y + 160))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 1000

    def update(self):
        self.rect.y += self.speed * DeltaTime

        if self.rect.y > HEIGHT:
            self.kill()


class PlayerProjectile(pygame.sprite.Sprite):
    """A class to handle lasers and torpedoes"""

    fire_left = True

    def __init__(self, x, y, w_type):
        super().__init__()
        self.type = w_type
        if self.type == "laser":
            self.image = pygame.image.load("./ASSETS/laser.png").convert_alpha()
            if PlayerProjectile.fire_left:  # Alternate fire between left and right laser on the ship
                self.rect = self.image.get_rect(center=(x + 9, y))
                PlayerProjectile.fire_left = False
            else:
                self.rect = self.image.get_rect(center=(x + 129, y))
                PlayerProjectile.fire_left = True
        else:
            self.image = pygame.image.load("./ASSETS/torpedo.png").convert_alpha()
            self.rect = self.image.get_rect(center=(x + 70, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 1500

    def update(self):
        self.rect.y -= self.speed * DeltaTime

        if self.rect.y < 0:
            self.kill()


class Game:
    """Main game class - everything runs from here"""
    def __init__(self):
        self.bg_animated = MovingBackground()
        self.font = pygame.font.Font("./ASSETS/crystal.ttf", 32)

        # Player ship
        self.player_ship = PlayerShip(WIDTH, HEIGHT)
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player_ship)
        self.text_player_lives = self.font.render(str(self.player_ship.player_lives), True, "green", None)
        self.death_time = pygame.time.get_ticks()

        # Player Projectiles
        self.lasers_group = pygame.sprite.Group()
        self.torpedoes_group = pygame.sprite.Group()
        self.torpedoes = 3
        self.text_torpedoes = self.font.render(str(self.torpedoes), True, "green", None)

        # Enemy ships and projectiles
        self.enemy_ships_group = pygame.sprite.Group()
        self.enemy_kill = pygame.sprite.groupcollide(self.lasers_group, self.enemy_ships_group, True, True,
                                                     collided=pygame.sprite.collide_mask)
        self.enemy_spawn_time = pygame.time.get_ticks()
        self.crash = pygame.sprite.groupcollide(self.player_group, self.enemy_ships_group, True, True,
                                                collided=pygame.sprite.collide_mask)
        self.torpedo_hit = pygame.sprite.groupcollide(self.torpedoes_group, self.enemy_ships_group, True, True,
                                                      collided=pygame.sprite.collide_mask)
        self.enemy_lasers_group = pygame.sprite.Group()
        self.player_kill = pygame.sprite.groupcollide(self.enemy_lasers_group, self.player_group, True, True,
                                                      collided=pygame.sprite.collide_mask)

    def run(self):
        while True:
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Firing projectiles
                if event.type == pygame.KEYDOWN:
                    if self.player_group:
                        if event.key == pygame.K_SPACE and current_time - self.player_ship.last_shot > 150:
                            self.lasers_group.add(self.player_ship.create_projectile("laser"))
                        if event.key == pygame.K_RCTRL and self.torpedoes > 0:
                            self.torpedoes_group.add(self.player_ship.create_projectile("torpedo"))
                            self.torpedoes -= 1
                            self.text_torpedoes = self.font.render(str(self.torpedoes), True, "green", None)

            # Draw and animate the background
            WINDOW.blit(BACKGROUND, (0, 0))
            self.bg_animated.update()
            self.bg_animated.render()
            WINDOW.blit(TORPEDO_ICON, (WIDTH - (WIDTH - 40), HEIGHT - 40))
            WINDOW.blit(self.text_torpedoes, (WIDTH - (WIDTH - 10), HEIGHT - 40))
            WINDOW.blit(self.text_player_lives, (WIDTH - 40, HEIGHT - 40))

            # Draw player projectiles
            self.lasers_group.draw(WINDOW)
            self.torpedoes_group.draw(WINDOW)
            self.torpedoes_group.update()
            self.lasers_group.update()

            # Draw player ship
            self.player_group.draw(WINDOW)
            self.player_ship.move(DeltaTime)

            # Draw enemy ships and projectiles
            for enemy in self.enemy_ships_group:
                if current_time - enemy.last_shot > random.randint(1000, 3500):
                    self.enemy_lasers_group.add(enemy.create_projectile())
            self.enemy_ships_group.draw(WINDOW)  # Draw enemies
            self.enemy_lasers_group.draw(WINDOW)
            self.enemy_lasers_group.update()

            # Check if enemy is hit by laser
            self.enemy_kill = pygame.sprite.groupcollide(self.lasers_group, self.enemy_ships_group, True, True,
                                                         collided=pygame.sprite.collide_mask)

            # Check if enemy is hit by torpedo
            self.torpedo_hit = pygame.sprite.groupcollide(self.torpedoes_group, self.enemy_ships_group, True, True,
                                                          collided=pygame.sprite.collide_mask)
            if self.torpedo_hit:
                self.enemy_ships_group.empty()

            # Check if enemy collided with player ship or if enemy killed player
            self.crash = pygame.sprite.groupcollide(self.player_group, self.enemy_ships_group, True, True,
                                                    collided=pygame.sprite.collide_mask)
            self.player_kill = pygame.sprite.groupcollide(self.enemy_lasers_group, self.player_group, True, True,
                                                          collided=pygame.sprite.collide_mask)
            if self.crash or self.player_kill:
                self.player_ship.player_lives -= 1
                self.text_player_lives = self.font.render(str(self.player_ship.player_lives), True, "green", None)
                self.player_ship.kill()
                self.death_time = pygame.time.get_ticks()

            # Check if player group is empty and add draw new player ship sprite if player has lives left
            if len(self.player_group) == 0:
                if self.player_ship.player_lives > 0 and current_time - self.death_time > 1000:
                    self.player_group.add(self.player_ship)
                    self.torpedoes = 3
                    self.text_torpedoes = self.font.render(str(self.torpedoes), True, "green", None)
                    self.player_ship.rect = self.player_ship.image.get_rect(center=(WIDTH/2, HEIGHT))

            # Check if enemies are less than 10 and add more
            if 10 > len(self.enemy_ships_group) >= 0 and current_time - self.enemy_spawn_time > 1000:
                self.enemy_ships_group.add(EnemyShip(WIDTH, HEIGHT/2))
                self.enemy_spawn_time = pygame.time.get_ticks()

            pygame.display.update()
            FramesPerSec.tick(FPS)


# Initializing
pygame.init()

# Game global parameters
WIDTH, HEIGHT = get_monitors()[0].width, get_monitors()[0].height
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
WINDOW_LIMIT = WINDOW.get_rect()
BACKGROUND = pygame.image.load("./ASSETS/background.png").convert()
EXPLOSION = pygame.image.load("./ASSETS/torpedo.png")
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
