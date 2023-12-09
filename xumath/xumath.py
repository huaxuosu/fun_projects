"""
Created on Sat Dec  9 13:50:54 2023

@author: Hua Xu
"""

import sys
# internal modules
import shortcuts
import menus
from addition import Addition
from subtraction import Subtraction
from multiplication import Multiplication
from division import Division

__version__ = "v0.0.1"


def main():
    print(
        "###########",
        "# XU MATH #",
        "###########",
        "Version: %s" % __version__,
        "",
        "Hello Hanyong!",
        "Welcome to XU Math!",
        "I am lucky to have you!",
        sep="\n",
    )

    mainMenu = menus.ListMenu(
        Addition(),
        Subtraction(),
        Multiplication(),
        Division(),
    )

    while True:
        choice = mainMenu.selectFromMenu()
        if choice == shortcuts.GO_BACK:
            print("This is the main menu, cannot go back. Exit the app.")
            sys.exit()
        ex = mainMenu.getItem(choice)
        if ex is not None:
            ex.main()


if __name__ == "__main__":
    main()
