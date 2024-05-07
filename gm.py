#!/usr/bin/env python3
import os
import requests

background = {
        "Soldier": "Melee +1",
        "Wizard": "Magic +1",
        "Thief": "Sneak +1",
        "Politician": "Speech +1",
        "Slave": "Toughness +1, Stamina +1",
        "Hunter": "Ranged +1"
    }

race = {
        "Human": "Speech +1",
        "Elf": "Ranged +1",
        "Ork": "Melee + 1",
        "Ratman": "Sneak +1"
        }

stats = {
    'melee' : 1,
    'sneak' : 1,
    'ranged' : 1,
    'speech' : 1,
    'toughness' : 1,
    'stamina' : 1,
    'magic' : 1
    }

char_data = {}
class GM():

    def startup():
        ui = 'ui.txt'

        modif = os.path.getmtime(ui)
        prev = modif
        while True:
            modif = os.path.getmtime(ui)
            if modif != prev:
                break
        GM.read_cmd()
    
    def read_cmd():
        ui = open('ui.txt', 'r')
        cmd = ui.readline()
        if 'character created' in cmd:
            ui.close()
            GM.character_race()
        elif (cmd != 'Choose a race: ') and ('Choose a race: ' in cmd):
            race  = cmd.removeprefix('Choose a race: ')
            char_data['race'] = race.strip()
            ui.close()
            GM.character_bg()
        elif (cmd != 'Choose a background: ') and ('Choose a background: ' in cmd):
            bg = cmd.removeprefix('Choose a background: ')
            char_data['background'] = bg.strip()
            ui.close()
            GM.character_stats()
        elif (cmd != 'Choose your stats : ') and ('Choose your stats: ' in cmd):
            p1_stats={}
            with open('ui.txt', 'r') as ui:
                for line in ui:
                    if 'Choose' not in line:
                        stat, value = line.strip().split(': ')
                        p1_stats[stat] = int(value)
            char_data['stats'] = p1_stats
            ui.close()
            GM.character_name()
        elif (cmd != 'Choose a name: ') and ('Choose a name: ' in cmd):
            name = cmd.removeprefix('Choose a name: ')
            char_data['name'] = name.strip()
            ui.close()
            requests.post('http://127.0.0.1:5000/characters',json=char_data)
            GM.startup()
    
    def character_race():
        gm = open('gm.txt', 'w')
        gm.writelines('')
        with open('gm.txt', 'a') as gm:
            gm.write("Choose a race: \n")
            for char, desc in race.items():
                gm.write(f"{char}: {desc}\n")
        gm.close()
        GM.startup()

    def character_bg():
        gm = open('gm.txt', 'w')
        gm.writelines('')
        with open('gm.txt', 'a') as gm:
            gm.write("Choose a background: \n")
            for char, desc in background.items():
                gm.write(f"{char}: {desc}\n")
        gm.close()
        GM.startup()

    def character_stats():
        gm = open('gm.txt', 'w')
        gm.writelines('')
        with open('gm.txt', 'a') as gm:
            gm.write('Choose your stats: \n')
            for stat, desc in stats.items():
                gm.write(f"{stat}: {desc}\n")
        gm.close
        GM.startup()

    def character_name():
        gm = open("gm.txt", "w")
        gm.writelines('Choose a name: ')
        gm.close()
        GM.startup()

if __name__ == "__main__":
    GM.startup()