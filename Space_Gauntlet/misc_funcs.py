import shelve
import pygame
import os


def exit_game():
    pygame.quit()
    exit()


def load_sounds():
    sounds = {}
    for dirpath, dirnames, filenames in os.walk("./ASSETS/SOUNDS"):
        for name in filenames:
            key = name[:-4]
            sounds[key] = os.path.join(dirpath, name)
    return sounds


def load_images():
    images = {}
    for dirpath, dirnames, filenames in os.walk("./ASSETS/IMAGES"):
        for name in filenames:
            key = name[:-4]
            path = str(os.path.join(dirpath, name))
            images[key] = pygame.image.load(path).convert_alpha()
    return images


def letter_change(pos, number):
    if pos + number > 90:
        pos = 65
    elif pos + number < 65:
        pos = 90
    else:
        pos += number
    return pos


def letter_pos(pos, pos1, pos2, pos3, screen):  # Changes position of screen pointer under letter
    if pos == 0:
        screen.blit(pos1, (0, 0))
    if pos == 1:
        screen.blit(pos2, (0, 0))
    if pos == 2:
        screen.blit(pos3, (0, 0))


def save_new_score(score):
    scores_file = shelve.open('scores.txt')
    scores_list = []
    if len(scores_file) > 0:
        scores_list = [UserScore(id_num, value[0], value[1]) for id_num, value in scores_file.items()]
        scores_list = sorted(scores_list, key=lambda x: x.score, reverse=True)
    while len(scores_list) >= 7:
        scores_list.pop()
    scores_list.append(score)
    scores_list = sorted(scores_list, key=lambda x: x.score, reverse=True)
    scores_file.clear()
    for userscore in scores_list:
        scores_file[userscore.id_num] = [userscore.user, userscore.score]
    scores_file.close()


def high_scores():
    scores_file = shelve.open('scores.txt')
    scores_list = []
    for id_num, value in scores_file.items():
        scores_list.append(UserScore(id_num, value[0], value[1]))
    scores_list = [UserScore(id_num, value[0], value[1]) for id_num, value in scores_file.items()]
    scores_file.close()
    return scores_list


def screen_update(window, width, height, resolution, clock, fps):
    pygame.transform.scale(window, (width, height), resolution)
    pygame.display.update()
    clock.tick(fps)


def mute_unmute_music(audio_bool, music, volume):
    audio_bool = not audio_bool
    if audio_bool:
        music.set_volume(volume)
    else:
        music.set_volume(0)
    return audio_bool


def mute_unmute_visualize(bool_var, screen, img_mute, img_unmute, x, y):
    if not bool_var:
        screen.blit(img_mute, (x, y))
    else:
        screen.blit(img_unmute, (x, y))


def play_track(music_track, volume, bool_var):
    pygame.mixer.fadeout(1000)
    music_track.set_volume(volume)
    pygame.mixer.Sound.play(music_track, -1, fade_ms=5000)
    if not bool_var:
        music_track.set_volume(0)


class UserScore:
    """Saves the score with a unique id, to allow for scores with same users' names"""
    def __init__(self, id_num, user, score):
        self.id_num = str(id_num)
        self.user = user
        self.score = score
