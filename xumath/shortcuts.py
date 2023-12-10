import sys

EXIT_APP = 0
GO_BACK = 1_000_001
CHECK_SCORE = 1_000_003

shortcuts = {
    # ctrl + B
    2: (GO_BACK, "Ctrl + B to go back to the precious menu."),
    # ctrl + D
    4: (EXIT_APP, "Ctrl + D to exit."),
    # ctrl + S
    19: (CHECK_SCORE, "Ctrl + S to check your score.")
}


def getShortcuts():
    return [v[1] for k, v in shortcuts.items()]


def parseShortcuts(inp):
    c = ord(inp[0]) if len(inp) == 1 else -1
    c = shortcuts.get(c, [None])[0]
    if c == EXIT_APP:
        print("Exit the app!")
        sys.exit()
    return c
