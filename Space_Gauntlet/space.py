from screeninfo import get_monitors
import pygame.transform
from pygame.locals import *

from player import *
from enemies import *
from animations import *
from misc_funcs import *


class Game:
    """Main game class - everything runs from here"""
    def __init__(self):
        self.bg_animated = MovingBackground(WINDOW, SMALL_STARS, BIG_STARS, 10, 30, DeltaTime)
        self.font = pygame.font.Font("./ASSETS/crystal.ttf", 42)
        self.score = 0
        self.score_text = self.font.render(f"SCORE: {self.score:010d}", True, "green", None)

        # Threshold and event variables
        self.kill_count = 0
        self.life_threshold = 2
        self.torpedo_threshold = 1
        self.max_enemies = 6
        self.enemy_boss_counter = 1
        self.enemy_boss_spawn = False
        self.pause = False

        # Player ship
        self.player_ship = PlayerShip(1920, 1080, PLAYER_SHIP_SPRITES, PLAYER_SHIP_INVULNERABLE_SPRITES)
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
        self.enemy_ships_advanced_group = pygame.sprite.Group()
        self.enemy_boss_group = pygame.sprite.Group()
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
        self.enemy_boss = None
        self.boss_health = ""
        self.enemy_boss_hit = {}
        self.enemy_boss_torpedo_hit = {}
        self.crash_boss = {}

        # Explosions
        self.explosion_group = pygame.sprite.Group()

        # Music track
        self.music_track = GAMEPLAY_MUSIC

    def enemy_shoot_and_move(self, time, enemy_group, projectile, sound):
        for enemy in iter(enemy_group):
            if time - enemy.last_shot > random.randint(1000, 3500):
                self.enemy_lasers_group.add(enemy.create_projectile(projectile, DeltaTime, 1080))
                if PLAY_SOUND:
                    pygame.mixer.Sound.play(sound)
        enemy_group.draw(WINDOW)
        for enemy in iter(enemy_group):
            enemy.move(DeltaTime, HEIGHT)

    def boss_shoot_and_move(self, time, projectile1, projectile2, sound):
        shot_timer = random.randint(1000, 2500)
        if time - self.enemy_boss.last_shot > shot_timer:
            self.enemy_lasers_group.add(self.enemy_boss.create_projectiles(projectile1, DeltaTime, 1080, "narrow"))
            if PLAY_SOUND:
                pygame.mixer.Sound.play(sound)
            if shot_timer % 2 == 0:
                self.enemy_lasers_group.add(self.enemy_boss.create_projectiles(projectile2, DeltaTime, 1080, "wide"))
                if PLAY_SOUND:
                    pygame.mixer.Sound.play(sound)
        self.enemy_boss_group.draw(WINDOW)
        self.enemy_boss.move(DeltaTime, HEIGHT)

    def enemy_destroyed(self, enemy_group, audio_play, play_sound, enemy_type):
        for enemy in enemy_group:
            enemy_explosion = Explosion(enemy.rect.x, enemy.rect.y, EXPLOSION_ENEMY_SPRITES)
            self.explosion_group.add(enemy_explosion)
            if enemy_type == 'advanced':
                self.score += 50
            else:
                self.score += 10
                self.kill_count += 1
            if play_sound:
                if audio_play and enemy_type == 'advanced':
                    pygame.mixer.Sound.play(ENEMY_BIG_EXPLOSION_SOUND)
                if audio_play:
                    pygame.mixer.Sound.play(ENEMY_EXPLOSION_SOUND)

    def boss_hit(self, hit_group, play_sound, play_music, dmg):
        for _ in iter(hit_group):
            self.enemy_boss.life -= dmg
            if self.enemy_boss.life <= 0:
                enemy_explosion = Explosion(self.enemy_boss.rect.x, self.enemy_boss.rect.y,
                                            EXPLOSION_BOSS_SPRITES)
                self.explosion_group.add(enemy_explosion)
                self.music_track = GAMEPLAY_MUSIC
                play_track(self.music_track)
                if play_sound:
                    pygame.mixer.Sound.play(ENEMY_BIG_EXPLOSION_SOUND)
                if not play_music:
                    self.music_track.set_volume(0)
                self.score += 1000
                self.enemy_boss_spawn = False
                self.enemy_boss_group.empty()
                self.enemy_boss = None
                break

    def torpedo_hit(self):
        if self.torpedo_hit_enemy:
            self.enemy_destroyed(self.enemy_ships_group, False, PLAY_SOUND, 'regular')
            self.enemy_destroyed(self.enemy_ships_advanced_group, False, PLAY_SOUND, 'advanced')
        if self.torpedo_hit_advanced_enemy:
            self.enemy_destroyed(self.enemy_ships_group, False, PLAY_SOUND, 'regular')
            self.enemy_destroyed(self.torpedo_hit_advanced_enemy, False, PLAY_SOUND, 'advanced')
        if PLAY_SOUND:
            pygame.mixer.Sound.play(ENEMY_EXPLOSION_SOUND)
            pygame.mixer.Sound.play(ENEMY_BIG_EXPLOSION_SOUND)
        if self.enemy_boss_spawn:
            self.boss_hit(self.enemy_boss_group, PLAY_SOUND, PLAY_MUSIC, 20)
        self.enemy_ships_group.empty()
        self.enemy_ships_advanced_group.empty()

    def menu_animations(self):
        WINDOW.blit(BACKGROUND, (0, 0))
        self.bg_animated.update()
        self.bg_animated.render()
        self.player_group.draw(WINDOW)
        self.player_group.update()

    def init_menu(self, speed_front, speed_back):
        self.player_group.empty()
        self.player_group.add(self.player_ship)
        self.player_ship.rect = self.player_ship.image.get_rect(center=(960, 1028))
        self.bg_animated.mov_speed_img_front = speed_front * DeltaTime
        self.bg_animated.mov_speed_img_back = speed_back * DeltaTime

    def new_game(self):

        # Play/pause music and sounds
        global PLAY_MUSIC
        global PLAY_SOUND

        if not PLAY_MUSIC:
            self.music_track.set_volume(0)

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
                self.enemy_shoot_and_move(current_time, self.enemy_ships_group, ENEMY_PROJECTILE, ENEMY_LASER_SOUND)
                self.enemy_shoot_and_move(current_time, self.enemy_ships_advanced_group, ENEMY_ADVANCED_PROJECTILE,
                                          ENEMY_ADVANCED_LASER_SOUND)
                self.enemy_lasers_group.draw(WINDOW)
                self.explosion_group.draw(WINDOW)

                # Check if an enemy is hit by laser
                self.enemy_kill = pygame.sprite.groupcollide(self.lasers_group, self.enemy_ships_group, True, True,
                                                             collided=lambda s1, s2: pygame.sprite.collide_mask(s1, s2)
                                                             is not None)
                if self.enemy_kill:
                    self.enemy_destroyed(self.enemy_kill, True, PLAY_SOUND, 'regular')

                self.enemy_advanced_kill = pygame.sprite.groupcollide(self.lasers_group,
                                                                      self.enemy_ships_advanced_group, True, True,
                                                                      collided=lambda s1, s2: pygame.sprite.collide_mask
                                                                      (s1, s2) is not None)
                if self.enemy_advanced_kill:
                    self.enemy_destroyed(self.enemy_advanced_kill, True, PLAY_SOUND, 'advanced')

                # Check if an enemy is hit by torpedo
                self.torpedo_hit_enemy = pygame.sprite.groupcollide(self.torpedoes_group, self.enemy_ships_group, True,
                                                                    False, collided=lambda s1, s2: pygame.sprite.
                                                                    collide_mask(s1, s2) is not None)
                self.torpedo_hit_advanced_enemy = pygame.sprite.groupcollide(self.torpedoes_group,
                                                                             self.enemy_ships_advanced_group, True,
                                                                             False, collided=lambda s1, s2: pygame.
                                                                             sprite.collide_mask(s1, s2) is not None)

                self.enemy_boss_torpedo_hit = pygame.sprite.groupcollide(self.torpedoes_group,
                                                                         self.enemy_boss_group, True, False,
                                                                         collided=lambda s1, s2: pygame.sprite.
                                                                         collide_mask(s1, s2) is not None)

                if self.torpedo_hit_enemy or self.torpedo_hit_advanced_enemy or self.enemy_boss_torpedo_hit:
                    self.torpedo_hit()

                # Check if an enemy collided with player ship or if an enemy killed player ship
                if current_time - self.death_time > 3000:
                    self.player_ship.invulnerable = False

                    self.crash = pygame.sprite.groupcollide(self.player_group, self.enemy_ships_group, True, True,
                                                            collided=lambda s1, s2: pygame.sprite.collide_mask(s1, s2)
                                                            is not None)
                    self.crash_advanced = pygame.sprite.groupcollide(self.player_group, self.enemy_ships_advanced_group,
                                                                     True, True, collided=lambda s1, s2: pygame.sprite.
                                                                     collide_mask(s1, s2) is not None)

                    self.player_kill = pygame.sprite.groupcollide(self.enemy_lasers_group, self.player_group, True,
                                                                  True, collided=lambda s1, s2: pygame.sprite.
                                                                  collide_mask(s1, s2) is not None)
                    if self.crash or self.player_kill or self.crash_advanced or self.crash_boss:
                        if PLAY_SOUND:
                            pygame.mixer.Sound.play(PLAYER_EXPLOSION_SOUND)
                        if self.crash or self.crash_advanced or self.crash_boss:
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
                else:
                    self.player_ship.invulnerable = True

                # Check if enemies are less than max number of enemies and add more
                if not self.enemy_boss_spawn:
                    if self.max_enemies > len(self.enemy_ships_group) >= 0 and current_time - self.enemy_spawn_time > \
                            1000:
                        self.enemy_ships_group.add(EnemyShip(1920, ENEMY_SHIP_SPRITES))
                        self.enemy_spawn_time = pygame.time.get_ticks()
                        # Increase max number of active enemies based on player score
                        if self.score / 100 >= self.max_enemies:
                            self.max_enemies += 2

                    # Check kill count and spawn an advanced enemy for every 10 regular enemies killed
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
                                if PLAY_SOUND:
                                    pygame.mixer.Sound.play(PLAYER_LASER_SOUND)
                            if (event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL) and self.torpedoes > 0:
                                self.torpedoes_group.add(self.player_ship.create_projectile("torpedo", PLAYER_TORPEDO,
                                                                                            DeltaTime))
                                if PLAY_SOUND:
                                    pygame.mixer.Sound.play(PLAYER_TORPEDO_SOUND)
                                self.torpedoes -= 1

                        # Cheat for testing purposes - uncomment during development
                        # if event.key == pygame.K_BACKSPACE:
                        #     self.player_ship.player_lives = 3

                        # Pause / Unpause
                        if event.key == pygame.K_ESCAPE:
                            self.pause = not self.pause

                # Award lives and torpedoes on milestones:
                if self.score / 1000 >= self.life_threshold:
                    self.life_threshold += 2
                    self.player_ship.player_lives += 1
                if self.score / 1000 >= self.torpedo_threshold:
                    self.torpedo_threshold += 1
                    self.torpedoes += 1

                # Check boss attributes and update

                # Check points and spawn a boss every 3000 points
                if self.score / 3000 >= self.enemy_boss_counter:
                    self.enemy_boss = EnemyBoss(1920, ENEMY_BOSS_SPRITES)
                    self.enemy_boss_spawn = True
                    self.enemy_boss_group.add(self.enemy_boss)
                    self.enemy_boss_counter += 1
                    self.music_track = BOSS_MUSIC
                    play_track(self.music_track)
                    if not PLAY_MUSIC:
                        self.music_track.set_volume(0)

                if self.enemy_boss_spawn:
                    self.enemy_boss.update()
                    self.boss_shoot_and_move(current_time, ENEMY_BOSS_PROJECTILE_NARROW,
                                             ENEMY_BOSS_PROJECTILE_WIDE, ENEMY_ADVANCED_LASER_SOUND)
                    self.enemy_boss_hit = pygame.sprite.groupcollide(self.lasers_group, self.enemy_boss_group, True,
                                                                     False, collided=lambda s1, s2: pygame.sprite.
                                                                     collide_mask(s1, s2) is not None)
                    if self.enemy_boss_hit:
                        self.boss_hit(self.enemy_boss_group, PLAY_SOUND, PLAY_MUSIC, 1)

                    self.crash_boss = pygame.sprite.groupcollide(self.player_group, self.enemy_boss_group, True, False,
                                                                 collided=lambda s1, s2: pygame.sprite.collide_mask(s1,
                                                                                                                    s2)
                                                                 is not None)
                    self.boss_health = self.font.render(f"BOSS HEALTH  {self.enemy_boss.life:03d}", True, "green", None)

                # Update background and groups
                self.bg_animated.update()
                self.player_group.update()
                self.lasers_group.update()
                self.torpedoes_group.update()
                self.enemy_ships_group.update()
                self.enemy_ships_advanced_group.update()
                self.enemy_lasers_group.update()
                self.explosion_group.update()

                # Render the player attributes
                self.score_text = self.font.render(f"SCORE: {self.score:010d}", True, "green", None)
                self.text_torpedoes = self.font.render(str(self.torpedoes), True, "green", None)
                self.text_player_lives = self.font.render(str(self.player_ship.player_lives), True, "green", None)

                # Draw the icons and text
                WINDOW.blit(TORPEDO_ICON, (50, 1010))
                WINDOW.blit(self.text_torpedoes, (10, 1015))
                WINDOW.blit(PLAYER_ICON, (1820, 1010))
                WINDOW.blit(self.text_player_lives, (1880, 1015))
                WINDOW.blit(self.score_text, (782, 20))

                # Blit boss health separately, to not be drawn under other images
                if self.enemy_boss_spawn:
                    WINDOW.blit(self.boss_health, (798, 60))

                # Scale, update the screen and get ticks
                screen_update(WINDOW, WIDTH, HEIGHT, RESOLUTION, FramesPerSec, FPS)

                # Check if player group is empty and add draw new player ship sprite if player has lives left
                if len(self.player_group) == 0:
                    if self.player_ship.player_lives > 0:
                        if current_time - self.death_time > 1000:
                            self.player_group.add(self.player_ship)
                            self.torpedoes = 3
                            self.player_ship.rect = self.player_ship.image.get_rect(center=(960, 1028))
                    else:
                        self.game_over()
                        run = False

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
                                run_pause = False
                                run = False
                            if event.key == pygame.K_m:
                                PLAY_MUSIC = mute_unmute_music(PLAY_MUSIC, self.music_track, 0.2)
                            if event.key == pygame.K_s:
                                PLAY_SOUND = not PLAY_SOUND
                    screen_update(WINDOW, WIDTH, HEIGHT, RESOLUTION, FramesPerSec, FPS)

    def sub_menu(self, picture):
        run = True
        self.init_menu(30, 10)
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
            screen_update(WINDOW, WIDTH, HEIGHT, RESOLUTION, FramesPerSec, FPS)

    def game_over(self):
        run = True
        letters = [65, 65, 65]
        letter_index = 0
        score_font = pygame.font.Font("./ASSETS/crystal.ttf", 80)
        self.init_menu(30, 10)
        while run:
            self.menu_animations()
            WINDOW.blit(GAME_OVER, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        letters[letter_index] = letter_change(letters[letter_index], 1)
                    if event.key == pygame.K_UP:
                        letters[letter_index] = letter_change(letters[letter_index], -1)
                    if event.key == pygame.K_LEFT:
                        if letter_index > 0:
                            letter_index -= 1
                    if event.key == pygame.K_RIGHT:
                        if letter_index < 2:
                            letter_index += 1
                    if event.key == pygame.K_RETURN:
                        save_new_score(UserScore(random.randint(0, 100), f"{chr(letters[0])}{chr(letters[1])}"
                                                                         f"{chr(letters[2])}", self.score))
                        run = False

            score = score_font.render(f"{chr(letters[0])}{chr(letters[1])}{chr(letters[2])}: {self.score:010d}", True,
                                      "green", None)
            letter_pos(letter_index, POS_1, POS_2, POS_3, WINDOW)
            WINDOW.blit(score, (660, 500))
            screen_update(WINDOW, WIDTH, HEIGHT, RESOLUTION, FramesPerSec, FPS)
        self.highscores()

    def highscores(self):
        run = True
        self.init_menu(30, 10)
        score_font = pygame.font.Font("./ASSETS/crystal.ttf", 80)
        line = 100
        score_list = high_scores()
        while run:
            self.menu_animations()
            for userscore in score_list:
                score_to_show = score_font.render(f"{userscore.user}: {userscore.score:010d}", True, "green", None)
                WINDOW.blit(score_to_show, (660, line))
                line += 100
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
            screen_update(WINDOW, WIDTH, HEIGHT, RESOLUTION, FramesPerSec, FPS)

    def main_menu(self):

        # Play/pause music and sounds
        global PLAY_MUSIC
        global PLAY_SOUND

        pygame.mixer.Sound.play(MENU_MUSIC)
        self.init_menu(2000, 500)
        while True:
            game.menu_animations()
            WINDOW.blit(TITLE, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        self.player_group.empty()
                        play_track(self.music_track)
                        Game().new_game()
                        play_track(MENU_MUSIC)
                        if not PLAY_MUSIC:
                            MENU_MUSIC.set_volume(0)
                        else:
                            MENU_MUSIC.set_volume(0.2)
                        self.init_menu(2000, 500)
                    if event.key == pygame.K_i:
                        self.sub_menu(INSTRUCTIONS)
                    if event.key == pygame.K_h:
                        self.highscores()
                    if event.key == pygame.K_c:
                        self.sub_menu(CREDITS)
                    if event.key == pygame.K_q:
                        exit_game()
                    if event.key == pygame.K_m:
                        PLAY_MUSIC = mute_unmute_music(PLAY_MUSIC, MENU_MUSIC, 0.2)
                    if event.key == pygame.K_s:
                        PLAY_SOUND = not PLAY_SOUND
            screen_update(WINDOW, WIDTH, HEIGHT, RESOLUTION, FramesPerSec, FPS)


# Initializing
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])

