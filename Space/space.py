from screeninfo import get_monitors
from sys import exit
import pygame.transform
import os

from player import *
from enemies import *
from animations import *


def exit_game():
    pygame.quit()
    exit()


def load_sounds(sounds):
    for dirpath, dirnames, filenames in os.walk("./ASSETS/SOUNDS"):
        for name in filenames:
            key = name[:-4]
            sounds[key] = os.path.join(dirpath, name)


class MovingBackground:
    """Create the moving stars in the background, simulating movement"""
    def __init__(self):
        self.bg_stars = SMALL_STARS
        self.rect_BG_img_stars = self.bg_stars.get_rect()
        self.bgY1s = 0
        self.bgX1s = 0
        self.bgY2s = self.rect_BG_img_stars.height
        self.bgX2s = 0
        self.movingSpeed_stars = 10 * DeltaTime

        self.bg_small_stars = BIG_STARS
        self.rect_BG_img_small_stars = self.bg_small_stars.get_rect()
        self.bgY1a = 0
        self.bgX1a = 0
        self.bgY2a = self.rect_BG_img_small_stars.height
        self.bgX2a = 0
        self.movingSpeed_small_stars = 30 * DeltaTime

    def update(self):
        self.bgY1s += self.movingSpeed_stars
        self.bgY2s += self.movingSpeed_stars
        self.bgY1a += self.movingSpeed_small_stars
        self.bgY2a += self.movingSpeed_small_stars
        if self.bgY1s >= self.rect_BG_img_stars.height:
            self.bgY1s = -self.rect_BG_img_stars.height
        if self.bgY2s >= self.rect_BG_img_stars.height:
            self.bgY2s = -self.rect_BG_img_stars.height
        if self.bgY1a >= self.rect_BG_img_small_stars.height:
            self.bgY1a = -self.rect_BG_img_small_stars.height
        if self.bgY2a >= self.rect_BG_img_small_stars.height:
            self.bgY2a = -self.rect_BG_img_small_stars.height

    def render(self):
        WINDOW.blit(self.bg_stars, (self.bgX1s, self.bgY1s))
        WINDOW.blit(self.bg_stars, (self.bgX2s, self.bgY2s))
        WINDOW.blit(self.bg_small_stars, (self.bgX1a, self.bgY1a))
        WINDOW.blit(self.bg_small_stars, (self.bgX2a, self.bgY2a))


