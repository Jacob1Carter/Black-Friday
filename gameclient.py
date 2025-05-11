from display import Display
from tools import fprint
import pygame


class Sprite:

    def __init__(self, id, image="none", width=1, height=1, angle=0, x=0, y=0):
        self.id = id
        self.image_name = "trolleysprite1"
        self.angle = 0
        self.width = 360
        self.height = 360
        self.x = 0
        self.y = 0

        self.angle_inverted = 0 - self.angle

        self.image_base = pygame.transform.scale(
                pygame.image.load(f"assets/{self.image_name}.png").convert_alpha(),
                (self.width, self.height)
            )
        
        self.image = pygame.transform.rotate(
            self.image_base,
            self.angle_inverted
        )

        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def update_transform(self):
        self.left = self.x - self.width / 2
        self.top = self.y - self.height / 2
        self.right = self.x + self.width / 2
        self.bottom = self.y + self.height / 2

        self.angle_inverted = 0 - self.angle

        self.image = pygame.transform.rotate(
            self.image_base,
            self.angle_inverted
        )

        self.rect = self.image.get_rect(center=(self.x, self.y))


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

        self.sprites = []

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
    
    def sprite_exists(self, id):
        for sprite in self.sprites:
            if sprite.id == id:
                return True
        return False
    
    def update_sprite(self, ip_address, image=None, width=None, height=None, angle=None, x=None, y=None):
        for sprite in self.sprites:
            if sprite.id == ip_address:
                reload_image = False
                if image is not None:
                    if sprite.image_name != image:
                        sprite.image_name = image
                        reload_image = True
                if width is not None:
                    if sprite.width != width:
                        sprite.width = width
                        reload_image = True
                if height is not None:
                    if sprite.height != height:
                        sprite.height = height
                        reload_image = True
                if angle is not None:
                    if sprite.angle != angle:
                        sprite.angle = angle
                        reload_image = True
                if x is not None:
                    sprite.x = x
                if y is not None:
                    sprite.y = y
                
                if reload_image:
                    sprite.image = pygame.transform.rotate(
                        pygame.transform.scale(
                            pygame.image.load(f"assets/{sprite.image_name}.png").convert_alpha(),
                            (sprite.width, sprite.height)
                        ),
                        sprite.angle_inverted
                    )
        
                sprite.update_transform()

    def add_sprite(self, ip_address, image="none", width=1, height=1, angle=0, x=0, y=0):
        if not self.sprite_exists(id):
            self.sprites.append(Sprite(
                id=ip_address,
                image=image,
                width=width,
                height=height,
                angle=angle,
                x=x,
                y=y
            ))