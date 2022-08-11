import pygame.font

class Button:

    def __init__(self, ai_game, msg):
        """initialise button attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #set the dimensions of the play buttons
        self.play_width, self.play_height = 320, 70

        #set the dimensions of the difficulty buttons
        self.width, self.height = 200, 50

        #other properties of buttons
        self.button_colour = 252, 211, 157
        self.text_colour = 0, 0, 0
        self.font = pygame.font.Font('invasion.ttf', 38)

        #build the play buttons rect attribute and center it
        self.play_rect = pygame.Rect(0, 0, self.play_width, self.play_height)
        self.play_rect.center = self.screen_rect.center
        self.play_rect.centery = self.screen_rect.centery + 120

        #build the buttons rect attribute and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.centery = self.screen_rect.centery + 120

        #the button message needs to be prepped once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """turn msg into a rendered image and centre it on the button"""
        self.msg_image = self.font.render(msg, True, self.text_colour,
                self.button_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def _change_colour(self, msg):
        """change colour of button"""
        self.button_colour = 168, 141, 104
        self.text_colour = 224, 223, 220
        self._prep_msg(msg)

    def _reset_colour(self, msg):
        """reset colours of button"""
        self.button_colour = 252, 211, 157
        self.text_colour = 0, 0, 0
        self._prep_msg(msg)

    def _update_msg_position(self):
        """if the button has been moved the text needs moving as well"""
        self.msg_image_rect.center = self.rect.center

    def draw_play_button(self):
        """draw a blank button for the play button then draw the message"""
        self.screen.fill(self.button_colour, self.play_rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def draw_button(self):
        """draw blank button and then draw message"""
        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
