import pygame
import random

from pygame.sprite import Sprite

class Bullet(Sprite):
    """a class to manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """create a bullet object at the ships current position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.colour = self.settings.bullet_colour

        #create a bullet rect at (0,0) and then set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        #store the bullets position as a decimal value
        self.y = float(self.rect.y)

    def update(self):
        """move the bullet up the screen"""
        #update the decimal position of the bullet
        self.y -= self.settings.bullet_speed
        #update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.colour, self.rect)

class AlienMissile(Sprite):
    """a class to manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """create bullet objects at an aliens current position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.missile_colour = self.settings.missile_colour
        self.aliens = ai_game.aliens

        #create a missile rect at (0, 0) then set correct position
        self.rect = pygame.Rect(0, 0, self.settings.missile_width,
            self.settings.missile_height)
        enemies = []
        for alien in self.aliens:
            enemies.append(alien)
            alien = random.choice(enemies)
        self.rect.midbottom = alien.rect.midbottom

        #store the missiles position as a decimal value
        self.y = float(self.rect.y)

    def update(self):
        """move the missile up the screen"""
        #update the decimal position of the missile
        self.y += self.settings.missile_speed
        #update the rect position
        self.rect.y = self.y

    def draw_missile(self):
        """draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.missile_colour, self.rect)
