import pygame.font

class Button:

    def __init__(self, ai_game, msg):
        """initialise button attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #set the dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_colour = 252, 211, 157
        self.text_colour = 0, 0, 0
        self.font = pygame.font.Font('invasion.ttf', 36)

        #build the buttons rect attribute and centre it
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

    def _update_msg_position(self):
        """if the button has been moved the text needs moving as well"""
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """draw blank button and then draw message"""
        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
