from tools import calculate_angle, fprint


class PlayerEntity:

    def __init__(self, id):
        self.id = id

        self.image = "trolleysprite2"
        self.width = 360
        self.height = 360
        self.angle = 0
        self.x = 0
        self.y = 0

        self.left = self.x - self.width / 2
        self.top = self.y - self.height / 2
        self.right = self.x + self.width / 2
        self.bottom = self.y + self.height / 2

        self.angle_inverted = 0 - self.angle

        self.movespeed = 3
        self.turnspeed = 1.5
    
    def update_transform(self):
        self.left = self.x - self.width / 2
        self.top = self.y - self.height / 2
        self.right = self.x + self.width / 2
        self.bottom = self.y + self.height / 2

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

