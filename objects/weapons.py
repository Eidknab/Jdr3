class Weapon:
    
    def __init__(self, name, damage, price):
        self.name = name
        self.damage = damage
        self.price = price
        
    def __str__(self):
        return f"{self.name}, {self.damage}, {self.price}"
        
    def get_name(self):
        return self.name
    
    def get_damage(self):
        return self.damage
    
    def get_price(self):
        return self.price
    
    def set_name(self, name):
        self.name = name
        
    def set_damage(self, damage):
        self.damage = damage
        
    def set_price(self, price):
        self.price = price
        
    def sell_price(self):
        return self.price / 3
        
    