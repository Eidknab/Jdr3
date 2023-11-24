class Shield:
    def __init__(self, name, armor, block, price):
        self.name = name
        self.armor = armor
        self.block = block
        self.price = price
    
    def __str__(self):
        return f"{self.name}, {self.armor}, {self.block}, {self.price}"
        
    def get_name(self):
        return self.name
    
    def get_armor(self):
        return self.armor
    
    def get_block(self):
        return self.block
    
    def get_price(self):
        return self.price
    
    def set_name(self, name):
        self.name = name
    
    def set_armor(self, armor):
        self.armor = armor  
        
    def set_block(self, block):
        self.block = block
        
    def set_price(self, price):
        self.price = price
        
    def sell_price(self):
        return self.price / 3