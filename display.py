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

        for dot in self.game.debug_dots:
            game.pygame.draw.rect(self.win, (255, 0, 0), dot)
    
        for sprite in game.sprites:
            for image in sprite.complete_images:
                self.win.blit(image, sprite.rect)
            game.pygame.draw.circle(self.win, (255, 0, 255), (sprite.x, sprite.y), 3)
            
            corners = sprite.hitbox_human.corners
            for i in range(4):
                start = corners[i]
                end = corners[(i + 1) % 4]
                game.pygame.draw.line(self.win, (255, 0, 0), start, end, 1)
            
            corners = sprite.hitbox_trolley.corners
            for i in range(4):
                start = corners[i]
                end = corners[(i + 1) % 4]
                game.pygame.draw.line(self.win, (0, 255, 0), start, end, 1)
    
        if self.UI:
            self.update_ui()
        
        self.game.pygame.display.update()

    def update_ui(self):
        pass