class Game:
    """Main game class - everything runs from here"""
    def __init__(self):
        self.bg_animated = MovingBackground()
        self.font = pygame.font.Font("./ASSETS/crystal.ttf", 42)
        self.score = 0
        self.score_text = self.font.render(f"SCORE: {self.score:010d}", True, "green", None)
        self.kill_count = 0
        self.life_threshold = 2
        self.torpedo_threshold = 1

        # Player ship
        self.player_ship = PlayerShip(1920, 1080, PLAYER_SHIP_SPRITES)
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
        self.max_enemies = 6
        self.enemy_ships_group = pygame.sprite.Group()
        self.enemy_ships_advanced_group = pygame.sprite.Group()
        self.enemy_kill = {}
        self.enemy_advanced_kill = {}
        self.enemy_spawn_time = pygame.time.get_ticks()
        self.crash = {}
        self.crash_advanced = {}
        self.torpedo_hit_enemy = {}
        self.torpedo_hit_advanced_enemy = {}
        self.enemy_lasers_group = pygame.sprite.Group()
        self.enemy_advanced_lasers_group = pygame.sprite.Group()
        self.player_kill = {}

        # Explosions
        self.explosion_group = pygame.sprite.Group()

        # Pause
        self.pause = False

    def enemy_destroyed(self, enemy_group, play):
        for enemy in enemy_group:
            enemy_explosion = Explosion(enemy.rect.x, enemy.rect.y, EXPLOSION_ENEMY_SPRITES)
            self.explosion_group.add(enemy_explosion)
            self.score += 10
            self.kill_count += 1
            if play:
                pygame.mixer.Sound.play(ENEMY_EXPLOSION_SOUND)

    def advanced_enemy_destroyed(self, enemy_group, play):
        for enemy in enemy_group:
            enemy_explosion = Explosion(enemy.rect.x, enemy.rect.y, EXPLOSION_ENEMY_SPRITES)
            self.explosion_group.add(enemy_explosion)
            self.score += 50
            if play:
                pygame.mixer.Sound.play(ENEMY_ADVANCED_EXPLOSION_SOUND)

    def menu_animations(self):
        WINDOW.blit(BACKGROUND, (0, 0))
        self.bg_animated.update()
        self.bg_animated.render()
        self.player_group.draw(WINDOW)
        self.player_group.update()

    def new_game(self):
        while True:
            if not self.pause:
                current_time = pygame.time.get_ticks()

                # Draw and animate the background
                WINDOW.blit(BACKGROUND, (0, 0))
                self.bg_animated.render()

                # Draw the icons and text
                WINDOW.blit(TORPEDO_ICON, (50, 1010))
                WINDOW.blit(self.text_torpedoes, (10, 1015))
                WINDOW.blit(PLAYER_ICON, (1820, 1010))
                WINDOW.blit(self.text_player_lives, (1880, 1015))
                WINDOW.blit(self.score_text, (782, 20))

                # Draw player projectiles
                self.lasers_group.draw(WINDOW)
                self.torpedoes_group.draw(WINDOW)

                # Draw player ship
                self.player_group.draw(WINDOW)
                self.player_ship.move(DeltaTime, WINDOW_LIMIT)

                # Draw and animate enemy ships, projectiles and explosions
                for enemy in iter(self.enemy_ships_group):
                    if current_time - enemy.last_shot > random.randint(1000, 3500):
                        self.enemy_lasers_group.add(enemy.create_projectile(ENEMY_PROJECTILE, DeltaTime, 1080))
                        pygame.mixer.Sound.play(ENEMY_LASER_SOUND)
                self.enemy_ships_group.draw(WINDOW)
                for enemy in iter(self.enemy_ships_group):
                    enemy.move(DeltaTime, HEIGHT)
                for enemy in iter(self.enemy_ships_advanced_group):
                    if current_time - enemy.last_shot > random.randint(1000, 3500):
                        self.enemy_lasers_group.add(enemy.create_projectile(ENEMY_ADVANCED_PROJECTILE, DeltaTime, 1080))
                        pygame.mixer.Sound.play(ENEMY_ADVANCED_LASER_SOUND)
                self.enemy_ships_advanced_group.draw(WINDOW)
                for enemy in iter(self.enemy_ships_advanced_group):
                    enemy.move(DeltaTime, HEIGHT)
                self.enemy_lasers_group.draw(WINDOW)
                self.explosion_group.draw(WINDOW)

                # Check if an enemy is hit by laser
                self.enemy_kill = pygame.sprite.groupcollide(self.lasers_group, self.enemy_ships_group, True, True)
                if self.enemy_kill:
                    self.enemy_destroyed(self.enemy_kill, True)

                self.enemy_advanced_kill = pygame.sprite.groupcollide(self.lasers_group,
                                                                      self.enemy_ships_advanced_group, True, True)
                if self.enemy_advanced_kill:
                    self.advanced_enemy_destroyed(self.enemy_advanced_kill, True)

                # Check if an enemy is hit by torpedo
                self.torpedo_hit_enemy = pygame.sprite.groupcollide(self.torpedoes_group, self.enemy_ships_group, True,
                                                                    False)
                self.torpedo_hit_advanced_enemy = pygame.sprite.groupcollide(self.torpedoes_group,
                                                                             self.enemy_ships_advanced_group, True,
                                                                             False)
                if self.torpedo_hit_enemy or self.torpedo_hit_advanced_enemy:
                    if self.torpedo_hit_enemy:
                        self.enemy_destroyed(self.enemy_ships_group, False)
                        self.advanced_enemy_destroyed(self.enemy_ships_advanced_group, False)
                    if self.torpedo_hit_advanced_enemy:
                        self.enemy_destroyed(self.enemy_ships_group, False)
                        self.advanced_enemy_destroyed(self.torpedo_hit_advanced_enemy, False)
                    pygame.mixer.Sound.play(ENEMY_EXPLOSION_SOUND)
                    pygame.mixer.Sound.play(ENEMY_ADVANCED_EXPLOSION_SOUND)
                    self.enemy_ships_group.empty()
                    self.enemy_ships_advanced_group.empty()

                # Check if an enemy collided with player ship or if an enemy killed player ship
                self.crash = pygame.sprite.groupcollide(self.player_group, self.enemy_ships_group, True, True)
                self.crash_advanced = pygame.sprite.groupcollide(self.player_group, self.enemy_ships_advanced_group,
                                                                 True, True)
                self.player_kill = pygame.sprite.groupcollide(self.enemy_lasers_group, self.player_group, True, True)
                if self.crash or self.player_kill or self.crash_advanced:
                    pygame.mixer.Sound.play(PLAYER_EXPLOSION_SOUND)
                    if self.crash or self.crash_advanced:
                        explosion_player = Explosion(self.player_ship.rect[0], self.player_ship.rect[1],
                                                     EXPLOSION_PLAYER_CRASH_SPRITES)
                        self.explosion_group.add(explosion_player)
                        if self.crash:
                            self.score += 10
                        if self.crash_advanced:
                            self.score += 50
                    if self.player_kill:
                        explosion_player = Explosion(self.player_ship.rect[0], self.player_ship.rect[1],
                                                     EXPLOSION_PLAYER_SPRITES)
                        self.explosion_group.add(explosion_player)
                    self.player_ship.player_lives -= 1
                    self.player_ship.kill()
                    self.death_time = pygame.time.get_ticks()

                # Check if player group is empty and add draw new player ship sprite if player has lives left
                if len(self.player_group) == 0:
                    if self.player_ship.player_lives > 0 and current_time - self.death_time > 1000:
                        self.player_group.add(self.player_ship)
                        self.torpedoes = 3
                        self.player_ship.rect = self.player_ship.image.get_rect(center=(960, 1080))

                # Check if enemies are less than max number of enemies and add more
                if self.max_enemies > len(self.enemy_ships_group) >= 0 and current_time - self.enemy_spawn_time > 1000:
                    self.enemy_ships_group.add(EnemyShip(1920, ENEMY_SHIP_SPRITES))
                    self.enemy_spawn_time = pygame.time.get_ticks()
                    if self.score / 100 >= self.max_enemies:
                        self.max_enemies += 2

                # Check kill count and spawn an advanced enemy for every 10 regular enemies killed:
                if self.kill_count >= 10:
                    self.enemy_ships_advanced_group.add(EnemyShipAdvanced(1920, ENEMY_SHIP_ADVANCED_SPRITES))
                    self.kill_count = 0

                # Check for events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit_game()

                    # Firing projectiles
                    if event.type == pygame.KEYDOWN:
                        if self.player_group:
                            if event.key == pygame.K_SPACE and current_time - self.player_ship.last_shot > 150:
                                self.lasers_group.add(self.player_ship.create_projectile("laser", PLAYER_LASER,
                                                                                         DeltaTime))
                                pygame.mixer.Sound.play(PLAYER_LASER_SOUND)
                            if (event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL) and self.torpedoes > 0:
                                self.torpedoes_group.add(self.player_ship.create_projectile("torpedo", PLAYER_TORPEDO,
                                                                                            DeltaTime))
                                pygame.mixer.Sound.play(PLAYER_TORPEDO_SOUND)
                                self.torpedoes -= 1
                                self.text_torpedoes = self.font.render(str(self.torpedoes), True, "green", None)
                        if event.key == pygame.K_BACKSPACE:
                            self.player_ship.player_lives = 3

                        # Game menus - FIX THIS!
                        if event.key == pygame.K_p:
                            self.pause = not self.pause

                        if event.key == pygame.K_q:
                            exit_game()

                        if event.key == pygame.K_m:
                            game.game()

                # Award lives and torpedoes on milestones:
                if self.score / 1000 >= self.life_threshold:
                    self.life_threshold += 2
                    self.player_ship.player_lives += 1
                if self.score / 1000 >= self.torpedo_threshold:
                    self.torpedo_threshold += 1
                    self.torpedoes += 1

                # Update background and groups
                self.bg_animated.update()
                self.player_group.update()
                self.lasers_group.update()
                self.torpedoes_group.update()
                self.enemy_ships_group.update()
                self.enemy_ships_advanced_group.update()
                self.enemy_lasers_group.update()
                self.explosion_group.update()

                # Update the player attributes
                self.score_text = self.font.render(f"SCORE: {self.score:010d}", True, "green", None)
                self.text_torpedoes = self.font.render(str(self.torpedoes), True, "green", None)
                self.text_player_lives = self.font.render(str(self.player_ship.player_lives), True, "green", None)

                # Scale, update the screen and get ticks
                pygame.transform.scale(WINDOW, (WIDTH, HEIGHT), RESOLUTION)
                pygame.display.update()
                FramesPerSec.tick(FPS)

            # Resume paused game - Make part of menu
            else:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.pause = not self.pause
                        if event.key == pygame.K_q:
                            exit_game()

    def how_to_play(self):
        run = True
        self.player_group.empty()
        self.player_group.add(self.player_ship)
        self.bg_animated.movingSpeed_small_stars = 30 * DeltaTime
        self.bg_animated.movingSpeed_stars = 10 * DeltaTime
        while run:
            self.menu_animations()
            WINDOW.blit(HOW_TO_PLAY, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.bg_animated.movingSpeed_small_stars = 3000 * DeltaTime
                        self.bg_animated.movingSpeed_stars = 1000 * DeltaTime
                        run = False
            pygame.transform.scale(WINDOW, (WIDTH, HEIGHT), RESOLUTION)
            pygame.display.update()
            # FramesPerSec.tick(FPS)

    def high_score(self):  # FIX THIS!
        self.menu_animations()

        pygame.transform.scale(WINDOW, (WIDTH, HEIGHT), RESOLUTION)
        pygame.display.update()
        FramesPerSec.tick(FPS)

    def quit_game(self):  # FIX THIS!
        pass

    def main_menu(self):  # FIX THIS!
        while True:
            self.menu_animations()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game()

            pygame.transform.scale(WINDOW, (WIDTH, HEIGHT), RESOLUTION)
            pygame.display.update()
            FramesPerSec.tick(FPS)

    def game(self):  # FIX THIS!
        pygame.mixer.Sound.play(MENU_MUSIC)
        self.player_group.empty()
        self.player_group.add(self.player_ship)
        self.bg_animated.movingSpeed_small_stars = 2000 * DeltaTime
        self.bg_animated.movingSpeed_stars = 500 * DeltaTime
        while True:
            game.menu_animations()
            WINDOW.blit(TITLE, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        self.player_group.empty()
                        pygame.mixer.fadeout(2000)
                        pygame.mixer.Sound.play(GAMEPLAY_MUSIC, -1, fade_ms=5000)
                        Game().new_game()
                    if event.key == pygame.K_s:
                        game.high_score()
                    if event.key == pygame.K_h:
                        game.how_to_play()
            pygame.transform.scale(WINDOW, (WIDTH, HEIGHT), RESOLUTION)
            pygame.display.update()
            FramesPerSec.tick(FPS)


# Initializing
pygame.mixer.pre_init(44100, 16, 2, 1096)
pygame.init()


# Game global parameters
WIDTH, HEIGHT = get_monitors()[0].width, get_monitors()[0].height
RESOLUTION = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
WINDOW = pygame.Surface((1920, 1080))
WINDOW_LIMIT = WINDOW.get_rect()
GAME_START = pygame.image.load("./ASSETS/background.png").convert()
BACKGROUND = pygame.image.load("./ASSETS/background.png").convert()
SMALL_STARS = pygame.image.load("./ASSETS/stars_small.png").convert_alpha()
BIG_STARS = pygame.image.load("./ASSETS/stars_big.png").convert_alpha()

# Animation sprites
EXPLOSION_ENEMY_SPRITES = SpriteList("./ASSETS/EXPLOSION_ENEMY/explosion_enemy*.png").image_list()
EXPLOSION_PLAYER_CRASH_SPRITES = SpriteList("./ASSETS/EXPLOSION_PLAYER_CRASH/explosion_player_crash*.png").image_list()
EXPLOSION_PLAYER_SPRITES = SpriteList("./ASSETS/EXPLOSION_PLAYER/explosion_player*.png").image_list()
PLAYER_SHIP_SPRITES = SpriteList("./ASSETS/PLAYER/player*.png").image_list()
ENEMY_SHIP_SPRITES = SpriteList("./ASSETS/ENEMY/enemy*.png").image_list()
ENEMY_SHIP_ADVANCED_SPRITES = SpriteList("./ASSETS/ENEMY_ADVANCED/enemy_advanced*.png").image_list()

# Game audio assets
audio_assets = {}
load_sounds(audio_assets)
PLAYER_LASER_SOUND = pygame.mixer.Sound(audio_assets['player_laser'])
PLAYER_LASER_SOUND.set_volume(0.3)
PLAYER_TORPEDO_SOUND = pygame.mixer.Sound(audio_assets['player_torpedo'])
PLAYER_TORPEDO_SOUND.set_volume(0.1)
PLAYER_EXPLOSION_SOUND = pygame.mixer.Sound(audio_assets['player_explosion'])
PLAYER_EXPLOSION_SOUND.set_volume(0.2)
ENEMY_LASER_SOUND = pygame.mixer.Sound(audio_assets['enemy_laser'])
ENEMY_LASER_SOUND.set_volume(0.1)
ENEMY_ADVANCED_LASER_SOUND = pygame.mixer.Sound(audio_assets['enemy_advanced_laser'])
ENEMY_ADVANCED_LASER_SOUND.set_volume(0.2)
ENEMY_EXPLOSION_SOUND = pygame.mixer.Sound(audio_assets['enemy_explosion'])
ENEMY_EXPLOSION_SOUND.set_volume(0.1)
ENEMY_ADVANCED_EXPLOSION_SOUND = pygame.mixer.Sound(audio_assets['enemy_advanced_explosion'])
ENEMY_ADVANCED_EXPLOSION_SOUND.set_volume(0.1)
MENU_MUSIC = pygame.mixer.Sound(audio_assets['menu_music'])
GAMEPLAY_MUSIC = pygame.mixer.Sound(audio_assets['gameplay_music'])
GAMEPLAY_MUSIC.set_volume(0.2)

# Icons, counters and misc images
PLAYER_ICON = pygame.image.load("./ASSETS/player_icon.png").convert_alpha()
PLAYER_LASER = pygame.image.load("./ASSETS/laser.png").convert_alpha()
PLAYER_TORPEDO = pygame.image.load("./ASSETS/torpedo.png").convert_alpha()
ENEMY_PROJECTILE = pygame.image.load("./ASSETS/laser_enemy.png").convert_alpha()
ENEMY_ADVANCED_PROJECTILE = pygame.image.load("./ASSETS/laser_enemy_advanced.png").convert_alpha()
TORPEDO_ICON = pygame.image.load("./ASSETS/torpedo_icon.png").convert_alpha()
TORPEDO_COUNT = 3
TITLE = pygame.image.load("./ASSETS/title.png").convert_alpha()
HOW_TO_PLAY = pygame.image.load("./ASSETS/how_to_play.png")

pygame.display.set_caption("Space Gauntlet")
pygame.mouse.set_visible(False)
FPS = 60
FramesPerSec = pygame.time.Clock()
DeltaTime = FramesPerSec.tick(FPS) / 1000
game = Game()
if __name__ == "__main__":
    game.game()
