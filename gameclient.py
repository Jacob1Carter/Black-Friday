from display import Display
from tools import fprint
import pygame

class Game:

    def __init__(self):
        self.pygame = pygame

        self.name = "Black Friday"
        self.display = Display(self)

        self.inputdata = {
            "keys": {
                "w": 0,
                "a": 0,
                "s": 0,
                "d": 0,
                "SPACE": 0,
                "SHIFT": 0,
                "e": 0,
                "f": 0,
                "r": 0,
                "q": 0,
                "ESC": 0,
                "CTRL": 0
            },
            "mouse_pos": {
                "x": 0,
                "y": 0
            },
            "mouse_buttons": {
                "left": 0,
                "right": 0,
                "middle": 0,
            }
        }

        self.entities = []

    def update_inputs(self):
        x, y = pygame.mouse.get_pos()
        self.inputdata["mouse_pos"]["x"] = x
        self.inputdata["mouse_pos"]["y"] = y
    
        keys_pressed = pygame.key.get_pressed()
        key_mapping = {
            "w": pygame.K_w,
            "a": pygame.K_a,
            "s": pygame.K_s,
            "d": pygame.K_d,
            "SPACE": pygame.K_SPACE,
            "SHIFT": pygame.K_LSHIFT,
            "e": pygame.K_e,
            "f": pygame.K_f,
            "r": pygame.K_r,
            "q": pygame.K_q,
            "ESC": pygame.K_ESCAPE,
            "CTRL": pygame.K_LCTRL
        }
    
        for key, pygame_key in key_mapping.items():
            if keys_pressed[pygame_key]:
                if self.inputdata["keys"][key] > 1:
                    self.inputdata["keys"][key] += 1
                else:
                    self.inputdata["keys"][key] = 2
            else:
                if self.inputdata["keys"][key] > 1:
                    self.inputdata["keys"][key] = 0
                elif self.inputdata["keys"][key] < 1:
                    self.inputdata["keys"][key] = 1
    
        mouse_pressed = pygame.mouse.get_pressed()
        for button, index in zip(["left", "right", "middle"], range(3)):
            if mouse_pressed[index]:
                if self.inputdata["mouse_buttons"][button] > 1:
                    self.inputdata["mouse_buttons"][button] += 1
                else:
                    self.inputdata["mouse_buttons"][button] = 2
            else:
                if self.inputdata["mouse_buttons"][button] > 1:
                    self.inputdata["mouse_buttons"][button] = 0
                elif self.inputdata["mouse_buttons"][button] < 1:
                    self.inputdata["mouse_buttons"][button] = 1

        """
        
        KEY VALUES MEANING:

        0: Key has JUST been released
        1: Key is NOT pressed
        2+: Key has been pressed for num-1 ticks

        """

    def update(self):
        self.update_inputs()

        self.display.update(self)