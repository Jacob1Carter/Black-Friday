from tools import fprint


class Display:

    def __init__(self, game):
        self.game = game

        self.name = "Black Friday"
        self.WIDTH = 1920
        self.HEIGHT = 1080
        self.UI = True

        if True:
            self.win = self.game.pygame.display.set_mode((900, 500))
        else:
            self.win = self.game.pygame.display.set_mode((self.WIDTH, self.HEIGHT), self.game.pygame.FULLSCREEN | self.game.pygame.NOFRAME | self.game.pygame.SRCALPHA, 32)
        self.game.pygame.display.set_caption(self.game.name)
    
    def update(self, game):
        self.win.fill((0, 0, 0))
    
        for sprite in game.sprites:
            self.win.blit(sprite.image, (sprite.x, sprite.y))
    
        if self.UI:
            self.update_ui()
        
        self.game.pygame.display.update()

    def update_ui(self):
        pass