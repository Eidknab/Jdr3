from objects.shields import Shield
from objects.characters import Character
from objects.weapons import Weapon
from objects.magic import Magic
from pathlib import Path
import curses
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
        player1.magic = np.random.choice([Magic("HolyBolt", 35, 1, 20), Magic("FireBall", 25, 1, 15), Magic("IceBolt", 30, 1, 20)])
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
                map[i][j-1] = "|"
                map[i][j+1] = "|"
                map[i-1][j] = "_"
    map[np.random.randint(map_size // 2)][np.random.randint(map_size)] = "@"
    
def get_position():
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == "@":
                return j, i
    return None, None
    
# Display the game banner when needed
def game_banner(stdscr=None):
    if stdscr is not None:
        pass
    else:
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
def map_display(stdscr=None):
    if stdscr is not None:
        for row in map:
            stdscr.addstr(''.join(row) + "\n")
        return
    else:
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
    print("\n1.Move 2.Inventory 3.Save Q.Quit",end=" ")
    while True:
        select = input("?") 
        if select == "1" or select == "m" or select == "M":
            clear_screen()
            curses.wrapper(move)
        if select == "2" or select == "i" or select == "I":
            player_inventory()
        if select == "3" or select == "s" or select == "S":
            save_game()
        if select == "4" or select == "q" or select == "Q":
            sys.exit()
        else:
            map_screen()
            
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
        print(f"\n1.Attack 2.{player1.magic.get_name()}({player1.magic.get_level()})({player1.magic.get_mana_cost()}) 3.Potions Q.Run")
    elif (player1.has_magic() is not None) and (player1.get_mana() >= player1.magic.get_mana_cost() and (player1.get_health_potion() <= 0 or player1.get_mana_potion() <= 0)):
        print(f"\n1.Attack 2.{player1.magic.get_name()}({player1.magic.get_level()})({player1.magic.get_mana_cost()}) 3.##### Q.Run")
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
                if select == "3" or select == "q" or select == "Q":
                    fight_screen()
                    break
                else:
                    pass
            break
        if select == "4" or select == "q" or select == "Q":
            i = random.randint(1, 3)
            if monster1.get_turn() == 2:
                monster1.attack(player1)
                monster1.set_turn(1)
                print("You failed to run away !")
                time.sleep(2)
            if i == 3:
                print("You ran away !")
                time.sleep(2)
                clear_screen()
                curses.wrapper(move)
            else:
                monster1.set_turn(2)
                print("You failed to run away !")
                time.sleep(2)
            pass
        if select == "5":
            print(f"test")
        else:
            pass

# Test who attack first, some monsters can have initiative
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

# Test if the monster is alive and give xp gp to the player
def is_monster_alive():
    if monster1.get_health() <= 0:
        print(f"{monster1.get_name()} is dead !")
        Character.gain_xp(player1, monster1.get_xp_max() / 4)
        Character.set_turn(player1, 1)
        monster1.gold_drop(player1)
        character_creation("Vendor")
        time.sleep(4)
        curses.wrapper(move)
        
# Test if the player is alive
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
    try: print(f"Armor: {player1.get_armor()} +{player1.shield.get_armor()}".center(40))
    except: print(f"Armor: {player1.get_armor()}".center(40))
    print("".center(40))
    try: print(f"Magic: {player1.magic.get_name()} Lvl {player1.magic.get_level()} Dmg {player1.magic.get_damage()} MCost {player1.magic.get_mana_cost()}".center(40)) 
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

# Save the game in a json file (save/save.json)
def save_game():
    save_dir = Path("save")
    save_dir.mkdir(exist_ok=True)
    save_file = save_dir / "save.json"
    if save_file.exists():
        while True:
            select = input("A save already exists. Overwrite? (y/n) ")
            if select == "y" or select == "Y" or select == "1":
                break
            if select == "n" or select == "N" or select == "2":
                return
            else:
                pass
    try: wp_data = f"{player1.weapon}"
    except: wp_data = "None"
    try: mg_data = f"{player1.magic}"
    except: mg_data = "None"
    try: sh_data = f"{player1.shield}"
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
    print("Game saved ! save/save.json")
    time.sleep(2)
    return

# Load a game from the save file (save/save.json)
def load_game():
    global player1
    with open("save/save.json", "r") as f:
        data = json.load(f)
    print("Loading atrributes...", end="")
    time.sleep(1)
    player1 = Character(data["name"], data["class_name"], data["level"], data["health_max"], data["health"], data["mana_max"], data["mana"], data["xp_max"], data["xp"], data["strength"], data["critical"], data["armor"], data["turn"], data["health_potion"], data["mana_potion"], data["gp"])
    print("Done !")
    
    print("Loading weapon, magic and shield...")
    time.sleep(.5)
    if data["weapon"] == "None":
        player1.weapon = None
        print("No weapon in inventory.")
    else: 
        wp_name = str(data["weapon"].split(",")[0])
        wp_damage = int(data["weapon"].split(",")[1])
        wp_price = int(data["weapon"].split(",")[2])
        player1.weapon = Weapon(wp_name, wp_damage, wp_price)
        print(f"{player1.weapon} loaded !")
    time.sleep(.5)
    if data["magic"] == "None":
        player1.magic = None
        print("No spells.")
    else:
        mg_name = str(data["magic"].split(",")[0])
        mg_damage = int(data["magic"].split(",")[1])
        mg_level = int(data["magic"].split(",")[2])
        mg_mana_cost = int(data["magic"].split(",")[3])
        player1.magic = Magic(mg_name, mg_damage, mg_level, mg_mana_cost)
        print(f"{player1.magic} loaded !")
    time.sleep(.5)
    if data["shield"] == "None":
        player1.shield = None
        print("No shield in inventory.")
    else: 
        sh_name = str(data["shield"].split(",")[0])
        sh_armor = int(data["shield"].split(",")[1])
        sh_block = int(data["shield"].split(",")[2])
        sh_price = int(data["shield"].split(",")[3])
        player1.shield = Shield(sh_name, sh_armor, sh_block, sh_price)
        print(f"{player1.shield} loaded !")
    time.sleep(5)

    map_creation()
    map_screen()
    return

def move(stdscr):
    if 'player_x' not in globals() or 'player_y' not in globals():
        global player_x, player_y
        player_x, player_y = get_position()
    stdscr.addstr("(-~*·~-.,-[ Knight's Quest ]-,.-~*·~-)\n")
    stdscr.addstr("\t\t- I -\n")
    map_display(stdscr)
    stdscr.addstr("@=Player #=Enemy $=Chest |=Walls Q.Back\n")
    stdscr.addstr("Move with the arrow keys.")
    while True:
        player_x, player_y = get_position()
        key = stdscr.getch()
        stdscr.addstr((player_y+2), player_x, " ")
        map[player_y][player_x] = " "
        if key == curses.KEY_UP and player_y > 0 and map[player_y-1][player_x] not in ["|", "_"]:
            player_y -= 1
            test_map(stdscr)
        elif key == curses.KEY_DOWN and (player_y) < (map_size // 2 - 1) and map[player_y+1][player_x] not in ["|", "_"]:
            player_y += 1
            test_map(stdscr)
        elif key == curses.KEY_RIGHT and player_x < (map_size - 1) and map[player_y][player_x+1] not in ["|", "_"]:
            player_x += 1
            test_map(stdscr)
        elif key == curses.KEY_LEFT and player_x > 0 and map[player_y][player_x-1] not in ["|", "_"]:
            player_x -= 1
            test_map(stdscr)
        elif key == ord("q"):
            map[player_y][player_x] = "@" 
            stdscr.clear()
            curses.endwin()
            map_screen()
            break
        stdscr.addstr((player_y+2), player_x, "@")
        map[player_y][player_x] = "@" 
        stdscr.refresh()

def test_map(stdscr):
    if map[player_y][player_x] == "#":
        map[player_y][player_x] = "@" 
        stdscr.clear()
        curses.endwin()
        fight_screen()
        curses.wrapper(move)
    try: 
        if map[player_y+1][player_x] == "#" or map[player_y-1][player_x] == "#" or map[player_y][player_x+1] == "#" or map[player_y][player_x-1] == "#":
            map[player_y][player_x] = "@" 
            stdscr.clear()
            curses.endwin()
            clear_screen()
            print("A monster just saw you !")
            time.sleep(2)
            if map[player_y-1][player_x] == "#":
                map[player_y-1][player_x] = " "
            elif map[player_y+1][player_x] == "#":
                map[player_y+1][player_x] = " "
            elif map[player_y][player_x-1] == "#":
                map[player_y][player_x-1] = " "
            elif map[player_y][player_x+1] == "#":
                map[player_y][player_x+1] = " "
            fight_screen()
    except:
        pass

    if map[player_y][player_x] == "$":
        map[player_y][player_x] = "@" 
        try: map[player_y][player_x-1] = " "
        except: pass
        try: map[player_y][player_x+1] = " "
        except: pass
        try: map[player_y-1][player_x] = " "
        except: pass
        stdscr.clear()
        curses.endwin()
        chest()
        
def chest():
    i = np.random.randint(1, 100)
    if i == 100:
        print("You found a legendary weapon !")
        print("LegendarySword Dmg+50")
        try: print(f"Pick it up and replace {player1.weapon.get_name()}, {player1.weapon.get_damage()} ? (y/n)", end=" ")
        except: print("Pick it up ? (y/n)", end=" ")
        while True:
            select = input("?")
            if select == "y" or select == "Y" or select == "1":
                player1.weapon = Weapon("LegendarySword", 50, 500)
                break
            if select == "n" or select == "N" or select == "2":
                break
            else:
                pass
    if i == 99:
        print("You found a legendary shield !")
        print("LegendaryShield Arm+8 %Blc+35")
        try: print(f"Pick it up and replace {player1.shield.get_name()}, {player1.shield.get_armor()}, {player1.shield.get_block()} ? (y/n)", end=" ")
        except: print("Pick it up ? (y/n)", end=" ")
        while True:
            select = input("?")
            if select == "y" or select == "Y" or select == "1":
                player1.shield = Shield("LegendaryShield", 8, 35, 400)
                break
            if select == "n" or select == "N" or select == "2":
                break
            else:
                pass
    if i <= 98 and i >= 97:
        print("You found a rare weapon !")
        print("RareSword Dmg+30")
        try: print(f"Pick it up and replace {player1.weapon.get_name()}, {player1.weapon.get_damage()} ? (y/n)", end=" ")
        except: print("Pick it up ? (y/n)", end=" ")
        while True:
            select = input("?")
            if select == "y" or select == "Y" or select == "1":
                player1.weapon = Weapon("RareSword", 30, 300)
                break
            if select == "n" or select == "N" or select == "2":
                break
            else:
                pass
    if i <= 96 and i >= 95:
        print("You found a rare shield !")
        print("RareShield Arm+6 %Blc+25")
        try: print(f"Pick it up and replace {player1.shield.get_name()}, {player1.shield.get_armor()}, {player1.shield.get_block()} ? (y/n)", end=" ")
        except: print("Pick it up ? (y/n)", end=" ")
        while True:
            select = input("?")
            if select == "y" or select == "Y" or select == "1":
                player1.shield = Shield("RareShield", 6, 25, 260)
                break
            if select == "n" or select == "N" or select == "2":
                break
            else:
                pass
    if i <= 94 and i >= 93:
        print("You found a spell !")
        rare_spell = random.choice([Magic("HolyBolt", 35, 1, 20), Magic("FireBall", 25, 1, 15), Magic("IceBolt", 30, 1, 20), Magic("ChargedBolt", 50, 1, 25)])
        print(rare_spell)
        try: print(f"Pick it up and replace {player1.magic.get_name()}, {player1.magic.get_damage()}, {player1.magic.get_mana_cost()} ? (y/n)", end=" ")
        except: print("Pick it up ? (y/n)", end=" ")
        while True:
            select = input("?")
            if select == "y" or select == "Y" or select == "1":
                player1.magic = rare_spell
                break
            if select == "n" or select == "N" or select == "2":
                break
            else:
                pass
    if i <= 92 and i >= 91:
        print("A big magic seems to emerge from the chest, you are now full life and mana !")
        player1.set_health(player1.get_health_max())
        player1.set_mana(player1.get_mana_max())
    if i <= 90 and i >= 80:
        print("You found 1 Health Potion and 1 Mana Potion !")
        player1.set_health_potion(player1.get_health_potion() + 1)
        player1.set_mana_potion(player1.get_mana_potion() + 1)
    if i <= 70 and i >= 60:
        if player1.magic.get_level() < player1.get_level():
            print("A big magic seems to emerge from the chest, your spell is now stronger !")
            try: 
                player1.magic.set_damage(player1.magic.get_damage() + 10)
                player1.magic.set_mana_cost(player1.magic.get_mana_cost() + 5)
                player1.magic.set_level(player1.magic.get_level() + 1)
                print(f"{player1.magic.get_name()} is now level {player1.magic.get_level()} Dmg+10 ManaCost+5")
            except: 
                player1.magic = random.choice([Magic("HolyBolt", 35, 1, 20), Magic("FireBall", 25, 1, 15), Magic("IceBolt", 30, 1, 20)])
                print(f"You found a spell named: {player1.magic.get_name()} Lvl 1")
        else:
            print("A big magic seems to emerge from the chest, \n but your level is too low to learn more right now !")
        time.sleep(2)
    if i <= 60 and i >= 50:
        print("You found nothing !")
    if i <= 50 and i >= 40:
        print("You found a Health Potion !")
        player1.set_health_potion(player1.get_health_potion() + 1)
    if i <= 40 and i >= 30:
        print("You found a Mana Potion !")
        player1.set_mana_potion(player1.get_mana_potion() + 1)
    if i <= 30:
        g = np.random.randint(1, 30)
        print(f"You found {g} gold !")
        player1.set_gp(player1.get_gp() + g)
    if i <= 10:
        print("A trap has been triggered !")
        h = np.random.randint(1, 30)
        player1.set_health(player1.get_health() - h)
        print(f"You lost {h} health !")
        is_player_alive()
    time.sleep(1)
    print("The walls have disappeared !")
    time.sleep(3)
    clear_screen()
    curses.wrapper(move)
    
# To do
# Better Fight Menu: possibility to use potions in first menu, better stats display.
# Saving feature for map
# add boss monster spawn on map each 5 levels or 75% opened chest / killed monsters.
# kill the boss reset the map.

# Main Loop
while True:
    clear_screen()
    game_banner()
    screen_menu()
    map_screen()