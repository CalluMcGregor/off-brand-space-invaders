class Settings:
    """a class to store all settings for Alien Invasion"""

    def __init__(self):
        """initialise the game's settings"""
        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (57, 99, 87)

        #ship Settings
        self.ship_limit = 2

        #bullet Settings
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_colour = (52, 235, 58)
        self.bullets_allowed = 3

        #Alien Settings
        #the amount of pixels the ship will drop upon hitting an edge
        self.fleet_drop_speed = 100

        #how quickly the game speeds up
        self.speedup_scale = 1.2

        #how quickly the alien point values increase
        self.score_scale = 1.5

        self.difficulty_level = 'medium'

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """initialize settings that change throughout the game"""
        if self.difficulty_level == 'easy':
            self.ship_limit = 2
            self.bullets_allowed = 6
            self.ship_speed = 1
            self.bullet_speed = 1.5
            self.alien_speed = 0.3
        elif self.difficulty_level == 'medium':
            self.ship_limit = 1
            self.bullets_allowed = 4
            self.ship_speed = 1.5
            self.bullet_speed = 2.2
            self.alien_speed = 0.6
        elif self.difficulty_level == 'hard':
            self.ship_limit = 0
            self.bullets_allowed = 3
            self.ship_speed = 3
            self.bullet_speed = 3.0
            self.alien_speed = 1.2

        #fleet direction 1 = right, -1 = left
        self.fleet_direction = 1

        #scoring
        self.alien_points = 50

    def increase_speed(self):
        """increase speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

    def set_difficulty(self, diff_setting):
        """set the difficulty setting"""
        if diff_setting == 'easy':
            print('easy')
        elif diff_setting == 'medium':
            pass
        elif diff_setting == 'hard':
            pass
