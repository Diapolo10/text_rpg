import math
import sys
import random
from subprocess import Popen, CREATE_NEW_CONSOLE

from settings import *
from objects import *
from gui import *

def arg_parse(args: list) -> tuple:
    """ Check call arguments for flags, defining operating mode """

    args = args[1:]
    if not args:
        print("No args!")
        return (PLAYER_NAME, MAX_STAGE_LEVEL, DEBUG_MODE)

    flags = (
             "--debug",
             "--max-stage-lvl",
             "--player-name",
             )

    try:
        player_name = (PLAYER_NAME
                       if not flags[2] in args
                       else args[args.index(flags[2])+1])
        stage_max = (MAX_STAGE_LEVEL
                     if not flags[1] in args
                     else int(args[args.index(flags[1])+1]))
        debug = (DEBUG_MODE if not flags[0] in args else True)
        print(player_name, stage_max, debug)
    except IndexError:
        raise IndexError("Missing arguments!")

    return (player_name, stage_max, debug)

def main():
    PLAYER_NAME, MAX_STAGE_LEVEL, DEBUG_MODE = arg_parse(sys.argv)
    current_stage = 1
    player = Player(PLAYER_NAME, 0)
    Popen(["python", "gui_process.py"], creationflags=CREATE_NEW_CONSOLE)
    while current_stage <= MAX_STAGE_LEVEL:
        player.hp = player.max_hp
        stage = Stage(current_stage)
        print(f"The current stage is: Floor {stage.floor}")
        if input("Challenge the current stage? ").strip() in ACCEPTED_ANSWERS:
            battle = Battle([player], stage.enemies)
            if battle.start():
                current_stage += 1
        else:
            print("Other options not implemented.")
    pass

if __name__ == "__main__":
    main()
