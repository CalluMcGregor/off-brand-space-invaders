import pygame
from pygame import mixer

class Sounds:
    """class to handle all the sounds of AlienInvasion"""

    def __init__(self):
        """initialise music attributes"""
        pygame.mixer.init()
        self.music_volume = pygame.mixer.music.set_volume(0.2)

    def _laser_sound(self):
        """play a laser shooting sound"""
        laser = pygame.mixer.Sound("sounds/laser.wav")
        laser.set_volume(0.1)
        pygame.mixer.Sound.play(laser)

    def _select_sound(self):
        """play a menu selection sound"""
        select = pygame.mixer.Sound("sounds/select.wav")
        select.set_volume(0.3)
        pygame.mixer.Sound.play(select)

    def _explosion_sound(self):
        """play an explosion sound"""
        explosion = pygame.mixer.Sound("sounds/explosion.wav")
        explosion.set_volume(0.2)
        pygame.mixer.Sound.play(explosion)

    def _ship_explosion_sound(self):
        """explosion of the ship"""
        ship_explosion = pygame.mixer.Sound("sounds/ship_explosion.wav")
        ship_explosion.set_volume(0.4)
        pygame.mixer.Sound.play(ship_explosion)

    def _play_soundtrack(self):
        """play the games soundtrack"""
        pygame.mixer.music.load("sounds/soundtrack.wav")
        self.music_volume
        pygame.mixer.music.play(-1)

    def faster_1(self):
        """play the games soundtrack, slightly faster"""
        self._stop_unloader()
        pygame.mixer.music.load("sounds/soundtrack05.wav")
        self.music_volume
        pygame.mixer.music.play(-1)

    def faster_2(self):
        """play the games soundtrack, faster still"""
        self._stop_unloader()
        pygame.mixer.music.load("sounds/soundtrack10.wav")
        self.music_volume
        pygame.mixer.music.play(-1)

    def faster_3(self):
        """play the games soundtrack, even faster"""
        self._stop_unloader()
        pygame.mixer.music.load("sounds/soundtrack15.wav")
        self.music_volume
        pygame.mixer.music.play(-1)

    def fast_4(self):
        """play the games soundtrack, more fast"""
        self._stop_unloader()
        pygame.mixer.music.load("sounds/soundtrack20.wav")
        self.music_volume
        pygame.mixer.music.play(-1)

    def faster_5(self):
        """play the games soundtrack, much faster"""
        self._stop_unloader()
        pygame.mixer.music.load("sounds/soundtrack25.wav")
        self.music_volume
        pygame.mixer.music.play(-1)

    def _stop_unloader(self):
        """stop and unload the current music"""
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
