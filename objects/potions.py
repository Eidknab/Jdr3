class Potion:
    def __init__(self, name, heal_amount, mana_amount, quantity):
        self.name = name
        self.heal_amount = heal_amount
        self.mana_amount = mana_amount
        self.quantity = quantity
        
    def get_name(self):
        return self.name
    
    def get_heal_amount(self):
        return self.heal_amount
    
    def get_mana_amount(self):
        return self.mana_amount
    
    def get_quantity(self):
        return self.quantity
    
    def set_name(self, name):
        self.name = name
        
    def set_heal_amount(self, heal_amount):
        self.heal_amount = heal_amount
    
    def set_mana_amount(self, mana_amount):
        self.mana_amount = mana_amount
        
    def set_quantity(self, quantity):
        self.quantity = quantity
        
        