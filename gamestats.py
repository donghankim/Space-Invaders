
class GameStats:
    def __init__(self, game):
        self.settings = game.settings
        self.reset_stats()
        self.high_score = 0
        self.game_active = False

    def reset_stats(self):
        self.ships_left = self.settings.ship_life
        self.score = 0
        self.level = 1