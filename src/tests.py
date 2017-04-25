from gui import *
from objects import *
from settings import *

player_party = [
                Player("Kaguya",0),
                Player("D3fau1t",0),
                Player("Cole",0),
                Player("Diapolo10",0)
                ]

enemy_party = [
               Monster("Thingummywut", 10)
               for i in range(4)
               ]

weapons = [
    Weapon("Excalibur", 42),
    Weapon("Stick o' power", 12, level_req=10),
    Weapon("Futility", 777, level_req=99, is_two_handed=True)
]

def gui_battle_tests():
    data = Information()
    data.battle(player_party, enemy_party)

def object_tests():
    for i in weapons:
        print(f"I love {i.name}!")
        print(i.__repr__())

if __name__ == "__main__":
    # gui_battle_tests()
    object_tests()
