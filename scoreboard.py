import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """a class to report scoring information"""

    def __init__(self, ai_game):
        """initialise score keeping attributes"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #font settings for scoring information
        self.text_colour = (252, 211, 157)
        self.font = pygame.font.Font('invasion.ttf', 44)
        self.level_font = pygame.font.Font('invasion.ttf', 32)

        #font settings for quit prompt
        self.prompt_colour = (250, 248, 247)
        self.prompt_font = pygame.font.Font('invasion.ttf', 24)

        #call for the prep of the different images
        self.prep_images()

    def prep_images(self):
        """prepare score, highscore, current level, and ships remaining"""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_quit_reminder()

    def prep_score(self):
        """turn the score into a rendered image"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        score_labelled = f"Score: {score_str}"
        self.score_image = self.font.render(score_labelled, True,
                self.text_colour, self.settings.bg_colour)

        #display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.screen_rect.left + 20
        self.score_rect.top = 5

    def prep_high_score(self):
        """turn the highscore into a rendered image"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        high_score_labelled = f"Highscore: {high_score_str}"
        self.high_score_image = self.font.render(high_score_labelled, True,
            self.text_colour, self.settings.bg_colour)

        #center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """check to see if theres a new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """turn the level into a rendered image"""
        level_str = str(f"Level: {self.stats.level}")
        #this renders the image
        self.level_image = self.level_font.render(level_str, True,
                self.text_colour, self.settings.bg_colour)

        #position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.score_rect.left
        self.level_rect.top = self.score_rect.bottom

    def prep_ships(self):
        """show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left + 1):
            ship = Ship(self.ai_game)
            ship.rect.x = (self.settings.screen_width - ship.rect.width -
                            ship_number * ship.rect.width - 10)
            ship.rect.y = 5
            self.ships.add(ship)

    def prep_quit_reminder(self):
        """remind players how they can quit, using 'Q'"""
        quit_prompt = "Press 'Q' or 'q' to quit!"
        self.quit_image = self.prompt_font.render(quit_prompt, True,
                self.prompt_colour, self.settings.bg_colour)

        #position in the bottom right
        self.quit_rect = self.quit_image.get_rect()
        self.quit_rect.bottom = self.screen_rect.bottom - 10
        self.quit_rect.right = self.screen_rect.right - 10

    def show_information(self):
        """draw scores, level, and ships to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.quit_image, self.quit_rect)
        self.ships.draw(self.screen)
