from tools import fprint


class Display:

    def __init__(self, game):
        self.game = game

        self.name = "Black Friday"
        self.WIDTH = 1920
        self.HEIGHT = 1080
        self.UI = True

        self.win = self.game.pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.game.pygame.display.set_caption(self.game.name)
    
    def update(self, game):
    
        for entity in game.entities:
            fprint(entity)
            sprite_path = f"assets/{entity['sprite']}.png"
            sprite_surface = self.game.pygame.image.load(sprite_path)  # Load the sprite as a Surface
            self.win.blit(sprite_surface, (entity["position"]["x"], entity["position"]["y"]))
    
        if self.UI:
            self.update_ui()
        
        self.game.pygame.display.update()

    def update_ui(self):
        pass