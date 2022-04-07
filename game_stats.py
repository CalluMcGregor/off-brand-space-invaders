class GameStats:
    """track statistics for Alien Invasion"""

    def __init__(self, ai_game):
        """initialise statistics"""
        self.settings = ai_game.settings
        self.reset_stats()
        #start Alien Invasion in an ative state
        self.game_active = True

    def reset_stats(self):
        """initialise statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit
