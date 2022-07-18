from screeninfo import get_monitors
from sys import exit
import pygame.transform

from player import *
from enemies import *
from explosions import *


class MovingBackground:
    """Create the moving stars in the background, simulating movement"""
    def __init__(self):
        self.bg_stars = SMALL_STARS
        self.rect_BG_img_stars = self.bg_stars.get_rect()
        self.bgY1s = 0
        self.bgX1s = 0
        self.bgY2s = self.rect_BG_img_stars.height
        self.bgX2s = 0
        self.movingUpSpeed_stars = 10 * DeltaTime

        self.bg_asteroids = BIG_STARS
        self.rect_BG_img_asteroids = self.bg_asteroids.get_rect()
        self.bgY1a = 0
        self.bgX1a = 0
        self.bgY2a = self.rect_BG_img_asteroids.height
        self.bgX2a = 0
        self.movingUpSpeed_asteroids = 30 * DeltaTime

    def update(self):
        self.bgY1s += self.movingUpSpeed_stars
        self.bgY2s += self.movingUpSpeed_stars
        self.bgY1a += self.movingUpSpeed_asteroids
        self.bgY2a += self.movingUpSpeed_asteroids
        if self.bgY1s >= self.rect_BG_img_stars.height:
            self.bgY1s = -self.rect_BG_img_stars.height
        if self.bgY2s >= self.rect_BG_img_stars.height:
            self.bgY2s = -self.rect_BG_img_stars.height
        if self.bgY1a >= self.rect_BG_img_asteroids.height:
            self.bgY1a = -self.rect_BG_img_asteroids.height
        if self.bgY2a >= self.rect_BG_img_asteroids.height:
            self.bgY2a = -self.rect_BG_img_asteroids.height

    def render(self):
        WINDOW.blit(self.bg_stars, (self.bgX1s, self.bgY1s))
        WINDOW.blit(self.bg_stars, (self.bgX2s, self.bgY2s))
        WINDOW.blit(self.bg_asteroids, (self.bgX1a, self.bgY1a))
        WINDOW.blit(self.bg_asteroids, (self.bgX2a, self.bgY2a))


