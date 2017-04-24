import math
import random
import time

from gui import *
from settings import *

class Entity(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return str(self.name)

    def nextlevel(self):
        raise NotImplementedError

    def levelup(self):
        raise NotImplementedError

    def give_exp(self):
        raise NotImplementedError

class Player(Entity):
    def __init__(self, name, exp):
        self.name = name
        self.exp = exp
        self.level = 1
        self.hp = 100
        self.max_hp = 100

    def nextlevel(self):
        """Level-up experience curve, no cap"""
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

class Monster(Entity):
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

class Battle(object):
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
        target.hp -= attacker.level
        print(f"{attacker.name} attacked {target.name}, causing {attacker.level} damage!", flush=True)
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

class Stage(object):
    def __init__(self, floor):
        self.floor = floor
        self.wave = 0
        self.enemies = [Monster("Goblin",             # Name
                                (self.floor/5)+1,     # Level
                                ((self.floor/5)*100), # HP
                                (self.floor * 100,    # XP Drops
                                 1,                   # dropct
                                 [None]               # drops
                                 ))
                                for i in range((self.floor % 5)+1)]
