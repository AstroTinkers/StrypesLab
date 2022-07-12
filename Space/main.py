import pygame


class MovingBackground:
    def __init__(self):
        self.bgimage = pygame.image.load("./ASSETS/stars.png")
        self.rectBGimg = self.bgimage.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = self.rectBGimg.height
        self.bgX2 = 0

        self.movingUpSpeed = 1

    def update(self):
        self.bgY1 += self.movingUpSpeed
        self.bgY2 += self.movingUpSpeed
        if self.bgY1 >= self.rectBGimg.height:
            self.bgY1 = -self.rectBGimg.height
        if self.bgY2 >= self.rectBGimg.height:
            self.bgY2 = -self.rectBGimg.height

    def render(self):
        WINDOW.blit(self.bgimage, (self.bgX1, self.bgY1))
        WINDOW.blit(self.bgimage, (self.bgX2, self.bgY2))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./ASSETS/player.png")
        self.surf = pygame.Surface((50, 50))
        self.rect = self.surf.get_rect(center=(480, 540))
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 250
        self.lasers = []
        self.torpedos = []

    def move(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_w]:
            self.rect.move_ip(0, -10)
        if pressed_key[pygame.K_s]:
            self.rect.move_ip(0, 10)
        if pressed_key[pygame.K_a]:
            self.rect.move_ip(-10, 0)
        if pressed_key[pygame.K_d]:
            self.rect.move_ip(10, 0)
        self.rect.clamp_ip(WINDOW_LIMIT)

    def fire(self, keypress):
        now = pygame.time.get_ticks()
        laser = Projectiles(self.rect.centerx, self.rect.top)
        torpedo = Projectiles(self.rect.centerx, self.rect.top)
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
        if keypress == pygame.K_SPACE:
            self.lasers.append(laser)
        if keypress == pygame.K_RCTRL:
            self.torpedos.append(torpedo)


class Projectiles(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("./ASSETS/laser.png")
        self.torpedo_img = pygame.image.load("./ASSETS/torpedo.png")
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 250

    def update(self):
        self.rect.y += self.speedy

        if self.rect.bottom < 0:
            self.kill()


class Game:
    def __init__(self):
        self.bg_animated = MovingBackground()
        self.pilot = Player()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.pilot)
        self.enemies = pygame.sprite.Group()

    def run(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:  # Firing projectiles
                    if event.key == pygame.K_SPACE:
                        self.pilot.fire(pygame.K_SPACE)

            WINDOW.blit(BACKGROUND, (0, 0))
            self.bg_animated.update()
            self.bg_animated.render()

            for entity in self.all_sprites:
                WINDOW.blit(entity.image, entity.rect)
                entity.move()


            pygame.display.update()
            FramesPerSec.tick(FPS)

        pygame.quit()


# Initializing
pygame.init()

# Game global parameters
FPS = 60
FramesPerSec = pygame.time.Clock()
WIDTH, HEIGHT = 960, 540
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
WINDOW_LIMIT = WINDOW.get_rect()
BACKGROUND = pygame.image.load("./ASSETS/background.png")

pygame.display.set_caption("Space game!")

game = Game()

if __name__ == "__main__":
    game.run()
