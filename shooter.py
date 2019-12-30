import pygame
import random

# Główne ustawienia
WIDTH = 480
HEIGHT = 600
FPS = 60

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter!")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('arial')


# Klasa dla obiektu czołg
class Tank(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # init Tank
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        state = pygame.key.get_pressed()
        if state[pygame.K_LEFT]:
            self.speedx = -8
        if state[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        # End of screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


# Klasa dla obiektu przeciwnik
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.set_start_position()
        self.speedx = random.randrange(-3, 3)

    def set_start_position(self):
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.set_start_position()


# Klasa dla obiektu naboju
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def new_enemy():
    e = Enemy()
    all_sprites.add(e)
    enemies.add(e)


def show_go_screen():
    draw_text(screen, "Shooter!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Naciśnij spacje aby rozpocząć", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False


# Główna pętla gry
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        # Utworzenie grup obiektów
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        tank = Tank()
        all_sprites.add(tank)
        score = 0

        # Inicjalizacja przeciwników
        for i in range(8):
            new_enemy()

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                tank.shoot()

    # Wywołanie metody update na wszystkich objektach w kolecji.
    all_sprites.update()

    # Sprawdzenie i utworzenie ponownie zestrzelonych obiektów zliczanie punktów
    for items in pygame.sprite.groupcollide(enemies, bullets, True, True):
        score += 1
        new_enemy()

    # Sprawdzenie czy nie został trafiony czołg.
    if pygame.sprite.spritecollide(tank, enemies, False):
        game_over = True

    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen, "Wynik: {}".format(str(score)), 18, WIDTH / 10, 10)
    pygame.display.flip()

pygame.quit()
