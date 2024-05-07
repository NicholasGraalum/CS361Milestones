#!/usr/bin/env python3
import requests
import os

class UI():
    
    @staticmethod
    def gm_check():
        gm = 'gm.txt'

        modif = os.path.getmtime(gm)
        prev = modif
        while True:
            modif = os.path.getmtime(gm)
            if modif != prev:
                break

    @staticmethod
    def read_cmd():
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        options = {}
        with open('gm.txt', 'r') as gm:
            phrase = gm.readline()
            for line in gm:
                if "Choose" not in line:
                    item, desc = line.strip().split(": ")
                    options[item] = desc
                    print(item)
        gm.close()
        item_in = input(phrase.removesuffix("\n"))
        ui = open('ui.txt', 'w')
        ui.writelines(phrase.removesuffix("\n") + " " + item_in)
        ui.close()

    @staticmethod
    def read_stats():
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        options = {}
        with open('gm.txt', 'r') as gm:
            phrase = gm.readline()
            for line in gm:
                if "Choose" not in line:
                    item, desc = line.strip().split(": ")
                    options[item] = desc
        gm.close()
        choice = 'N'
        while (choice.upper() == 'N') or (choice.upper() == 'NO'):
            total = 20
            for i in options:
                options[i] = str(1)
            for item in options:
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print("Choose your stats, each being 1-5 with the total being 20: ")
                for i in options:
                    print(f"{i}: {options[i]}")
                stat = input("Choose for " + item + " total remaining " +  str(total) + " : " )
                while(not stat.isnumeric()):
                    try:
                        stat = int(stat)
                    except ValueError:
                        stat = input("Choose an integer from 1-5, total remaining " + str(total) +  ": ")
                if (total - int(stat) + 1 < 0) or ((int(stat) > 5) or (int(stat) < 1)):
                    stat = input("Choose for " + item + " again, total remaining " +  str(total) + " : " )
                elif int(stat) > 1:
                    total -= (int(stat) - 1)
                    options[item] = stat
            if total > 0:
                while True:
                    for i in options:
                        os.system('cls' if os.name == 'nt' else "printf '\033c'")
                        for j in options:
                            print(f"{j}: {options[j]}")
                        print(f"You have some extra stat points to use: {total}")
                        stat = input(f"How much would you like to increase {i} by?")
                        while(not stat.isnumeric()):
                            try:
                                stat = int(stat)
                            except ValueError:
                                stat = input("Choose an integer from 1-5, total remaining " + str(total) +  ": ")
                        if (total - int(stat) + 1 < 0) or (int(options[i]) + int(stat) > 5):
                            print("make sure the end stat is less than 5 and the number inputted is positive.")
                            stat = input(f"How much would you like to increase {i} by?")
                        else:
                            new_val = int(options[i]) + int(stat)
                            options[i] = str(new_val)
                            total -= int(stat)
                        if total - int(stat) == 0:
                            break
                    if total == 0:
                        break
                    
            choice = input("Would you like to finalize your stats (Y/N): ")
            while (choice.upper() != 'Y') and (choice.upper() != 'YES') and (choice.upper() != 'N') and (choice.upper() != 'NO'):
                choice = input("Would you like to finalize your stats (Y/N): ")

        with open('ui.txt', 'w') as ui:
            ui.writelines(phrase)
            for stats, num in options.items():
                ui.write(f"{stats}: {num}\n")
        ui.close()
        
    @staticmethod
    def startup():
        while(True):
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            print("----Welcome to My text based adventure game!----\n")
            print("Choose your options:\n1)new game\n2)load game\n3)delete game\n4)exit\n")
            Uin = input("Input here: ").strip()
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            if Uin == "1":
                UI.new_game()
            elif Uin == "2":
                UI.load_game()
            elif Uin == "3":
                UI.delete_game()
            elif Uin == "4":
                print("Exiting the game. Goodbye!")
                break
    
    @staticmethod
    def get_char():
        response = requests.get('http://127.0.0.1:5000/characters')
        chars = []
        data = response.json()

        for character in data:
            char_name = character['name']
            chars.append(char_name.upper())
        return chars

    @staticmethod
    def new_game():
        ui = open('ui.txt', 'w')
        ui.writelines("character created")
        ui.close()

        i = 0
        while i < 4:
            UI.gm_check()
            if i != 2:
                UI.read_cmd()
            else:
                UI.read_stats()
                
            i += 1
        return

    @staticmethod
    def load_game():
        while(True):
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            characters = UI.get_char()
            print('--Which character would you like to load?---')
            for character in characters:
                print(character)
            print("GO BACK")
            Uin=input("input here with spaces: ").upper()
            if Uin in characters:
                while(True):
                    os.system('cls' if os.name == 'nt' else "printf '\033c'")
                    response = requests.get('http://127.0.0.1:5000/characters/' + Uin)
                    character = response.json()
                    print(f"----{character['name']}----")
                    print(f"Race: {character['race']}")
                    print(f"Background: {character['background']}")
                    print("Stats:")
                    print(f"  melee: {character['stats']['melee']}")
                    print(f"  sneak: {character['stats']['sneak']}")
                    print(f"  ranged: {character['stats']['ranged']}")
                    print(f"  speech: {character['stats']['speech']}")
                    print(f"  toughness: {character['stats']['toughness']}")
                    print(f"  stamina: {character['stats']['stamina']}")
                    print(f"  magic: {character['stats']['magic']}")
                    Uin2 = input('Go back(Y/N)?').upper()
                    if Uin2 == 'Y':
                        break
            elif Uin == 'GO BACK':
                return
            
    @staticmethod
    def delete_game():
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        chars = UI.get_char()
        if len(chars) == 0:
            print("There are no Characters to delete")
            Uin = input("Would you like to go back (Y/N): ")
            if (Uin.upper() == "Y") or (Uin.upper() == "YES"):
                UI.startup()
            else:
                return
        else:
            while(True):
                print("---all character files---")
                for character in chars:
                    print(character)
                print("Go Back")
                Uin = input("Which character would you like to delete, or would you like to go back? ")
                if Uin.upper() in chars:
                    Uin2 = input("Are you sure you would like to delete "+ Uin +" (Y/N)? ")
                    if (Uin2.upper() == "Y") or (Uin2.upper() == "YES"):
                        requests.delete('http://127.0.0.1:5000/characters/' + Uin.upper())
                        break
                    elif (Uin2.upper() == "N") or (Uin2.upper() == "NO"):
                        Uin = input("Would you like to still delete a character? ")
                        if Uin2.upper() == "N" or "NO":
                            break
                elif Uin.upper() == "GO BACK":
                    break
                else:
                    os.system('cls' if os.name == 'nt' else "printf '\033c'")
                    print("Please enter a valid character")            
        return
    
if __name__ == "__main__":
    UI.startup()