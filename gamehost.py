class Game:

    def __init__(self):
        self.entities = []
    
    def update_entity(self, id, keys, mouse_buttons, mouse_pos):
        for entity in self.entities:
            if entity.id == id:
                entity.update(keys, mouse_buttons, mouse_pos)

    def entity_exists(self, id):
        for entity in self.entities:
            if entity.id == id:
                return True
        
        return False
    
    def add_entity(self, id):
        pass