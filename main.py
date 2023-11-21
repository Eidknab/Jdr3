from objects.characters import Character
from objects.weapons import Weapon
from objects.magic import Magic
from objects.potions import Potion
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
def character_creation(name, class_name="default", level=1, health=100, health_max=100, mana=0, mana_max=0, xp=0, xp_max=100, strength=15, critical=5, armor=1, turn=1):
    if name == "Player":
        global player1
        player1 = Character("Player", class_name, level, health, health_max, 40, 40, xp_max, xp, strength, critical, armor, turn)
        player1.weapon = Weapon("Sword", 10)
        player1.magic = Magic("HolyBolt", 30, 1, 20)
        player1.potion = Potion("Health Potion", 40, 0, 1)
    elif name == "Monster":
        global monster1
        if class_name == "default":
            class_name = np.random.choice(["Wolf", "Zombie", "Skeleton"])
        if player1.get_level() > 1:
            level = player1.get_level() + np.random.randint(-1, 2)
        elif player1.get_level() == 1:
            level = player1.get_level() + np.random.randint(0, 2)
        monster1 = Character("Monster", class_name, level, health, health_max, mana, mana_max, xp_max, xp, strength, critical, armor, turn)
        for i in range(0, monster1.get_level()):
            Character.level_up(monster1)
        
# Create a new map (change the map_size variable to change the size of the map)
def map_creation():
    global map_size
    global map
    map_size = 20
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
    print("_"*20 + "\n")
    print("  KNIGHT'S QUEST I")
    print("_"*20 + "\n")
    return

# Display the main menu
def screen_menu():
    print("1. New Game")
    print("2. Quit")
    print("")
    while True:
        select = input("? Votre choix : ")
        if select == "1":
            new_game()
            break
        if select == "2" or select == "q" or select == "Q":
            sys.exit()

# Display Characters Stats
def character_display(name):
    print("-"*50)
    print(f"{name.get_name()} {name.get_class_name()} Lvl {name.get_level()} Exp {int(name.get_xp())}/{int(name.get_xp_max())} HP {name.get_health()}/{name.get_health_max()} MP {name.get_mana()}/{name.get_mana_max()}")
    print(f"Strength {name.get_strength()} Critical {name.get_critical()} Armor {name.get_armor()}")
    print("-"*50)

# Display VERSUS animation between two characters in a fight
def display_versus(duration, total_length=50):
    word = "VERSUS"
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
    print("\n1.Move 2.Fight 3.Inventory 4.Quit")
    while True:
        select = input("? Votre choix : ") 
        if select == "1":
            print("Not Implemented Yet !")
        if select == "2":
            fight_screen()
        if select == "3":
            print("Not Implemented Yet !")
        if select == "4" or select == "q" or select == "Q":
            sys.exit()
            
# Create a new monster and start a fight screen
def fight_screen():
    character_creation("Monster", turn=0)
    i = 0
    while monster1.get_health() > 0 and player1.get_health() > 0:
        clear_screen()
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
    if (player1.has_magic() is not None) and (player1.get_mana() >= player1.magic.get_mana_cost()):
        print(f"\n1.Attack 2.{player1.magic.get_name()}({player1.magic.get_level()}) 3.Potions 4.Run")
    else:
        print(f"\n1.Attack 3.Potions 4.Run")
    while True:
        select = input("? Votre choix : ") 
        if select == "1":
            turn_test(magic=False)
            break
        if select == "2" and player1.get_mana() >= player1.magic.get_mana_cost():
            turn_test(magic=True)
            break
        if select == "3":
            player1.use_potion("Health Potion")
            # player1.set_health(player1.get_health() + 40)
            # if player1.get_health() > player1.get_health_max():
            #     player1.set_health(player1.get_health_max())
            break
        if select == "4" or select == "q" or select == "Q":
            map_screen()
            break
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
        time.sleep(5)
        map_screen()
        
def is_player_alive():
    if player1.get_health() <= 0:
        print(f"{player1.get_name()} is dead !")
        time.sleep(5)
        sys.exit()
    
# player_magic()
# player_potions()
# player_inventory()
# move()

# Main Loop
while True:
    clear_screen()
    game_banner()
    screen_menu()
    map_screen()