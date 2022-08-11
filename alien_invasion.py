import sys
import pygame
import json
import random

from time import sleep
from pygame import mixer

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet, AlienMissile
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

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.sounds = Sounds()
        self.bullets = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #make the play button
        self.play_button = Button(self, "Press 'Enter'")

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
                self._update_bullets_and_missiles()
                self._update_aliens()

                if random.randrange(0, 60) == 1:
                    self._fire_alien_missile()

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
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                self._change_button_colour(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """start a new game and music when the player clicks play"""
        button_clicked = self.play_button.play_rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()
            self.sounds._select_sound()

    def _change_button_colour(self, mouse_pos):
        """change colour of buttons if player hovers over it"""
        hovering_play = self.play_button.play_rect.collidepoint(mouse_pos)
        hovering_easy = self.easy_button.rect.collidepoint(mouse_pos)
        hovering_medium = self.medium_button.rect.collidepoint(mouse_pos)
        hovering_hard = self.hard_button.rect.collidepoint(mouse_pos)

        if hovering_play:
            self.play_button._change_colour("Press 'Enter'")
        else:
            self.play_button._reset_colour("Press 'Enter'")
        if hovering_easy:
            self.easy_button._change_colour('Easy')
        else:
            self.easy_button._reset_colour('Easy')
        if hovering_medium:
            self.medium_button._change_colour('Medium')
        else:
            self.medium_button._reset_colour('Medium')
        if hovering_hard:
            self.hard_button._change_colour('Hard')
        else:
            self.hard_button._reset_colour('Hard')

    def _start_game(self):
        """start a new game"""
        #reset the game settings
        self.settings.initialize_dynamic_settings()

        #reset game stats
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_images()

        #get rid of any remaining aliens and bullets
        self._empty_bullets_aliens_missiles()

        #create a new fleet and center the ship
        self._create_fleet()
        self.ship.centre_ship()

        #start the games music
        self.sounds._play_soundtrack()

        #hide the mouse cursor
        pygame.mouse.set_visible(False)

    def _empty_bullets_aliens_missiles(self):
        """empty bullets and alien groups"""
        self.aliens.empty()
        self.bullets.empty()
        self.missiles.empty()

    def _check_difficulty_buttons(self, mouse_pos):
        """set the appropriate difficulty level"""
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        medium_button_clicked = self.medium_button.rect.collidepoint(
                mouse_pos)
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)

        if easy_button_clicked:
            self.sounds._select_sound()
            self.settings.difficulty_level = 'easy'
        elif medium_button_clicked:
            self.sounds._select_sound()
            self.settings.difficulty_level = 'medium'
        elif hard_button_clicked:
            self.sounds._select_sound()
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
                self._fire_bullet()
        elif event.key == pygame.K_RETURN and not self.stats.game_active:
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
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.sounds._laser_sound()

    def _fire_alien_missile(self):
        """fire an alien missile if limit is not reached"""
        #create a new missile and add it to the missile group"""
        if len(self.missiles) <= self.settings.missiles_allowed:
            new_missile = AlienMissile(self)
            self.missiles.add(new_missile)

    def _update_bullets_and_missiles(self):
        """update position of bullets and get rid of old bullets"""
        #update bullet positions
        self.bullets.update()
        #update missile positions
        self.missiles.update()

        #delete old bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        #delete old missiles
        for missile in self.missiles.copy():
            if missile.rect.top >= self.screen_rect.bottom:
                self.missiles.remove(missile)

        self._check_bullet_alien_collisions()
        self._check_missile_ship_collisions()

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

    def _check_missile_ship_collisions(self):
        """respond to missile ship collisions"""
        #remove all alien missiles, recenter ship, and remove a life
        if pygame.sprite.spritecollideany(self.ship, self.missiles):
            self._ship_hit()

    def start_new_level(self):
        """start a new level of aliens"""
        #destroy existing bullets and create the new fleet
        self.bullets.empty()
        self.missiles.empty()
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

        self.sounds._ship_explosion_sound()
        if self.stats.ships_left > 0:
            #decrement ships_left, and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #remove any remaining aliens and bullets
            self._empty_bullets_aliens_missiles()

            #create a new fleet and centre the ship
            self._create_fleet()
            self.ship.centre_ship()

            #pause the game for a moment
            sleep(0.55)
        else:
            pygame.mixer.music.fadeout(3000)
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
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for missile in self.missiles.sprites():
            missile.draw_missile()

        self.aliens.draw(self.screen)

        #draw the score information
        self.sb.show_information()

        #draw the ship to the screen
        self.ship.blitme()

        #draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_play_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()

        #Make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    #Make the game instance, and run the run_game
    ai = AlienInvasion()
    ai.run_game()
