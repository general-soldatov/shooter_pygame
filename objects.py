import pygame
from random import randint

from constants import *

class Wall(pygame.sprite.Sprite):
    def __init__(self, x=20, y=0, width=120, height=120, color=C_GREEN):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x=20, y=0, filename=img_file_enemy, width=120, height=120):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load(filename), (width, height)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += randint(-10, 10)
        self.rect.y += randint(-5, 5)

class Star(pygame.sprite.Sprite):
    def __init__(self, width=50, height=50):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(C_YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = randint(0, win_width - 20), randint(0, win_height - 20)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width=5, height=5):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(C_RED)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        if self.rect.y < win_height:
            self.rect.y += 5
        self.remove()

class Hero(pygame.sprite.Sprite):
    """
    Person Hero
    """
    def __init__(self, filename, x_speed=0, y_speed=0, x=left_bound, y=0, width=120, height=120):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(filename), (width, height)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.lives = 3
        self.stars_collected = 0
        self.enemies_killed = 0
        self.reload_time = 0

        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

    def shoot(self, game):
        bullet = Bullet(x=self.rect.centerx, y=self.rect.centery)
        game.add_bullet(bullet)
