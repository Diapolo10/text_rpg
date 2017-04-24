from gui import *
from objects import *
from settings import *

player_party = [Player("Kaguya",0),
                Player("D3fau1t",0),
                Player("Cole",0),
                Player("Diapolo10",0)
                ]

enemy_party = [
               Monster("Thingummywut", 10)
               for i in range(4)
               ]

data = Information()
data.battle(player_party, enemy_party)
