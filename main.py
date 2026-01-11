import pygame
from random import randint

from objects import Wall, Enemy, Star, Hero
from constants import *

pygame.init()


class Game:
    def __init__(self, win_width, win_height, name="SHOOTER"):
        self.run = True
        self.name = name
        self.win_size = win_width, win_height
        self.all_sprites = pygame.sprite.Group()
        self.barriers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

    def start(self):
        pygame.init()
        self.timer = pygame.time.Clock()
        pygame.display.set_caption(self.name)
        self.window = pygame.display.set_mode(self.win_size)

    def stop(self):
        self.run = False

    def add_barrier(self, platform):
        self.barriers.add(platform)
        self.all_sprites.add(platform)

    def add_enemy(self, enemy):
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def add_stars(self, star):
        self.stars.add(star)

    def add_bullet(self, bullet):
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)

    def draw(self):
        self.all_sprites.draw(self.window)
        self.bombs.draw(self.window)
        self.stars.draw(self.window)
        self.bullets.draw(self.window)

game = Game(win_width, win_height)
game.start()

img = pygame.image.load(img_file_back).convert()
back = pygame.transform.scale(img, (win_width, win_height))

# add hero to sprites
robin = Hero(img_file_hero)
game.all_sprites.add(robin)

pygame.mixer.music.load('static/background_music.mp3')
pygame.mixer.music.play(-1)

# create barriers
for barrier in [
        Wall(50, 150, 480, 50),
        Wall(700, 50, 50, 360),
        Wall(350, 400, 640, 50)
    ]:
    game.add_barrier(barrier)

for _ in range(ENEMY_COUNT):
    enemy = Enemy(150, 460)
    game.add_enemy(enemy)

for _ in range(STAR_COUNT):
    game.add_stars(Star())

bomb = Wall(x=550, y=470, color=C_RED)
game.bombs.add(bomb)

run = True

while game.run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            game.stop()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                robin.x_speed = -5
            elif event.key == pygame.K_RIGHT:
                robin.x_speed = 5
            elif event.key == pygame.K_UP:
                robin.y_speed = -5
            elif event.key == pygame.K_DOWN:
                robin.y_speed = 5
            elif event.key == pygame.K_SPACE:
                robin.shoot(game)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                robin.x_speed = 0
            elif event.key == pygame.K_RIGHT:
                robin.x_speed = 0
            elif event.key == pygame.K_UP:
                robin.y_speed = 0
            elif event.key == pygame.K_DOWN:
                robin.y_speed = 0

    game.all_sprites.update()
    pygame.sprite.groupcollide(game.bombs, game.all_sprites, True, True)

    if pygame.sprite.groupcollide(game.stars, game.barriers, True, False):
        game.add_stars(Star())

    if pygame.sprite.groupcollide(game.bullets, game.enemies, True, True):
        game.add_enemy(Enemy(randint(0, win_width), randint(0, win_height)))
        robin.enemies_killed += 1

    pygame.sprite.groupcollide(game.barriers, game.bullets, False, True)

    if pygame.sprite.spritecollide(robin, game.enemies, False):
        robin.lives -= 1
        robin.rect.x = x_start
        robin.rect.y = y_start
        if robin.lives <= 0:
            print(f"Game Over!\nYour result: Stars: {robin.stars_collected} | Enemies Killed: {robin.enemies_killed}")
            robin.kill()
            game.stop()

    if pygame.sprite.spritecollide(robin, game.barriers, False):
        robin.rect.x -= robin.x_speed
        robin.rect.y -= robin.y_speed

    if pygame.sprite.spritecollide(robin, game.stars, True):
        robin.stars_collected += 1
        game.add_stars(Star())

    if robin.rect.top < 0 or robin.rect.bottom > win_height:
        robin.rect.y -= robin.y_speed
    if (robin.rect.right > right_bound and robin.x_speed > 0
        or robin.rect.left < left_bound and robin.x_speed < 0):
        robin.rect.x -= robin.x_speed
        shift -= robin.x_speed
        for s in game.all_sprites:
            s.rect.x -= robin.x_speed
        for s in game.bombs:
            s.rect.x -= robin.x_speed

    shift += speed
    local_shift = shift % win_width
    game.window.blit(back, (local_shift, 0))
    if local_shift != 0:
        game.window.blit(back, (local_shift - win_width, 0))

    game.draw()

    font = pygame.font.Font(None, 36)
    stats_text = f"Lives: {robin.lives} | Stars: {robin.stars_collected} | Enemies Killed: {robin.enemies_killed}"
    text = font.render(stats_text, True, C_RED)
    game.window.blit(text, (10, 10))

    pygame.display.update()

    game.timer.tick(FPS)