from objects.shields import Shield
from objects.characters import Character
from objects.weapons import Weapon
from objects.magic import Magic
from pathlib import Path
import json
import os
import time
import sys
import random
import numpy as np

# Cls
def clear_screen():
    os.system("cls")
    os.system("clear")
    
# Start a new game
def new_game():
    character_creation("Player", "Knight")
    map_creation()

# Characters Creation (Monsters and Player), Works with the Character class in objects/characters.py
def character_creation(name, class_name="default", level=1, health=100, health_max=100, mana=0, mana_max=0, xp=0, xp_max=100, strength=15, critical=5, armor=1, turn=1, health_potion=0, mana_potion=0, gp=random.randint(1, 20)):
    if name == "Player":
        global player1
        gp = 100
        player1 = Character("Player", "Knight", level, health, health_max, 40, 40, xp_max, xp, strength, critical, armor, turn, 2, 1, gp)
        player1.weapon = Weapon("ShortSword", 15, 30)
        player1.magic = np.random.choice([Magic("HolyBolt", 35, 1, 20), Magic("Fireball", 25, 1, 15), Magic("Icebolt", 30, 1, 20)])
    elif name == "Monster":
        global monster1
        if class_name == "default":
            class_name = np.random.choice(["Wolf", "Zombie", "Skeleton"])
        if player1.get_level() >= 3:
            level_generator = player1.get_level() + np.random.randint(-2, 3)
        elif player1.get_level() == 2:
            level_generator = player1.get_level() + np.random.randint(-1, 3)
        elif player1.get_level() == 1:
            level_generator = player1.get_level() + np.random.randint(0, 3)
        monster1 = Character("Monster", class_name, level, health, health_max, mana, mana_max, xp_max, xp, strength, critical, armor, turn, health_potion, mana_potion, gp)
        for i in range(0, level_generator-1):
            Character.level_up(monster1)
            monster1.set_gp(monster1.get_gp() + random.randint(1, 20))
    elif name == "Vendor":
        global vendor1
        vendor1 = Character("Vendor", "Vendor", 50, health, health_max, mana, mana_max, xp_max, xp, 20, critical, 20, turn, random.randint(0,2), random.randint(0,2), random.randint(1, 250))
        vendor1.weapon = np.random.choice([Weapon("ShortSword", 15, 30), Weapon("LongSword", 20, 100), Weapon("Axe", 25, 150), Weapon("GreatSword", 30, 300)])
        vendor1.magic = np.random.choice([Magic("HolyBolt", 35, 1, 20), Magic("Fireball", 25, 1, 15), Magic("Icebolt", 30, 1, 20)])
        vendor1.shield = np.random.choice([Shield("WoodenShield", 1, 10, 60), Shield("IronShield", 3, 15, 120), Shield("SteelShield", 5, 20, 240)])
        vendor1.set_gp(1000)
        
