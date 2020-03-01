import pygame.font

class Scoreboard:
    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats

        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)
        
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def prep_score(self):
        score_str = "score: " + str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, 
            self.settings.bg_colour)
        
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    
    def prep_level(self):
        level_str = "level: " + str( self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, 
            self.settings.bg_colour)
        
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.screen_rect.left + 20
        self.level_rect.top = 20
    
    def prep_high_score(self):
        high_score = "highscore: " + str(self.stats.high_score)
        self.high_score_image = self.font.render(high_score, True, self.text_color, 
            self.settings.bg_colour)
        
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
    
    def reset_score(self):
        self.stats.score = 0
        
        