# Game global parameters
WIDTH, HEIGHT = [(m.width, m.height) for m in get_monitors() if m.is_primary][0]
FLAGS = FULLSCREEN | DOUBLEBUF
RESOLUTION = pygame.display.set_mode((WIDTH, HEIGHT), FLAGS, 16)
WINDOW = pygame.Surface((1920, 1080))
WINDOW_LIMIT = WINDOW.get_rect()
TORPEDO_COUNT = 3
PLAY_MUSIC = True
PLAY_SOUND = True

# Animation sprites
sprite_animation_assets = load_sprite_animations()
PLAYER_SHIP_SPRITES = sprite_animation_assets['PLAYER_SHIP']
PLAYER_SHIP_INVULNERABLE_SPRITES = sprite_animation_assets['PLAYER_SHIP_INVULNERABLE']
EXPLOSION_PLAYER_SPRITES = sprite_animation_assets['EXPLOSION_PLAYER']
EXPLOSION_PLAYER_CRASH_SPRITES = sprite_animation_assets['EXPLOSION_PLAYER_CRASH']
ENEMY_SHIP_SPRITES = sprite_animation_assets['ENEMY_SHIP']
ENEMY_SHIP_ADVANCED_SPRITES = sprite_animation_assets['ENEMY_SHIP_ADVANCED']
ENEMY_BOSS_SPRITES = sprite_animation_assets['ENEMY_BOSS']
EXPLOSION_ENEMY_SPRITES = sprite_animation_assets['EXPLOSION_ENEMY']
EXPLOSION_BOSS_SPRITES = sprite_animation_assets['EXPLOSION_BOSS']

