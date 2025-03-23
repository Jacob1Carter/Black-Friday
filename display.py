
class Display:

    def __init__(self, game):
        self.game = game

        self.name = "Black Friday"
        self.WIDTH = 800
        self.HEIGHT = 600
        self.UI = True

        self.win = self.game.pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.game.pygame.display.set_caption(self.game.name)
    
    def update(self):

        pass

        if self.UI:
            self.update_ui()
        
        self.game.pygame.display.update()

    def update_ui(self):
        pass