import sys
import pygame
import json

from time import sleep
from pygame import mixer

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from soundfx import Sounds

class AlienInvasion:
    """Overall class to manage game assets and behaviour"""

    def __init__ (self):
        """initalise the game, and create game resources"""
        pygame.init()
        self.settings = Settings()

        #set the game to full screen mode
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Alien Invasion")

        #create an instance to store game statistics,
        #and create a Scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.sounds = Sounds()
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #make the play button
        self.play_button = Button(self, "Play")

        #make difficulty level buttons
        self._make_difficulty_buttons()

    def _make_difficulty_buttons(self):
        """make buttons that allow player to select difficulty level"""
        self.easy_button = Button(self, "Easy")
        self.medium_button = Button(self, "Medium")
        self.hard_button = Button(self, "Hard")

        #position buttons so they don't overlap
        self.easy_button.rect.top = (
            self.play_button.rect.top + 1.5 * self.play_button.rect.height)
        self.easy_button.rect.right = self.play_button.rect.left - 20
        self.easy_button._update_msg_position()

        self.medium_button.rect.top = self.easy_button.rect.top
        self.medium_button.rect.left = self.play_button.rect.left
        self.medium_button._update_msg_position()

        self.hard_button.rect.top = self.medium_button.rect.top
        self.hard_button.rect.left = self.play_button.rect.right + 20
        self.hard_button._update_msg_position()

    def run_game(self):
        """start the main loop for the game"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """respond to key presses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            #Detect KEYDOWN events
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            #detect KEYUP events
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            #detect mouse events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_difficulty_buttons(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """start a new game and music when the player clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.sounds._play_soundtrack()
            self._start_game()

    def _start_game(self):
        """start a new game"""
        #reset the game settings
        self.settings.initialize_dynamic_settings()

        #reset game stats
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_images()

        #get rid of any remaining aliens and bullets
        self._empty_bullets_aliens()

        #create a new fleet and center the ship
        self._create_fleet()
        self.ship.centre_ship()

        #hide the mouse cursor
        pygame.mouse.set_visible(False)

    def _empty_bullets_aliens(self):
        """empty bullets and alien groups"""
        self.aliens.empty()
        self.bullets.empty()

    def _check_difficulty_buttons(self, mouse_pos):
        """set the appropriate difficulty level"""
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        medium_button_clicked = self.medium_button.rect.collidepoint(
                mouse_pos)
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)

        if easy_button_clicked:
            self.settings.difficulty_level = 'easy'
        elif medium_button_clicked:
            self.settings.difficulty_level = 'medium'
        elif hard_button_clicked:
            self.settings.difficulty_level = 'hard'

    def _check_keydown_events(self, event):
        """respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self._save_high_score()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            if self.stats.game_active:
                if len(self.bullets) < self.settings.bullets_allowed:
                    self._fire_bullet()
                    self.sounds._laser_sound()
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()

    def _check_keyup_events(self, event):
        """respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _save_high_score(self):
        """write the high_score to a file to save it"""
        filename = 'high_score.json'
        with open(filename, 'w') as f:
            json.dump(self.stats.high_score, f)

    def _fire_bullet(self):
        """create a new bullet and add it to the bullets group"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_bullets(self):
        """update position of bullets and get rid of old bullets"""
        #update bullet positions
        self.bullets.update()

        #delete old bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """respond to bullet-alien collisions"""
        #remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sounds._explosion_sound()
            self.sb.prep_score()
            self.sb.check_high_score()

        if len(self.aliens) == 0:
            self.start_new_level()

    def start_new_level(self):
        """start a new level of aliens"""
        #destroy existing bullets and create the new fleet
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()

        #increase level
        self.stats.level += 1
        self.sb.prep_level()

        #change the music speed depending on the level
        self._speed_up_music()

    def _speed_up_music(self):
        """speed up the music"""
        if self.stats.level >= 2:
            self.sounds.faster_1()
        if self.stats.level >= 3:
            self.sounds.faster_2()
        if self.stats.level >= 4:
            self.sounds.faster_3()
        if self.stats.level >= 5:
            self.sounds.fast_4()
        if self.stats.level >= 6:
            self.sounds.faster_5()
        if self.stats.level >= 7:
            self.sounds.faster_6()
        if self.stats.level >= 8:
            self.sounds.faster_7()
        if self.stats.level >= 9:
            self.sounds.faster_8()

    def _update_aliens(self):
        """check if the fleet is at an edge, then update all alien positions"""
        self._check_fleet_edges()
        self.aliens.update()

        #look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """check if any aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen_rect.bottom:
                #treat same as if ship hit
                self._ship_hit()
                break

    def _ship_hit(self):
        """respond to the ship being hit by an alien"""

        if self.stats.ships_left > 0:
            #decrement ships_left, and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #remove any remaining aliens and bullets
            self._empty_bullets_aliens()

            #create a new fleet and centre the ship
            self._create_fleet()
            self.ship.centre_ship()

            #pause the game for a moment
            sleep(0.25)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """create a fleet of aliens"""
        #make an alien and find the number of aliens in a row
        #spacing between each alien is = one aliens width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #determine the number of rows of aliens that fit on screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
            (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """create an alien and place it in the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """respond appropriately if any aliens hit the edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """drop the fleet and change the fleets direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """update images on the screen and flip to the new screen"""
        #redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_colour)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        #draw the score information
        self.sb.show_score()

        #draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()

        #Make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    #Make the game instance, and run the run_game
    ai = AlienInvasion()
    ai.run_game()
