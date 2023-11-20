import random

class Character: 
    def __init__(self, name, class_name, level, health_max, health, mana_max, mana, xp_max, xp, strength, critical, armor, turn):
        
        # Attributs
        self.name = name
        self.class_name = class_name
        self.level = level
        self.health_max = health_max
        self.health = health
        self.mana_max = mana_max
        self.mana = mana
        self.xp_max = xp_max
        self.xp = xp
        self.strength = strength
        self.critical = critical
        self.armor = armor
        self.turn = turn
        self.weapon = None
        
    # Getters
    def get_name(self):
        return self.name
    
    def get_class_name(self):
        return self.class_name
    
    def get_level(self):
        return self.level
    
    def get_health_max(self):
        return self.health_max
    
    def get_health(self):
        return self.health
    
    def get_mana_max(self):
        return self.mana_max
    
    def get_mana(self):
        return self.mana
    
    def get_xp_max(self):
        return self.xp_max
    
    def get_xp(self):
        return self.xp
    
    def get_strength(self):
        return self.strength
    
    def get_critical(self):
        return self.critical
    
    def get_armor(self):
        return self.armor
    
    def get_turn(self):
        return self.turn
    
    # Setters
    def set_name(self, name):
        self.type = name
        
    def set_class_name(self, class_name):
        self.name = class_name
        
    def set_level(self, level):
        self.level = level
        
    def set_health_max(self, health_max):
        self.health_max = health_max
    
    def set_health(self, health):
        self.health = health
        
    def set_mana_max(self, mana_max):
        self.mana_max = mana_max
        
    def set_mana(self, mana):
        self.mana = mana
        
    def set_xp_max(self, xp_max):
        self.xp_max = xp_max
        
    def set_xp(self, xp):
        self.xp = xp
        
    def set_strength(self, strength):
        self.strength = strength
        
    def set_critical(self, critical):
        self.critical = critical
        
    def set_armor(self, armor):
        self.armor = armor
    
    def set_turn(self, turn):
        self.turn = turn
        
    def set_weapon(self, weapon):
        self.weapon = weapon
        
    # Methods
    def attack(self, target):
        damage = random.randint(self.strength-5, self.strength+5)
        if random.randint(0, 100) <= self.critical:
            damage *= 1.5
            print("Critical Hit !")
        if self.has_weapon():
            damage += self.weapon.get_damage()
        target.damage(int(damage))
        
    def damage(self, amount):
        self.health -= amount
        print(f"{self.name} has taken {amount} damage !")
        
    def heal(self, amount):
        self.health += amount
        print(f"{self.name} has healed {amount} health !")
    
    def gain_xp(self, amount):
        self.xp += int(amount)
        if self.xp >= self.xp_max and self.level < 50:
            self.level_up()
        else:
            print(f"{self.name} has gained {int(amount)} xp !")
        if self.level == 50 and self.xp >= self.xp_max:
            self.xp = self.xp_max
    
    def level_up(self):
        self.level += 1
        self.xp = 0
        self.xp_max *= 1.5
        self.health_max += 20
        self.health += self.health_max
        self.mana_max += 10
        self.strength += 1
        if self.level == 5 or self.level == 10 or self.level == 15 or self.level == 20 or self.level == 25 or self.level == 30 or self.level == 35 or self.level == 40 or self.level == 45 or self.level == 50:
            self.critical += 1
            self.armor += 1
        print(f"Ding! {self.name} is now level {self.level} !")
        
    def calc_xp(self):
        for i in range(1, self.level):
            self.xp_max *= 1.5
        return self.xp_max
    
    def has_weapon(self):
        return self.weapon is not None