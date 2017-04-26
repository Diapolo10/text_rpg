import sys
from settings import *
# Used in an additional process!


class Information:

    @staticmethod
    def battle(player_party, enemy_party):
        sys.stdout.flush()

        box_width = GUI_ITEM_WIDTH
        gui_width = GUI_WIDTH - 2 * box_width
        rwidth = box_width + gui_width

        def info_row(*characters, right=False):
            print_two = False
            if len(characters) == 2:
                print_two = True

            #name_length = len(character.name)
            border = "#" * box_width
            tmp = "# {} #"
            fmt_width = box_width-(len(tmp)-2)

            name = []
            health = []
            level = []
            exp = []

            for character in characters:
                name.append(tmp.format(character.name.center(fmt_width)))
                health.append(tmp.format(f"HP: {int(character.hp)}/{int(character.max_hp)}".center(fmt_width)))
                level.append(tmp.format(f"Level: {int(character.level)}".center(fmt_width)))
                try:
                    exp.append(tmp.format(f"EXP: {character.exp}".center(fmt_width)))
                except (AttributeError, NotImplementedError):
                    exp.append(tmp.format(f"EXP: NaN".center(fmt_width)))


            if not print_two:
                if not right:
                    return f"{border}\n{name[0]}\n{health[0]}\n{level[0]}\n{exp[0]}\n{border}"
                else:
                    return f"{' '*rwidth}{border}\n{' '*rwidth}{name[0]}\n{' '*rwidth}{health[0]}\n{' '*rwidth}{level[0]}\n{' '*rwidth}{exp[0]}\n{' '*rwidth}{border}"
            else:
                return f"{border}{' '*gui_width}{border}\n{name[0]}{' '*gui_width}{name[1]}\n{health[0]}{' '*gui_width}{health[1]}\n{level[0]}{' '*gui_width}{level[1]}\n{exp[0]}{' '*gui_width}{exp[1]}\n{border}{' '*gui_width}{border}"


        chars = list(sum(zip(player_party, enemy_party+[0]), ())[:-1])
        output = [f"\n{'Player party'.center(box_width)}{' '*gui_width}{'Enemy party'.center(box_width)}"]
        min_length = min(len(player_party), len(enemy_party))

        for i in range(min_length):
            output.append(info_row(player_party[i], enemy_party[i]))
        if min_length < len(enemy_party):
            for i in enemy_party[min_length-1:]:
                output.append(info_row(i, right=True))
        elif min_length < len(player_party):
            for i in player_party[min_length-1:]:
                output.append(info_row(i))

        with open('temp.gui', 'w') as f:
            f.write("\n".join(output))
