import sys
import os
from time import sleep
import pygame
from settings import Settings
from gamestats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class SpaceAttack:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.create_fleet()
        self.stats = GameStats(self)
        self.play_button = Button(self, "Play")
        self.sb = Scoreboard(self)


    def run_game(self):

        while True:
            self.check_events()

            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self.bullet_limit()
                self.update_aliens()
            
            self.update_screen()
        
        print("game over")
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
                
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_play_button(mouse_pos)
    
    def check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()

            self.aliens.empty()
            self.bullets.empty()
            self.create_fleet()
            self.ship.center_ship()

    def check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
                    
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
                        
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
                        
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()
        
        elif event.key == pygame.K_q:
            sys.exit()
    
    def check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
                    
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
                    
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
                    
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        
    def fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
    
    def bullet_limit(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self.check_bullet_collision()

    def check_bullet_collision(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            self.bullets.empty()
            self.create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
    
            self.sb.prep_score()
            self.sb.check_high_score()
            
    
    def create_alien(self, alien_number, row):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row
        self.aliens.add(alien)
    
    def create_fleet(self):

        #to determine number of alines to put on screen (dummy alien)
        alien = Alien(self)        
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #finding how many rows needed
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #alien fleet added in this loop
        for rows in range(number_rows - 4):
            for i in range(number_aliens_x):
                self.create_alien(i, rows)

    def check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break
    
    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        
        self.settings.fleet_direction *= -1

    def check_alien_bottom(self):
        screen_rect = self.screen.get_rect()
        for aliens in self.aliens.sprites():
            if aliens.rect.bottom >= screen_rect.bottom:
                self.ship_hit()
                break
    
    def update_aliens(self):
        self.check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()
        
        self.check_alien_bottom()
    
    def ship_hit(self):

        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.aliens.empty()
            self.bullets.empty()
            self.create_fleet()
            self.ship.center_ship()

            sleep(0.5)

        else:
            self.stats.reset_stats()
            self.sb.prep_level()
            self.sb.check_high_score()
            self.sb.prep_score()
                          
    def update_screen(self):
        self.screen.fill(self.settings.bg_colour)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        self.aliens.draw(self.screen)
        self.sb.show_score()

        if self.stats.game_active == False:
            self.play_button.draw_button()
            

        pygame.display.flip()
    


if __name__ == '__main__':
    game = SpaceAttack()
    game.run_game()

