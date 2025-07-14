from tools import calculate_angle, fprint


class Hitbox:

    def __init__(self, entity, width, height, rel_x, rel_y):
        self.width = width
        self.height = height
        self.rel_x = rel_x
        self.rel_y = rel_y
        self.x = entity.x + rel_x
        self.y = entity.y + rel_y

        self.left = self.x - self.width / 2
        self.top = self.y - self.height / 2
        self.right = self.x + self.width / 2
        self.bottom = self.y + self.height / 2

    def update_transform(self):
        self.left = self.x - self.width / 2
        self.top = self.y - self.height / 2
        self.right = self.x + self.width / 2
        self.bottom = self.y + self.height / 2


class PlayerEntity:

    def __init__(self, id):
        self.id = id

        # Images need to be in order of z-index, so the first image is drawn first
        self.images = ["trolleywheels0", "humanlegs0", "trolleybody0", "humanbody0"]

        # Sprite transform
        # width height MUST match ALL images
        self.sprite_width = 360
        self.sprite_height = 540
        self.x = 0
        self.y = 0

        self.sprite_left = self.x - self.sprite_width / 2
        self.sprite_top = self.y - self.sprite_height / 2
        self.sprite_right = self.x + self.sprite_width / 2
        self.sprite_bottom = self.y + self.sprite_height / 2

        # Hitboxes

        self.hitbox_human = Hitbox(self, 180, 100, 0, 190)

        self.hitbox_trolley = Hitbox(self, 180, 260, 0, 10)
        
        # Angles
        self.angle = 0
        self.angle_inverted = 0 - self.angle

        self.movespeed = 9
        self.turnspeed = 1.5
    
    def update_transform(self):
        self.sprite_left = self.x - self.sprite_width / 2
        self.sprite_top = self.y - self.sprite_height / 2
        self.sprite_right = self.x + self.sprite_width / 2
        self.sprite_bottom = self.y + self.sprite_height / 2

        self.angle_inverted = 0 - self.angle

    def update(self, keys, mouse_buttons, mouse_pos):
        if keys["w"] > 1:
            self.y -= self.movespeed
        if keys["a"] > 1:
            self.x -= self.movespeed
        if keys["s"] > 1:
            self.y += self.movespeed
        if keys["d"] > 1:
            self.x += self.movespeed

        target_angle = calculate_angle(self.x, self.y, mouse_pos["x"], mouse_pos["y"])
        self.angle = target_angle

        self.update_transform()