class Game:
    """Main game class - everything runs from here"""
    def __init__(self):
        self.bg_animated = MovingBackground()
        self.font = pygame.font.Font("./ASSETS/crystal.ttf", 42)
        self.points = 0
        self.points_text = self.font.render(f"POINTS: {str(self.points)}", True, "green", None)

        # Player ship
        self.player_ship = PlayerShip(1920, 1280, PLAYER_SHIP)
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
        self.enemy_kill = {}
        self.enemy_spawn_time = pygame.time.get_ticks()
        self.crash = {}
        self.torpedo_hit = {}
        self.enemy_lasers_group = pygame.sprite.Group()
        self.player_kill = {}

        # Explosions
        self.explosion_group = pygame.sprite.Group()

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
                            self.lasers_group.add(self.player_ship.create_projectile("laser", PLAYER_LASER,
                                                                                     PLAYER_TORPEDO, DeltaTime))
                        if (event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL) and self.torpedoes > 0:
                            self.torpedoes_group.add(self.player_ship.create_projectile("torpedo", PLAYER_LASER,
                                                                                        PLAYER_TORPEDO, DeltaTime))
                            self.torpedoes -= 1
                            self.text_torpedoes = self.font.render(str(self.torpedoes), True, "green", None)
                    if event.key == pygame.K_BACKSPACE:
                        self.player_ship.player_lives = 3
                        self.text_player_lives = self.font.render(str(self.player_ship.player_lives), True, "green",
                                                                  None)

            # Draw and animate the background
            WINDOW.blit(BACKGROUND, (0, 0))
            self.bg_animated.update()
            self.bg_animated.render()
            WINDOW.blit(TORPEDO_ICON, (50, 1220))
            WINDOW.blit(self.text_torpedoes, (10, 1225))
            WINDOW.blit(PLAYER_ICON, (1820, 1210))
            WINDOW.blit(self.text_player_lives, (1880, 1215))
            WINDOW.blit(self.points_text, (900, 20))

            # Draw player projectiles
            self.lasers_group.draw(WINDOW)
            self.torpedoes_group.draw(WINDOW)
            self.torpedoes_group.update()
            self.lasers_group.update()

            # Draw player ship
            self.player_group.draw(WINDOW)
            self.player_ship.move(DeltaTime, WINDOW_LIMIT)

            # Draw enemy ships and projectiles
            for enemy in self.enemy_ships_group:
                if current_time - enemy.last_shot > random.randint(1000, 3500):
                    self.enemy_lasers_group.add(enemy.create_projectile(ENEMY_PROJECTILE, DeltaTime, 1280))
            self.enemy_ships_group.draw(WINDOW)  # Draw enemies
            self.enemy_lasers_group.draw(WINDOW)
            self.enemy_lasers_group.update()

            # Check if enemy is hit by laser
            self.enemy_kill = pygame.sprite.groupcollide(self.lasers_group, self.enemy_ships_group, True, True,
                                                         collided=pygame.sprite.collide_mask)
            if self.enemy_kill:
                for enemy in self.enemy_kill:
                    enemy_explosion = Explosion(enemy.rect.x, enemy.rect.y, EXPLOSION_ENEMY)
                    self.explosion_group.add(enemy_explosion)
                    self.points += 10

            # Check if enemy is hit by torpedo
            self.torpedo_hit = pygame.sprite.groupcollide(self.torpedoes_group, self.enemy_ships_group, True, True,
                                                          collided=pygame.sprite.collide_mask)
            if self.torpedo_hit:
                for enemy in self.enemy_ships_group:
                    enemy_explosion = Explosion(enemy.rect.x, enemy.rect.y, EXPLOSION_ENEMY)
                    self.explosion_group.add(enemy_explosion)
                    self.points += 10
                self.enemy_ships_group.empty()

            # Check if enemy collided with player ship or if enemy killed player
            self.crash = pygame.sprite.groupcollide(self.player_group, self.enemy_ships_group, True, True,
                                                    collided=pygame.sprite.collide_mask)
            self.player_kill = pygame.sprite.groupcollide(self.enemy_lasers_group, self.player_group, True, True,
                                                          collided=pygame.sprite.collide_mask)

            if self.crash or self.player_kill:
                if self.crash:
                    explosion_player = Explosion(self.player_ship.rect[0], self.player_ship.rect[1],
                                                 EXPLOSION_PLAYER_CRASH)
                    self.points += 10
                if self.player_kill:
                    explosion_player = Explosion(self.player_ship.rect[0], self.player_ship.rect[1],
                                                 EXPLOSION_PLAYER)
                self.explosion_group.add(explosion_player)
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
                    self.player_ship.rect = self.player_ship.image.get_rect(center=(960, 1280))

            # Check if enemies are less than 10 and add more
            if 10 > len(self.enemy_ships_group) >= 0 and current_time - self.enemy_spawn_time > 1000:
                self.enemy_ships_group.add(EnemyShip(1920, 640, ENEMY_SHIP))
                self.enemy_spawn_time = pygame.time.get_ticks()

            self.explosion_group.draw(WINDOW)
            self.explosion_group.update()

            self.points_text = self.font.render(f"POINTS: {str(self.points)}", True, "green", None)

            pygame.transform.scale(WINDOW, (WIDTH, HEIGHT), RESOLUTION)
            pygame.display.update()
            FramesPerSec.tick(FPS)


# Initializing
pygame.init()

# Game global parameters
WIDTH, HEIGHT = get_monitors()[0].width, get_monitors()[0].height
RESOLUTION = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
WINDOW = pygame.Surface((1920, 1280))
WINDOW_LIMIT = WINDOW.get_rect()
BACKGROUND = pygame.image.load("./ASSETS/background.png").convert()
SMALL_STARS = pygame.image.load("./ASSETS/stars_small.png").convert_alpha()
BIG_STARS = pygame.image.load("./ASSETS/stars_big.png").convert_alpha()

EXPLOSION_ENEMY = ExplosionList("./ASSETS/EXPLOSION_ENEMY/explosion_enemy*.png").image_list()
EXPLOSION_PLAYER_CRASH = ExplosionList("./ASSETS/EXPLOSION_PLAYER_CRASH/explosion_player_crash*.png").image_list()
EXPLOSION_PLAYER = ExplosionList("./ASSETS/EXPLOSION_PLAYER/explosion_player*.png").image_list()

PLAYER_SHIP = pygame.image.load("./ASSETS/player.png").convert_alpha()
PLAYER_ICON = pygame.image.load("./ASSETS/player_icon.png").convert_alpha()
PLAYER_LASER = pygame.image.load("./ASSETS/laser.png").convert_alpha()
PLAYER_TORPEDO = pygame.image.load("./ASSETS/torpedo.png").convert_alpha()
ENEMY_SHIP = pygame.image.load("./ASSETS/enemy_1.png").convert_alpha()
ENEMY_PROJECTILE = pygame.image.load("./ASSETS/laser_enemy.png").convert_alpha()
TORPEDO_ICON = pygame.image.load("./ASSETS/torpedo_icon.png").convert_alpha()
TORPEDO_COUNT = 3

pygame.display.set_caption("Space game!")
pygame.mouse.set_visible(False)
FPS = 60
FramesPerSec = pygame.time.Clock()
DeltaTime = FramesPerSec.tick(FPS) / 1000
game = Game()

if __name__ == "__main__":
    game.run()
