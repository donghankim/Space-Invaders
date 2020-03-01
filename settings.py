
class Settings:
    def __init__(self):
        #window settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (204, 255, 204)
        
        #ship settings
        self.ship_speed = 8
        self.ship_life = 1

        #bullet settings
        self.bullet_speed = 7
        self.bullet_width = 7
        self.bullet_height = 15
        self.bullet_color = (60,60,60)

        #alien settings
        self.alien_speed = 3.0
        self.fleet_drop_speed = 25
        self.fleet_direction = 1    # 1 represents right; -1 represents left

        #game settings
        self.speedup_scale = 1.5
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

        #score settings
        self.alien_points = 50


    def initialize_dynamic_settings(self):
        # The game settings that will change throughout the game
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        self.fleet_direction = 1
    
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
    
    