# Game audio assets
audio_assets = load_sounds()
PLAYER_LASER_SOUND = pygame.mixer.Sound(audio_assets['player_laser'])
PLAYER_LASER_SOUND.set_volume(0.2)
PLAYER_TORPEDO_SOUND = pygame.mixer.Sound(audio_assets['player_torpedo'])
PLAYER_TORPEDO_SOUND.set_volume(0.1)
PLAYER_EXPLOSION_SOUND = pygame.mixer.Sound(audio_assets['player_explosion'])
PLAYER_EXPLOSION_SOUND.set_volume(0.1)
ENEMY_LASER_SOUND = pygame.mixer.Sound(audio_assets['enemy_laser'])
ENEMY_LASER_SOUND.set_volume(0.08)
ENEMY_ADVANCED_LASER_SOUND = pygame.mixer.Sound(audio_assets['enemy_advanced_laser'])
ENEMY_ADVANCED_LASER_SOUND.set_volume(0.1)
ENEMY_EXPLOSION_SOUND = pygame.mixer.Sound(audio_assets['enemy_explosion'])
ENEMY_EXPLOSION_SOUND.set_volume(0.07)
ENEMY_BIG_EXPLOSION_SOUND = pygame.mixer.Sound(audio_assets['enemy_big_explosion'])
ENEMY_BIG_EXPLOSION_SOUND.set_volume(0.1)
MENU_MUSIC = pygame.mixer.Sound(audio_assets['menu_music'])
MENU_MUSIC.set_volume(0.2)
GAMEPLAY_MUSIC = pygame.mixer.Sound(audio_assets['gameplay_music'])
GAMEPLAY_MUSIC.set_volume(0.2)
BOSS_MUSIC = pygame.mixer.Sound(audio_assets['boss_music'])
BOSS_MUSIC.set_volume(0.2)

# Game images
image_assets = load_images()
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
ENEMY_BOSS_PROJECTILE_NARROW = image_assets['laser_boss_narrow']
ENEMY_BOSS_PROJECTILE_WIDE = image_assets['laser_boss_wide']
INSTRUCTIONS = image_assets['instructions']
CREDITS = image_assets['credits']
PAUSE = image_assets['pause']
GAME_OVER = image_assets['game_over']
POS_1 = image_assets['pos_1']
POS_2 = image_assets['pos_2']
POS_3 = image_assets['pos_3']


pygame.display.set_caption("Space Gauntlet")
pygame.display.set_icon(PLAYER_ICON)
pygame.mouse.set_visible(False)
FPS = 60
FramesPerSec = pygame.time.Clock()
DeltaTime = FramesPerSec.tick(FPS) / 1000
game = Game()

if __name__ == "__main__":
    game.main_menu()
