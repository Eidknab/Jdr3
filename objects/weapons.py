class Weapon:
    
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage
        
    def get_name(self):
        return self.name
    
    def get_damage(self):
        return self.damage
    
    def set_damage(self, damage):
        self.damage = damage
        
    def set_name(self, name):
        self.name = name
        
    