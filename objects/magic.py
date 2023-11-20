class Magic:
    def __init__(self, name, damage, level, mana_cost):
        self.name = name
        self.damage = damage
        self.level = level
        self.mana_cost = mana_cost
        
    def get_name(self):
        return self.name
    
    def get_damage(self):
        return self.damage
    
    def get_level(self):
        return self.level 
    
    def get_mana_cost(self):
        return self.mana_cost
    
    def set_name(self, name):
        self.name = name
    
    def set_damage(self, damage):
        self.damage = damage
        
    def set_level(self, level):
        self.level = level
        
    def set_mana_cost(self, mana_cost):
        self.mana_cost = mana_cost