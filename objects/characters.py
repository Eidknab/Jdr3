import random
import time

class Character: 
    def __init__(self, name, class_name, level, health_max, health, mana_max, mana, xp_max, xp, strength, critical, armor, turn, health_potion, mana_potion, gp):
        
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
        self.health_potion = health_potion
        self.mana_potion = mana_potion
        self.gp = gp
        self.shield = None
        self.weapon = None
        self.magic = None
        
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
    
    def get_health_potion(self):
        return self.health_potion
    
    def get_mana_potion(self):
        return self.mana_potion
    
    def get_gp(self):
        return self.gp
    
    def get_shield(self):
        return self.shield
    
    def get_weapon(self):
        return self.weapon
    
    def get_magic(self):
        return self.magic
    
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
        
    def set_health_potion(self, health_potion):
        self.health_potion = health_potion
        
    def set_mana_potion(self, mana_potion):
        self.mana_potion = mana_potion
        
    def set_gp(self, gp):
        self.gp = gp
        
    def set_shield(self, shield):
        self.shield = shield
        
    def set_weapon(self, weapon):
        self.weapon = weapon
        
    def set_magic(self, magic):
        self.magic = magic
        
    # Methods
    # Physical Attack applied to the target
    def attack(self, target):
        # Min and Max Damage
        damage = random.randint(self.strength-5, self.strength+5)
        # Armor Reduction
        damage -= target.armor
        if target.has_shield():
            # Block Chance
            if random.randint(0, 100) <= target.shield.get_block():
                damage = 0
                print(f"{target.name} has blocked the attack !")
                return
            # Armor Reduction from Shield
            damage -= target.shield.get_armor()
        # Level Difference
        damage += (self.level - target.level)
        # Critical Hit Chance - level difference is added to the critical chance
        if random.randint(0, 100) <= (self.critical + (self.level-target.level)*5):
            damage *= 1.5
            print("Critical Hit !")
        # Add Weapon Damage
        if self.has_weapon():
            damage += self.weapon.get_damage()
        # Inflict Damage
        target.damage(int(damage))
    
    # Magic Attack applied to the target
    def magic_attack(self, target):
        print(f"{self.name} casts {self.magic.get_name()} (Level {self.magic.get_level()})!")
        # Test if the target is undead
        if (self.magic.get_name() == "HolyBolt") and (target.get_class_name() == "Wolf"):
            print((f"{self.get_name()} did no effect to {target.get_name()} !"))
            return
        # Min and Max Damage
        damage = random.randint(self.magic.get_damage()-5, self.magic.get_damage()+5)
        # Damage Multiplier Based on Level
        damage = damage * (1.1 ** (self.level - 1))
        # Apply Damage 
        target.damage(int(damage))
        # Consume Mana of the Caster
        self.mana -= self.magic.get_mana_cost() 
        print(f"You consumed {self.magic.get_mana_cost()} mana !")
        
    def damage(self, amount):
        self.health -= amount
        print(f"{self.name} has taken {amount} damage !")
    
    def heal(self, amount):
        self.health += amount
        print(f"{self.name} has healed {amount} health !")
    
    # Gain XP and Level Up if XP Max is reached
    def gain_xp(self, amount):
        self.xp += int(amount)
        if self.xp >= self.xp_max and self.level < 50:
            self.level_up()
        else:
            print(f"{self.name} has gained {int(amount)} xp !")
        if self.level == 50 and self.xp >= self.xp_max:
            self.xp = self.xp_max
    
    # Level Up and upgrade stats
    def level_up(self):
        self.level += 1
        self.xp = 0
        self.xp_max *= 1.5
        self.health_max += 20
        self.health = self.health_max
        self.mana_max += 10
        self.mana = self.mana_max
        self.strength += 3
        if self.level == 5 or self.level == 10 or self.level == 15 or self.level == 20 or self.level == 25 or self.level == 30 or self.level == 35 or self.level == 40 or self.level == 45 or self.level == 50:
            self.critical += 1
            self.armor += 1
        if self.name == "Player":
            print(f"Ding! {self.name} is now level {self.level} !")
    
    # test if the character has a weapon, a shield or a magic
    def has_weapon(self):
        return self.weapon is not None
    def has_shield(self):
        return self.shield is not None
    def has_magic(self):
        return self.magic is not None
    
    # Use potion parameter is the potion name
    def use_potion(self, potion):
        if potion == "Health Potion" and self.health_potion > 0:
            self.health += 50
            if self.health > self.health_max:
                self.health = self.health_max
            self.health_potion -= 1
        elif potion == "Mana Potion" and self.mana_potion > 0:
            self.mana += 40
            if self.mana > self.mana_max:
                self.mana = self.mana_max
            self.mana_potion -= 1
        else:
            print("You don't have any potion left !")
            time.sleep(1)
            
    # give gold to the target
    def gold_drop(self, target):
        target.gp += self.get_gp()
        print(f"{self.name} has droped {self.get_gp()} gold !")