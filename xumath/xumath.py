"""
Created on Sat Dec  9 13:50:54 2023

@author: Hua Xu
"""

import sys
import os.path
# internal modules
import shortcuts
from user_profile import UserProfile
import menus
from ex_simple_op import (
    Addition,
    Subtraction,
    Multiplication,
    Division,
)

__version__ = "v0.0.2"
__user__ = "hanyong"


def main():
    print(
        "###########",
        "# XU MATH #",
        "###########",
        "Version: %s" % __version__,
        "",
        "Hello Hanyong!",
        "Welcome back to XU Math!",
        "I am lucky to have you!",
        "",
        sep="\n",
    )

    # user profile
    usrProfFile = os.path.join(os.path.dirname(sys.argv[0]), __user__ + ".prf")
    usrProf = UserProfile(usrProfFile)
    print(usrProf.data)
    print(usrProf.getStreakXPInfo())
    mainMenu = menus.ListMenu(
        Addition(usrProf),
        Subtraction(usrProf),
        Multiplication(usrProf),
        Division(usrProf),
    )

    while True:
        choice = mainMenu.selectFromMenu()
        if choice == shortcuts.GO_BACK:
            print("This is the main menu, cannot go back. Exit the app.")
            sys.exit()
        elif choice == shortcuts.CHECK_SCORE:
            print(usrProf.getStreakXPInfo())
        else:
            ex = mainMenu.getItem(choice)
            if ex is not None:
                ex.main()


if __name__ == "__main__":
    main()
