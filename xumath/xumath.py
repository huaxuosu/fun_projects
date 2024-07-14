"""
Created on Sat Dec  9 13:50:54 2023

@author: Hua Xu
"""

import sys
import os.path
import random
# internal modules
from algo.tools.str_fmt import framedStr
from ui import menus, shortcuts
from user_profile import UserProfile
from ex_base import ExerciseBase
from ex_simple_op import (
    Addition,
    Subtraction,
    Multiplication,
    Division,
)
from ex_complex_op import FourOperations
from ex_fac_n_mul import (
    Factors,
    Multiples,
)
from ex_fraction import ExFractions
from ex_decimal import Decimals

__version__ = "v0.0.2"
__user__ = "hanyong"


"""
To do:
- variables & equations
- power / exponential / logarithm / sqaure/cube & root
"""


def main():
    print(
        framedStr("XU MATH"),
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
    print(usrProf.getStreakXPInfo())
    ExerciseBase.init(usrProf)
    mainMenu = menus.ListMenu(
        Addition,
        Subtraction,
        Multiplication,
        Division,
        FourOperations,
        Factors,
        Multiples,
        ExFractions,
        Decimals,
        baseClass=ExerciseBase,
    )

    random.seed()
    while True:
        choice = mainMenu.selectFromMenu()
        if choice == shortcuts.GO_BACK:
            print("This is the main menu, cannot go back. Exit the app.")
            sys.exit()
        elif choice == shortcuts.CHECK_SCORE:
            print(usrProf.getStreakXPInfo())
        else:
            mainMenu.getItem(choice).main()


if __name__ == "__main__":
    main()
