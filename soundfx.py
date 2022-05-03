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

    def _explosion_sound(self):
        """play an explosion sound"""
        explosion = pygame.mixer.Sound("sounds/explosion.wav")
        explosion.set_volume(0.2)
        pygame.mixer.Sound.play(explosion)

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

    def faster_6(self):
        """play the games soundtrack, way faster"""
        self._stop_unloader()
        pygame.mixer.music.load("sounds/soundtrack35.wav")
        self.music_volume
        pygame.mixer.music.play(-1)

    def faster_7(self):
        """play the games soundtrack, super fast"""
        self._stop_unloader()
        pygame.mixer.music.load("sounds/soundtrack50.wav")
        self.music_volume
        pygame.mixer.music.play(-1)

    def faster_8(self):
        """play the games soundtrack, ultra fast"""
        self._stop_unloader()
        pygame.mixer.music.load("sounds/soundtrack65.wav")
        self.music_volume
        pygame.mixer.music.play(-1)

    def _stop_unloader(self):
        """stop and unload the current music"""
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
