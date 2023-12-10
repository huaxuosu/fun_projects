import sys

EXIT_APP = 0
GO_BACK = 1_000_001
CHECK_SCORE = 1_000_003

shortcuts = {
    "B": (GO_BACK, "to go back to the precious menu."),
    "E": (EXIT_APP, "to exit."),
    "X": (CHECK_SCORE, "to check your score."),
}


def getShortcuts():
    return ["Ctrl + %s %s" % (k, v[1]) for k, v in shortcuts.items()]


def parseShortcuts(inp):
    shortcut = None
    if len(inp) == 1 and ord(inp[0]) <= 26:
        c = chr(ord(inp[0]) + ord("A") - 1)
        if c in shortcuts:
            shortcut = shortcuts[c][0]
            if shortcut == EXIT_APP:
                print("Exit the app!")
                sys.exit()
    return shortcut
