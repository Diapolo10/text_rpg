import math
import random
import time

from gui import *
from settings import *

################################# Item classes ################################

class Item:
    def __init__(self, name):
        self.name = name
        self.is_worn = False
        self.worn_slot = None

    def __str__(self):
        return f"Item({self.name})"

    def __repr__(self):
        return f"Item({self.name})"

class Weapon(Item):
    def __init__(self, name, attack_power, level_req=None, is_two_handed=False):
        self.name = name
        self.attpow = attack_power
        self.level_req = level_req
        self.is2h = is_two_handed
        self.is_worn = True
        self.worn_slot = 0

    def __str__(self):
        return f"Weapon({self.name}, {self.attpow}, level_req: {self.level_req}, 2h: {self.is2h})"

    def __repr__(self):
        return f"Weapon({self.name}, {self.attpow}, level_req: {self.level_req}, 2h: {self.is2h})"

class Shield(Item):
    def __init__(self, name, defence, level_req=None):
        self.name = name
        self.dfc = defence
        self.level_req = level_req
        self.is_worn = True
        self.worn_slot = 1

    def __str__(self):
        return f"Shield({self.name}, {self.dfc}, level_req: {self.level_req})"

    def __repr__(self):
        return f"Shield({self.name}, {self.dfc}, level_req: {self.level_req})"

class Armour(Item):
    def __init__(self, name: str, defence: int, slot: int, level_req=None):
        self.name = name
        self.dfc = defence
        self.worn_slot = slot
        self.level_req = level_req
        self.is_worn = True

    def __str__(self):
        return f"Armour({self.name}, {self.dfc}, {self.worn_slot}, level_req: {self.level_req})"

    def __repr__(self):
        return f"Armour({self.name}, {self.dfc}, {self.worn_slot}, level_req: {self.level_req})"

############################### Entity classes ################################

class Entity:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"Entity({self.name})"

    def __repr__(self):
        return f"Entity({self.name})"

    @property
    def attack(self):
        raise NotImplementedError

    @property
    def defence(self):
        raise NotImplementedError

    def nextlevel(self):
        raise NotImplementedError

    def levelup(self):
        raise NotImplementedError

    def give_exp(self):
        raise NotImplementedError

class Player(Entity):
    def __init__(self, name: str, exp: int):
        self.name = name
        self.exp = exp
        self.level = 1
        self.hp = 100
        self.max_hp = 100
        self.equipment = [
            None, # Weapon
            None, # Shield
            None, # Head
            None, # Body
            None, # Legs
        ]

    def __str__(self):
        return f"Player({self.name}, level: {self.level}, gear: {self.equipment})"

    def __repr__(self):
        return f"Player({self.name}, level: {self.level}, gear: {self.equipment})"

    @property
    def attack(self):
        """ Returns player's real attack power as int """
        equipment_power = sum([i.attpow if hasattr(i, 'attpow') else 0 for i in self.equipment])
        return round(self.level * 0.3 + equipment_power + 1)

    @property
    def defence(self):
        """ Returns player's real defence as int """
        equipment_def = sum([i.dfc if hasattr(i, 'dfc') else 0 for i in self.equipment])
        return round(self.level * 0.1 + equipment_def)

    def nextlevel(self):
        """ Level-up experience curve, no cap """
        exponent = 1.6
        basexp = 85
        return math.floor(basexp * self.level**exponent)

    def levelup(self):
        counter = 0
        while True:
            if self.nextlevel() <= self.exp:
                self.level += 1
                counter += 1
                self.max_hp = math.floor(self.max_hp * 1.1 + 100)
                self.hp = self.max_hp
            else:
                if counter > 1:
                    print("You levelled up {} times at once!".format(counter))
                if counter:
                    print("Congratulations! You are now level {}.".format(self.level))
                print("EXP required for next level: {}".format(self.nextlevel() - self.exp))
                break

    def give_exp(self, value):
        self.exp += value
        self.levelup()

class Enemy(Entity):
    def __init__(self, name, level, hp=1337, loot=(0,0,())):
        """
        name: str
        level: int
        hp: int
        loot: (xp: int,
               drops: int,
               drop_table: tuple)
        """
        self.name = name
        self.level = level
        self.hp = hp
        self.max_hp = self.hp
        self.reward_exp = loot[0]
        self.drop_count = random.randint(0,loot[1])
        self.drop_table = loot[2]

    def __str__(self):
        return f"Enemy({self.name}, level: {self.level}, hp: {self.max_hp}, drops: {self.drop_table})"

    def __repr__(self):
        return f"Enemy({self.name}, level: {self.level}, hp: {self.max_hp}, drops: {self.drop_table})"

    @property
    def attack(self):
        return int(self.level ** 1.5 + 1)

    @property
    def defence(self):
        return int(self.level ** 1.1)

################################ Game objects #################################

class Battle:
    """ Creates a battle sequence """
    def __init__(self, party, enemy):
        """
        party: list of player party members
        enemy: list of enemy objects
        """
        self.party = party
        self.enemy = enemy
        self.party_hp = sum([int(char.hp) for char in self.party])
        self.enemy_hp = sum([int(e.hp) for e in self.enemy])
        self.update_gui()

    def start(self):
        while self.party_hp or self.enemy_hp:
            try:
                for char in self.party:
                    target = random.choice(self.enemy)
                    self.attack(char, target)
                for e in self.enemy:
                    target = random.choice(self.party)
                    self.attack(e, target)
            except IndexError:
                pass
            self.group_hp()
            if not self.party_hp:
                print("Players lost!", flush=True)
                return False
            if not self.enemy_hp:
                print("Enemies lost!", flush=True)
                return True

    def attack(self, attacker, target):
        attack_avg = attacker.attack * (MAX_DEFENCE - target.defence) / MAX_DEFENCE
        variance = round(random.uniform(0.0, 1.0), 3)
        attack_dmg = round(attack_avg * variance)

        target.hp -= attack_dmg
        if attack_dmg:
            print(f"{attacker.name} attacked {target.name}, causing {int(round(attack_dmg))} damage!", flush=True)
        else:
            print(f"{attacker.name} tried to attack {target.name}, but they skillfully dodged it.")
        time.sleep(0.1)
        if target.hp <= 0:
            target.hp = 0
            print(f"{target.name} fell in battle!", flush=True)
            try:
                attacker.give_exp(target.reward_exp)
            except AttributeError:
                pass
            try:
                self.enemy.remove(target)
            except ValueError:
                self.party.remove(target)
        self.update_gui()

    def update_gui(self):
        Information.battle(self.party, self.enemy)

    def group_hp(self):
        self.party_hp = sum([int(char.hp) for char in self.party])
        self.enemy_hp = sum([int(e.hp) for e in self.enemy])

class Stage:
    """ Creates a stage with multiple battle sequences """
    def __init__(self, floor):
        self.floor = floor
        self.wave = 0
        self.enemies = [Enemy("Goblin",             # Name
                                (self.floor/5)+1,     # Level
                                ((self.floor/5)*100), # HP
                                (self.floor * 100,    # XP Drops
                                 1,                   # dropct
                                 [None]               # drops
                                 ))
                                for i in range((self.floor % 5)+1)]