# Create a new map (change the map_size variable to change the size of the map)
def map_creation():
    global map_size
    global map
    map_size = 40
    map = [[np.random.choice([".", "#", "$"], p=[0.9, 0.05, 0.05]) for _ in range(map_size)] for _ in range(map_size // 2)]
    for i in range(len(map)):
        for j in range(len(map[i]) - 1):
            if map[i][j] == "$":
                map[i][j-1] = "!"
                map[i][j+1] = "!"
                map[i-1][j] = "_"
    map[np.random.randint(map_size // 2)][np.random.randint(map_size)] = "@"
    
# Display the game banner when needed
def game_banner():
    print("")
    print("(-~*·~-.,-[ Knight's Quest ]-,.-~*·~-)".center(40))
    print("- I -".center(40))
    return

# Display the main menu
def screen_menu():
    print("")
    print("▬▬ι═══════>".center(40))
    print("")
    print("1. New Game".center(40))
    print("2. Load Game".center(40))
    print("Q. Quit    ".center(40))
    print("")
    print("<═══════ι▬▬".center(40))
    print("")
    while True:
        select = input("?")
        if select == "1":
            new_game()
            break
        if select == "2":
            load_game()
            pass
        if select == "3" or select == "q" or select == "Q":
            sys.exit()

# Display Characters Stats
def character_display(name):
    print("-"*40)
    print(f"{name.get_name()} {name.get_class_name()} Lvl {name.get_level()} Exp {int(name.get_xp())}/{int(name.get_xp_max())} HP {name.get_health()}/{name.get_health_max()}")
    print(f"Strength {name.get_strength()} Critical {name.get_critical()} Armor {name.get_armor()} MP {name.get_mana()}/{name.get_mana_max()}")
    print("-"*40)

# Display VERSUS animation between two characters in a fight
def display_versus(duration, total_length=40):
    j1 = int(calculate_health_percentage(player1))
    j2 = int(calculate_health_percentage(monster1))
    word = f"{j1}% VERSUS {j2}%"
    for i in range(len(word) + 1):
        sys.stdout.write(f"\r{word[:i].center(total_length)}")
        sys.stdout.flush()
        time.sleep(duration / len(word))
    print()

# Display the map stored in the map list variable
def map_display():
    for row in map:
        print(''.join(row))
    return

# Display the map screen with the map and the menu
def map_screen():
    clear_screen()
    game_banner()
    map_display()
    map_menu()
    
# Display the menu for the map screen
def map_menu():
    print("\n1.Move 2.Fight 3.Inventory 4.Save Q.Quit")
    while True:
        select = input("? Votre choix : ") 
        if select == "1":
            print("Not Implemented Yet !")
        if select == "2":
            fight_screen()
        if select == "3":
            player_inventory()
        if select == "4":
            save_game()
        if select == "5" or select == "q" or select == "Q":
            sys.exit()
            
# Create a new monster and start a fight screen
def fight_screen():
    character_creation("Monster", turn=0)
    i = 0
    while monster1.get_health() > 0 and player1.get_health() > 0:
        clear_screen()
        game_banner()
        character_display(player1)
        if i == 0:
            display_versus(1)
            i += 1
        else:
            display_versus(0)
        character_display(monster1)
        fight_menu()
        
# Display the action menu for the fight screen
def fight_menu():
    if (player1.has_magic() is not None) and (player1.get_mana() >= player1.magic.get_mana_cost() and (player1.get_health_potion() > 0 or player1.get_mana_potion() > 0)):
        print(f"\n1.Attack 2.{player1.magic.get_name()}({player1.magic.get_level()}) 3.Potions Q.Run")
    elif (player1.has_magic() is not None) and (player1.get_mana() >= player1.magic.get_mana_cost() and (player1.get_health_potion() <= 0 or player1.get_mana_potion() <= 0)):
        print(f"\n1.Attack 2.{player1.magic.get_name()}({player1.magic.get_level()}) 3.##### Q.Run")
    elif (player1.get_health_potion() > 0 or player1.get_mana_potion() > 0):
        print(f"\n1.Attack 2.##### 3.Potion Q.Run")
    else:
        print(f"\n1.Attack 2.##### 3.##### Q.Run")
    while True:
        select = input("? Votre choix : ") 
        if select == "1":
            turn_test(magic=False)
            break
        if select == "2" and player1.get_mana() >= player1.magic.get_mana_cost():
            turn_test(magic=True)
            break
        if select == "3":
            if player1.get_health_potion() > 0 and player1.get_mana_potion() > 0:
                print(f"1.HealthPotion 2.ManaPotion Q.Back")
            elif player1.get_health_potion() > 0 and player1.get_mana_potion() <= 0:
                print(f"1.HealthPotion 2.##### Q.Back")
            elif player1.get_health_potion() <= 0 and player1.get_mana_potion() > 0:
                print(f"1.##### 2.ManaPotion Q.Back")
            else:
                print("1.##### 2.##### Q.Back")
            while True:
                select = input("? Votre choix : ")
                if select == "1":
                    player1.use_potion("Health Potion")
                    break
                if select == "2":
                    player1.use_potion("Mana Potion")
                    break
                if select == "3":
                    fight_screen()
                    break
                else:
                    pass
            break
        if select == "4" or select == "q" or select == "Q":
            map_screen()
            break
        if select == "5":
            print(f"test")
        else:
            pass

def turn_test(magic):
    if player1.get_turn() >= monster1.get_turn():
        if magic is False:
            player1.attack(monster1)
            time.sleep(0.5)
            is_monster_alive()
            monster1.attack(player1)
            time.sleep(3)
            is_player_alive()
        if magic is True:
            player1.magic_attack(monster1)
            time.sleep(0.5)
            is_monster_alive()
            monster1.attack(player1)
            time.sleep(3)
            is_player_alive()
    if player1.get_turn() < monster1.get_turn():
        print(f"{monster1.get_name()} got initiative !")
        monster1.attack(player1)
        time.sleep(0.5)
        is_player_alive()
        player1.attack(monster1)
        time.sleep(3)
        is_monster_alive()

def is_monster_alive():
    if monster1.get_health() <= 0:
        print(f"{monster1.get_name()} is dead !")
        Character.gain_xp(player1, monster1.get_xp_max() / 4)
        Character.set_turn(player1, 1)
        monster1.gold_drop(player1)
        character_creation("Vendor")
        time.sleep(5)
        map_screen()
        
def is_player_alive():
    if player1.get_health() <= 0:
        print(f"{player1.get_name()} is dead !")
        time.sleep(5)
        sys.exit()

# player_inventory()
def player_inventory():
    clear_screen()
    game_banner()
    print("".center(40))
    print(f"|{player1.get_class_name()} Lvl {player1.get_level()}|".center(40))
    print("".center(40))
    experience_bar = f"Exp:[{'#' * (int(player1.get_xp() * 20) // int(player1.get_xp_max())):<20}]"
    print(f"{experience_bar}".center(40))
    health_bar = f"Health:[{'#' * (player1.get_health() * 10 // player1.get_health_max()):<10}]"
    mana_bar = f"Mana:[{'#' * (player1.get_mana() * 10 // player1.get_mana_max()):<10}]"
    print(f"{health_bar} {mana_bar}".center(40))
    print("".center(40))
    print(f"Strength: {player1.get_strength()}".center(40))
    print(f"Critical %: {player1.get_critical()}".center(40))
    print(f"Armor: {player1.get_armor()}".center(40))
    print("".center(40))
    try: print(f"Magic: {player1.magic.get_name()} Lvl {player1.magic.get_level()}".center(40))
    except: print("Magic: #####".center(40))
    print("".center(40))
    try: print(f"Weapon: {player1.weapon.get_name()} Dmg+{player1.weapon.get_damage()}".center(40))
    except: print("Weapon: #####".center(40))
    try: print(f"Shield: {player1.shield.get_name()} Arm+{player1.shield.get_armor()} %Blc+{player1.shield.get_block()}".center(40))
    except: print("Shield: #####".center(40))
    if player1.get_health_potion() > 1:
        print(f"HealthPotions: {player1.get_health_potion()}".center(40))
    else:
        print(f"HealthPotion: {player1.get_health_potion()}".center(40))
    if player1.get_mana_potion() > 1:
        print(f"ManaPotions: {player1.get_mana_potion()}".center(40))
    else:
        print(f"ManaPotion: {player1.get_mana_potion()}".center(40))
    print(f"Gold: {int(player1.get_gp())}".center(40))
    print("".center(40))
    inventory_menu()
    map_screen()
    
def inventory_menu():
    if player1.get_health_potion() > 0 and player1.get_mana_potion() > 0:
        print("1.HealthPotion 2.ManaPotion 3.BuyThings Q.Back")
    elif player1.get_health_potion() > 0 and player1.get_mana_potion() <= 0:
        print("1.HealthPotion 2.##### 3.BuyThings Q.Back")
    elif player1.get_health_potion() <= 0 and player1.get_mana_potion() > 0:
        print("1.##### 2.ManaPotion 3.BuyThings Q.Back")
    else:
        print("1.##### 2.##### 3.BuyThings Q.Back")
    while True:
        select = input("? Votre choix : ")
        if select == "1":
            player1.use_potion("Health Potion")
            player_inventory()
        if select == "2":
            player1.use_potion("Mana Potion")
            player_inventory()
        if select == "3":
            vendor_inventory()
        if select == "4" or select == "q" or select == "Q":
            map_screen()
            break
        else:
            pass
    pass

def vendor_inventory():
    if 'vendor1' in globals():
        vendor1.get_name()
        clear_screen()
        game_banner()
        print("".center(40))
        print(f"|{vendor1.get_class_name()} Lvl {vendor1.get_level()}|".center(40))
        print(("-"*40).center(40))
        print("BUY THINGS".center(40))
        try: print(f"1. Weapon: {vendor1.weapon.get_name()} Dmg+{vendor1.weapon.get_damage()} {vendor1.weapon.get_price()}gp".center(40))
        except: print("".center(40))
        try: print(f"2. Shield: {vendor1.shield.get_name()} Arm+{vendor1.shield.get_armor()} %Blc+{vendor1.shield.get_block()} {vendor1.shield.get_price()}gp".center(40))
        except: print("".center(40))
        try: print(f"3. HealthPotion: {vendor1.get_health_potion()} 20gp".center(40))
        except: print("".center(40))
        try: print(f"4. ManaPotion: {vendor1.get_mana_potion()} 20gp".center(40))
        except: print("".center(40))
        print(("-"*20).center(40))
        print("SELL THINGS".center(40))
        try: print(f"5. Weapon: {player1.weapon.get_name()} Dmg+{player1.weapon.get_damage()} {int(player1.weapon.sell_price())}gp".center(40))
        except: print("".center(40))
        try: print(f"6. Shield: {player1.shield.get_name()} Arm+{player1.shield.get_armor()} %Blc+{player1.shield.get_block()} {int(player1.shield.sell_price())}gp".center(40))
        except: print("".center(40))
        try: print(f"7. HealthPotion: {player1.get_health_potion()} 10gp".center(40))
        except: print("".center(40))
        try: print(f"8. ManaPotion: {player1.get_mana_potion()} 10gp".center(40))
        except: print("".center(40))
        print(("-"*20).center(40))
        print("Q. Back".center(40))
        print("".center(40))
        print(f"$ Gold: {int(player1.get_gp())} $".center(40))
        print(("-"*40).center(40))
        print("Hey ! Do you want to buy something ?".center(40))
        while True:
            select = input("? Votre choix : ")
            if select == "1":
                if player1.get_gp() >= vendor1.weapon.get_price():
                    player1.set_gp(player1.get_gp() - vendor1.weapon.get_price())
                    player1.weapon = vendor1.weapon
                    print(f"You bought {vendor1.weapon.get_name()} !")
                    vendor1.weapon = None
                    time.sleep(2)
                    vendor_inventory()
                else:
                    print("You don't have enough gold !")
                    time.sleep(2)
                    vendor_inventory()
            if select == "2":
                if player1.get_gp() >= vendor1.shield.get_price():
                    player1.set_gp(player1.get_gp() - vendor1.shield.get_price())
                    player1.shield = vendor1.shield
                    print(f"You bought {vendor1.shield.get_name()} !")
                    vendor1.shield = None

                    time.sleep(2)
                    vendor_inventory()
                else:
                    print("You don't have enough gold !")
                    time.sleep(2)
                    vendor_inventory()
            if select == "3":
                if player1.get_gp() >= 20 and vendor1.get_health_potion() > 0:
                    player1.set_gp(player1.get_gp() - 20)
                    player1.set_health_potion(player1.get_health_potion() + 1)
                    vendor1.set_health_potion(vendor1.get_health_potion() - 1)
                    print(f"You bought a HealthPotion !")
                    time.sleep(2)
                    vendor_inventory()
                elif vendor1.get_health_potion() <= 0:
                    print("The vendor has no more HealthPotion !")
                    time.sleep(2)
                    vendor_inventory()
                else:
                    print("You don't have enough gold !")
                    time.sleep(2)
                    vendor_inventory()
            if select == "4":
                if player1.get_gp() >= 20 and vendor1.get_mana_potion() > 0:
                    player1.set_gp(player1.get_gp() - 20)
                    player1.set_mana_potion(player1.get_mana_potion() + 1)
                    vendor1.set_mana_potion(vendor1.get_mana_potion() - 1)
                    print(f"You bought a ManaPotion !")
                    time.sleep(2)
                    vendor_inventory()
                elif vendor1.get_mana_potion() <= 0:
                    print("The vendor has no more ManaPotion !")
                    time.sleep(2)
                    vendor_inventory()
                else:
                    print("You don't have enough gold !")
                    time.sleep(2)
                    vendor_inventory()
            if select == "5":
                if player1.weapon is not None:
                    player1.set_gp(player1.get_gp() + player1.weapon.sell_price())
                    player1.weapon = None
                    print(f"You sold your weapon !")
                    time.sleep(2)
                    vendor_inventory()
                else:
                    print("You have nothing to sell !")
                    time.sleep(2)
                    vendor_inventory()
            if select == "6":
                if player1.shield is not None:
                    player1.set_gp(player1.get_gp() + player1.shield.sell_price())
                    player1.shield = None
                    print(f"You sold your shield !")
                    time.sleep(2)
                    vendor_inventory()
                else:
                    print("You have nothing to sell !")
                    time.sleep(2)
                    vendor_inventory()
            if select == "7":
                if player1.get_health_potion() > 0:
                    player1.set_gp(player1.get_gp() + 10)
                    player1.set_health_potion(player1.get_health_potion() - 1)
                    print(f"You sold a HealthPotion !")
                    time.sleep(2)
                    vendor_inventory()
                else:
                    print("You have nothing to sell !")
                    time.sleep(2)
                    vendor_inventory()
            if select == "8":
                if player1.get_mana_potion() > 0:
                    player1.set_gp(player1.get_gp() + 10)
                    player1.set_mana_potion(player1.get_mana_potion() - 1)
                    print(f"You sold a ManaPotion !")
                    time.sleep(2)
                    vendor_inventory()
                else:
                    print("You have nothing to sell !")
                    time.sleep(2)
                    vendor_inventory()
            if select == "9" or select == "q" or select == "Q":
                player_inventory()
                break
            
    else: print("The vendor is not here ! Come back later !")
    time.sleep(5)
    
def calculate_health_percentage(player):
    return (player.get_health() / player.get_health_max()) * 100

def save_game():
    save_dir = Path("save")
    save_dir.mkdir(exist_ok=True)
    save_file = save_dir / "save.json"
    if save_file.exists():
        while True:
            select = input("A save already exists. Overwrite? (o/n) ")
            if select == "o" or select == "O" or select == "1":
                break
            if select == "n" or select == "N" or select == "2":
                return
            else:
                pass
    try: wp_data = f"{player1.weapon.get_name()}, {player1.weapon.get_damage()}, {player1.weapon.get_price()}"
    except: wp_data = "None"
    try: mg_data = f"{player1.magic.get_name()}, {player1.magic.get_damage()}, {player1.magic.get_mana_cost()}, {player1.magic.get_level()}"
    except: mg_data = "None"
    try: sh_data = f"{player1.shield.get_name()}, {player1.shield.get_armor()}, {player1.shield.get_block()}, {player1.shield.get_price()}"
    except: sh_data = "None"
    data = {
        "name": player1.get_name(),
        "class_name": player1.get_class_name(),
        "level": player1.get_level(),
        "health": player1.get_health(),
        "health_max": player1.get_health_max(),
        "mana": player1.get_mana(),
        "mana_max": player1.get_mana_max(),
        "xp": player1.get_xp(),
        "xp_max": player1.get_xp_max(),
        "strength": player1.get_strength(),
        "critical": player1.get_critical(),
        "armor": player1.get_armor(),
        "turn": player1.get_turn(),
        "health_potion": player1.get_health_potion(),
        "mana_potion": player1.get_mana_potion(),
        "gp": player1.get_gp(),
        "weapon": wp_data,
        "magic": mg_data,
        "shield": sh_data,
    }
    with save_file.open("w") as f:
        json.dump(data, f, indent=4)
    print("Game saved ! Game/Save.json")
    return

def load_game():
    print("Not Implemented Yet !")
    pass


# loading system
# move()
# Update magic possibilities
# Monster can drop very rare loots
# add boss monster each 5 levels

# Main Loop
while True:
    clear_screen()
    game_banner()
    screen_menu()
    map_screen()