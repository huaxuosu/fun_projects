import sys
import shortcuts


class ListMenu:
    def __init__(self, *items):
        self.items = items

    def selectFromMenu(self):
        print(
            "",
            "Please select an item from the following list.",
            *shortcuts.getShortcuts(),
            "",
            "\n".join("%d.: %s" % (i + 1, e) for i, e in enumerate(self.items)),
            sep="\n",
        )
        while True:
            inp = input(">>> ")
            shortcut = shortcuts.parseShortcuts(inp)
            if shortcut == shortcuts.EXIT_APP:
                print("Exit the app!")
                sys.exit()
            elif shortcut == shortcuts.RESTART:
                print("Cannot restart, this is a menu!")
            elif shortcut == shortcuts.CHECK_SCORE:
                print("Check XP score is not ready yet.")
            elif shortcut == shortcuts.GO_BACK:
                return shortcut
            elif shortcut is not None:
                print("Unknown shortcuts", shortcut)
            elif inp.isdigit() and 0 < int(inp) <= len(self.items):
                return int(inp)
            else:
                # print(ord(inp))
                print("Invalid input, please try again and enter a number between 1 and {}".format(
                    len(self.items),
                ))

    def getItem(self, i):
        if i < 0 or i > len(self.items):
            print("Warning: invalid call to ListMenu.getItem with i = %d", i)
            return None
        return self.items[i-1]
