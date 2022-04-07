class Settings:
    """a class to store all settings for Alien Invasion"""

    def __init__(self):
        """initialise the game's settings"""
        #screen settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_colour = (230, 230, 230)

        #ship Settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        #bullet Settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = (60, 60, 60)
        self.bullets_allowed = 3

        #Alien Settings
        self.alien_speed = 0.2
        #the amount of pixels the ship will drop upon hitting an edge
        self.fleet_drop_speed = 100
        #fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
