from display import Display
import pygame

class Game:

    def __init__(self):
        self.pygame = pygame

        self.name = "Black Friday"
        self.display = Display(self)

    def update(self):
        x, y = pygame.mouse.get_pos()
        keys_pressed = pygame.key.get_pressed() 
        mouse_pressed = pygame.mouse.get_pressed()

        self.display.update()