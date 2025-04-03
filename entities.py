class PlayerEntity:

    def __init__(self, id):
        self.id = id

        self.image = "trolleysprite0"
        self.width = 180
        self.height = 360
        self.angle = 0
        self.x = 0
        self.y = 0


        self.speed = 3
    
    def update(self, keys, mouse_buttons, mouse_pos):
        if keys["w"] > 1:
            self.y -= self.speed
        if keys["a"] > 1:
            self.x -= self.speed
        if keys["s"] > 1:
            self.y += self.speed
        if keys["d"] > 1:
            self.x += self.speed
        
