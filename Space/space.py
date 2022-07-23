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


def load_sprite_animations(sprites):
    for dirpath, dirnames, filenames in os.walk("./ASSETS/SPRITE_ANIMATIONS"):
        for name in dirnames:
            key = name
            path = str(os.path.join(dirpath, name))
            sprites[key] = SpriteList(f"{path}/*.png").image_list()


def load_images(images):
    for dirpath, dirnames, filenames in os.walk("./ASSETS/IMAGES"):
        for name in filenames:
            key = name[:-4]
            path = str(os.path.join(dirpath, name))
            images[key] = pygame.image.load(path).convert_alpha()


def letter_change(pos, number):
    if pos + number > 90:
        pos = 65
    elif pos + number < 65:
        pos = 90
    else:
        pos += number
    return pos


def letter_pos(pos, screen):
    if pos == 0:
        screen.blit(POS_1, (0, 0))
    if pos == 1:
        screen.blit(POS_2, (0, 0))
    if pos == 2:
        screen.blit(POS_3, (0, 0))


class Game:
    """Main game class - everything runs from here"""
    def __init__(self):
        self.bg_animated = MovingBackground(WINDOW, SMALL_STARS, BIG_STARS, 10, 30, DeltaTime)
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

    def enemy_destroyed(self, enemy_group, play, enemy_type):
        for enemy in enemy_group:
            enemy_explosion = Explosion(enemy.rect.x, enemy.rect.y, EXPLOSION_ENEMY_SPRITES)
            self.explosion_group.add(enemy_explosion)
            if enemy_type == 'advanced':
                self.score += 50
            else:
                self.score += 10
                self.kill_count += 1
            if play and enemy_type == 'advanced':
                pygame.mixer.Sound.play(ENEMY_ADVANCED_EXPLOSION_SOUND)
            if play:
                pygame.mixer.Sound.play(ENEMY_EXPLOSION_SOUND)

    def menu_animations(self):
        WINDOW.blit(BACKGROUND, (0, 0))
        self.bg_animated.update()
        self.bg_animated.render()
        self.player_group.draw(WINDOW)
        self.player_group.update()

    def new_game(self):
        run = True
        while run:
            if not self.pause:
                current_time = pygame.time.get_ticks()

                # Draw and render the background
                WINDOW.blit(BACKGROUND, (0, 0))
                self.bg_animated.render()

                # Draw player projectiles
                self.lasers_group.draw(WINDOW)
                self.torpedoes_group.draw(WINDOW)

                # Draw and animate the player ship
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
                    self.enemy_destroyed(self.enemy_kill, True, 'regular')

                self.enemy_advanced_kill = pygame.sprite.groupcollide(self.lasers_group,
                                                                      self.enemy_ships_advanced_group, True, True)
                if self.enemy_advanced_kill:
                    self.enemy_destroyed(self.enemy_advanced_kill, True, 'advanced')

                # Check if an enemy is hit by torpedo
                self.torpedo_hit_enemy = pygame.sprite.groupcollide(self.torpedoes_group, self.enemy_ships_group, True,
                                                                    False)
                self.torpedo_hit_advanced_enemy = pygame.sprite.groupcollide(self.torpedoes_group,
                                                                             self.enemy_ships_advanced_group, True,
                                                                             False)
                if self.torpedo_hit_enemy or self.torpedo_hit_advanced_enemy:
                    if self.torpedo_hit_enemy:
                        self.enemy_destroyed(self.enemy_ships_group, False, 'regular')
                        self.enemy_destroyed(self.enemy_ships_advanced_group, False, 'advanced')
                    if self.torpedo_hit_advanced_enemy:
                        self.enemy_destroyed(self.enemy_ships_group, False, 'regular')
                        self.enemy_destroyed(self.torpedo_hit_advanced_enemy, False, 'advanced')
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
                    if self.player_ship.player_lives > 0:
                        if current_time - self.death_time > 1000:
                            self.player_group.add(self.player_ship)
                            self.torpedoes = 3
                            self.player_ship.rect = self.player_ship.image.get_rect(center=(960, 1080))
                    else:
                        self.end_game_score()
                        run = False

                # Check if enemies are less than max number of enemies and add more
                if self.max_enemies > len(self.enemy_ships_group) >= 0 and current_time - self.enemy_spawn_time > 1000:
                    self.enemy_ships_group.add(EnemyShip(1920, ENEMY_SHIP_SPRITES))
                    self.enemy_spawn_time = pygame.time.get_ticks()
                    # Increase max number of active enemies based on player score
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

                    # Keypress events
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

                        # Cheat for testing purposes - uncomment during development
                        # if event.key == pygame.K_BACKSPACE:
                        #     self.player_ship.player_lives = 3

                        # Game menus - FIX THIS!
                        if event.key == pygame.K_ESCAPE:
                            self.pause = not self.pause

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

                # Draw the icons and text
                WINDOW.blit(TORPEDO_ICON, (50, 1010))
                WINDOW.blit(self.text_torpedoes, (10, 1015))
                WINDOW.blit(PLAYER_ICON, (1820, 1010))
                WINDOW.blit(self.text_player_lives, (1880, 1015))
                WINDOW.blit(self.score_text, (782, 20))

                # Render the player attributes
                self.score_text = self.font.render(f"SCORE: {self.score:010d}", True, "green", None)
                self.text_torpedoes = self.font.render(str(self.torpedoes), True, "green", None)
                self.text_player_lives = self.font.render(str(self.player_ship.player_lives), True, "green", None)

                # Scale, update the screen and get ticks
                pygame.transform.scale(WINDOW, (WIDTH, HEIGHT), RESOLUTION)
                pygame.display.update()
                FramesPerSec.tick(FPS)

            # Pause menu
            else:
                run_pause = True
                WINDOW.blit(PAUSE, (0, 0))
                while run_pause:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                self.pause = not self.pause
                                run_pause = False
                            if event.key == pygame.K_q:
                                run = False
                                run_pause = False
                            if event.key == pygame.K_m:
                                pygame.mixer.pause()
                            if event.key == pygame.K_u:
                                pygame.mixer.unpause()
                    pygame.transform.scale(WINDOW, (WIDTH, HEIGHT), RESOLUTION)
                    pygame.display.update()
                    FramesPerSec.tick(FPS)

    def display_overlay(self, picture):
        run = True
        self.player_group.empty()
        self.player_group.add(self.player_ship)
        self.bg_animated.mov_speed_img_front = 30 * DeltaTime
        self.bg_animated.mov_speed_img_back = 10 * DeltaTime
        while run:
            self.menu_animations()
            WINDOW.blit(picture, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.bg_animated.mov_speed_img_front = 3000 * DeltaTime
                        self.bg_animated.mov_speed_img_back = 1000 * DeltaTime
                        run = False
            pygame.transform.scale(WINDOW, (WIDTH, HEIGHT), RESOLUTION)
            pygame.display.update()
            FramesPerSec.tick(FPS)

    def end_game_score(self):
        run = True
        letters = [65, 65, 65]
        current_index = 0
        score_font = pygame.font.Font("./ASSETS/crystal.ttf", 80)
        while run:
            self.menu_animations()
            WINDOW.blit(GAME_OVER, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        letters[current_index] = letter_change(letters[current_index], 1)
                    if event.key == pygame.K_UP:
                        letters[current_index] = letter_change(letters[current_index], -1)
                    if event.key == pygame.K_RETURN:
                        if current_index < 2:
                            current_index += 1
                        else:
                            with open('scores.txt', 'r') as file:
                                scores_to_sort = file.readlines()
                                scores_dict = {}
                                scores_to_show = [score for score in scores_to_sort if score != "\n"]
                                for score in range(len(scores_to_show)):
                                    scores_to_show[score].replace("\n", "")
                                if len(scores_to_show) > 9:
                                    scores_to_show.pop()
                                scores_to_show.append(f"{chr(letters[0])}{chr(letters[1])}{chr(letters[2])}"
                                                      f"{self.score:010d}")
                                for score in scores_to_show:
                                    scores_dict[score[:3]] = score[3:14]
                                print(scores_dict)
                                file.close()
                            with open('scores.txt', 'w') as file:
                                for score in scores_to_show:
                                    file.write(f"{score}\n")
                            run = False
                    if event.key == pygame.K_BACKSPACE:
                        if current_index > 0:
                            current_index -= 1
            score = score_font.render(f"{chr(letters[0])}{chr(letters[1])}{chr(letters[2])}: {self.score:010d}", True,
                                      "green", None)
            letter_pos(current_index, WINDOW)
            WINDOW.blit(score, (660, 500))

            pygame.transform.scale(WINDOW, (WIDTH, HEIGHT), RESOLUTION)
            pygame.display.update()
            FramesPerSec.tick(FPS)

    def scores(self):
        run = True
        self.player_group.empty()
        self.player_group.add(self.player_ship)
        self.bg_animated.mov_speed_img_front = 30 * DeltaTime
        self.bg_animated.mov_speed_img_back = 10 * DeltaTime
        score_font = pygame.font.Font("./ASSETS/crystal.ttf", 80)
        line = 100
        with open('scores.txt', 'r') as file:
            scores_to_sort = file.readlines()
            scores_to_show = [score for score in scores_to_sort if score != "\n"]
            for score in range(len(scores_to_show)):
                scores_to_show[score].replace("\n", "")
                file.close()
        while run:
            self.menu_animations()
            for score in scores_to_show:
                score_to_show = score_font.render(f"{score}", True, "green", None)
                WINDOW.blit(score_to_show, (660, line))
                line += 100
                if score == scores_to_show[-1]:
                    line = 100
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.bg_animated.mov_speed_img_front = 3000 * DeltaTime
                        self.bg_animated.mov_speed_img_back = 1000 * DeltaTime
                        run = False
            WINDOW.blit(score_font.render("Press Esc to return to Main Menu", True, "green", None), (495, 850))
            pygame.transform.scale(WINDOW, (WIDTH, HEIGHT), RESOLUTION)
            pygame.display.update()
            FramesPerSec.tick(FPS)

    def main_menu(self):
        pygame.mixer.Sound.play(MENU_MUSIC)
        self.player_group.empty()
        self.player_group.add(self.player_ship)
        self.bg_animated.mov_speed_img_front = 2000 * DeltaTime
        self.bg_animated.mov_speed_img_back = 500 * DeltaTime
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
                        self.player_group.add(self.player_ship)
                    if event.key == pygame.K_h:
                        self.display_overlay(HOW_TO_PLAY)
                    if event.key == pygame.K_s:
                        self.scores()
                    if event.key == pygame.K_c:
                        self.display_overlay(CREDITS)
                    if event.key == pygame.K_q:
                        exit_game()
                    if event.key == pygame.K_m:
                        pygame.mixer.pause()
                    if event.key == pygame.K_u:
                        pygame.mixer.unpause()

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
TORPEDO_COUNT = 3

# Animation sprites
sprite_animation_assets = {}
load_sprite_animations(sprite_animation_assets)
PLAYER_SHIP_SPRITES = sprite_animation_assets['PLAYER_SHIP']
EXPLOSION_PLAYER_SPRITES = sprite_animation_assets['EXPLOSION_PLAYER']
EXPLOSION_PLAYER_CRASH_SPRITES = sprite_animation_assets['EXPLOSION_PLAYER_CRASH']
ENEMY_SHIP_SPRITES = sprite_animation_assets['ENEMY_SHIP']
ENEMY_SHIP_ADVANCED_SPRITES = sprite_animation_assets['ENEMY_SHIP_ADVANCED']
EXPLOSION_ENEMY_SPRITES = sprite_animation_assets['EXPLOSION_ENEMY']

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
MENU_MUSIC.set_volume(0.4)
GAMEPLAY_MUSIC = pygame.mixer.Sound(audio_assets['gameplay_music'])
GAMEPLAY_MUSIC.set_volume(0.2)

# Game images
image_assets = {}
load_images(image_assets)
BACKGROUND = image_assets['background']
SMALL_STARS = image_assets['stars_small']
BIG_STARS = image_assets['stars_big']
TITLE = image_assets['title']
PLAYER_LASER = image_assets['laser']
PLAYER_TORPEDO = image_assets['torpedo']
PLAYER_ICON = image_assets['player_icon']
TORPEDO_ICON = image_assets['torpedo_icon']
ENEMY_PROJECTILE = image_assets['laser_enemy']
ENEMY_ADVANCED_PROJECTILE = image_assets['laser_enemy_advanced']
HOW_TO_PLAY = image_assets['how_to_play']
CREDITS = image_assets['credits']
PAUSE = image_assets['pause']
GAME_OVER = image_assets['game_over']
POS_1 = image_assets['pos_1']
POS_2 = image_assets['pos_2']
POS_3 = image_assets['pos_3']


pygame.display.set_caption("Space Gauntlet")
pygame.mouse.set_visible(False)
FPS = 60
FramesPerSec = pygame.time.Clock()
DeltaTime = FramesPerSec.tick(FPS) / 1000
game = Game()

if __name__ == "__main__":
    game.main_menu()
