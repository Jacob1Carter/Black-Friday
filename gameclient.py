from display import Display
from tools import fprint
import pygame
import math


class Hitbox:

    def __init__(self, entity, width, height, rel_x, rel_y):
        self.entity = entity
        self.width = width
        self.height = height
        self.rel_x = rel_x
        self.rel_y = rel_y
        self.x = self.entity.x + rel_x
        self.y = self.entity.y + rel_y
        self.angle = self.entity.angle  # Store the angle

        self.update_transform()

    def update_transform(self):
        # Rotate rel_x, rel_y by entity.angle
        angle_rad = math.radians(self.entity.angle)
        rotated_x = self.rel_x * math.cos(angle_rad) - self.rel_y * math.sin(angle_rad)
        rotated_y = self.rel_x * math.sin(angle_rad) + self.rel_y * math.cos(angle_rad)
        self.x = self.entity.x + rotated_x
        self.y = self.entity.y + rotated_y

        self.angle = self.entity.angle  # Update hitbox angle

        # Calculate the four corners of the hitbox after rotation
        hw, hh = self.width / 2, self.height / 2
        corners = [
            (-hw, -hh),
            ( hw, -hh),
            ( hw,  hh),
            (-hw,  hh)
        ]
        angle_rad = math.radians(self.angle)
        self.corners = []
        for cx, cy in corners:
            rx = cx * math.cos(angle_rad) - cy * math.sin(angle_rad)
            ry = cx * math.sin(angle_rad) + cy * math.cos(angle_rad)
            self.corners.append((self.x + rx, self.y + ry))

        # Optionally, update the bounding rect (axis-aligned)
        xs, ys = zip(*self.corners)
        self.left = min(xs)
        self.right = max(xs)
        self.top = min(ys)
        self.bottom = max(ys)
        self.rect = (self.left, self.top, self.right - self.left, self.bottom - self.top)


class Sprite:

    def __init__(self, id, images=[], width=1, height=1, angle=0, x=0, y=0):
        self.id = id
        self.images = images
        self.angle = angle
        self.width = width
        self.height = height
        self.x = x
        self.y = y

        self.angle_inverted = 0 - self.angle

        self.reload_images()

        # Hitboxes

        self.hitbox_human = Hitbox(self, 180, 100, 0, 190)

        self.hitbox_trolley = Hitbox(self, 180, 260, 0, 10)

        fprint(self.hitbox_human.rect)

    def reload_images(self):
        self.loaded_images = []
        for image_name in self.images:
            self.loaded_images.append(pygame.image.load(f"assets/{image_name}.png").convert_alpha())
        
        self.reformat_images()
    
    def reformat_images(self):
        self.complete_images = []
        for image in self.loaded_images:
            self.complete_images.append(
                pygame.transform.rotate(
                    pygame.transform.scale(image, (self.width, self.height)),
                    self.angle_inverted
                )
            )
        
        if len(self.complete_images) > 0:
            self.rect = self.complete_images[0].get_rect(center=(self.x, self.y))
        else:
            self.rect = pygame.Rect(0, 0, self.width, self.height)

    
    def update_transform(self):
        self.left = self.x - self.width / 2
        self.top = self.y - self.height / 2
        self.right = self.x + self.width / 2
        self.bottom = self.y + self.height / 2

        self.angle_inverted = 0 - self.angle

        self.reformat_images()

        self.hitbox_human.update_transform()
        self.hitbox_trolley.update_transform()


class Game:

    class DebugDot:

        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.rect = pygame.Rect(x, y, 10, 10)
            self.color = (255, 0, 0)

        def update(self):
            pass

    def __init__(self):
        self.pygame = pygame

        self.name = "Black Friday"
        self.display = Display(self)

        self.debug_dots = []
        for i in range(self.display.WIDTH // 30):
            for j in range(self.display.HEIGHT // 30):
                self.debug_dots.append(pygame.Rect(i * 30, j * 30, 10, 10))

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

        for debug_dot in self.debug_dots:
            pass
            #debug_dot.update()

        self.display.update(self)
    
    def sprite_exists(self, id):
        for sprite in self.sprites:
            if sprite.id == id:
                return True
        return False
    
    def update_sprite(self, ip_address, images=None, width=None, height=None, angle=None, x=None, y=None):
        for sprite in self.sprites:
            if sprite.id == ip_address:
                reload_images = False
                if images is not None:
                    if sprite.images != images:
                        sprite.images = images
                        reload_images = True
                if width is not None:
                    if sprite.width != width:
                        sprite.width = width
                if height is not None:
                    if sprite.height != height:
                        sprite.height = height
                if angle is not None:
                    if sprite.angle != angle:
                        sprite.angle = angle
                if x is not None:
                    sprite.x = x
                if y is not None:
                    sprite.y = y

                sprite.update_transform()

                if reload_images or not sprite.loaded_images:
                    fprint(f"Reloading images for sprite {sprite.id} with images {sprite.images}")
                    sprite.reload_images()
                else:
                    sprite.reformat_images()

    def add_sprite(self, ip_address, images=[], width=1, height=1, angle=0, x=0, y=0):
        if not self.sprite_exists(id):
            self.sprites.append(Sprite(
                id=ip_address,
                images=images,
                width=width,
                height=height,
                angle=angle,
                x=x,
                y=y
            ))