import sys
import random
# internal modules
import shortcuts


class ExerciseBase:
    """
        There are n levels
        You start at level 1
        You will need to get 5 questions correctly answered in a row to move to the next level
        If you get a question incorrect, you will be demoted to previous level, and
        you will need to get 3 more questions right to move back.
        If you reach the highest level, you can keep practicing as much as you want.
        """

    ANSWER_FORMAT = "integer number"
    SCORE_TO_ADVANCE = 5
    INIT_SCORE_AF_DEMOTION = 2
    MAX_N_ATTEMPTS = 2

    @classmethod
    def validateAnswer(cls, t, a):
        if not ExerciseBase.isInteger(a):
            return -1
        return 0 if int(a) == eval(t) else 1

    @staticmethod
    def isInteger(s):
        return s[1:].isdigit() if s.startswith("-") else s.isdigit()

    def __init__(self):
        self.nLevels = 4
        self.score = 0
        self.level = 0

    def generateTwoOperands(self):
        n1Ranges = [
            [1, 1, 10, 100],
            [9, 9, 99, 999_999],
        ]
        n2Ranges = [
            [1, 10, 10, 100],
            [9, 99, 99, 999_999],
        ]
        n1 = random.randint(n1Ranges[0][self.level], n1Ranges[1][self.level])
        n2 = random.randint(n2Ranges[0][self.level], n2Ranges[1][self.level])
        return n1, n2

    def generateExercise(self):
        raise NotImplementedError

    def __repr__(self):
        return self.__class__.__name__

    def main(self):
        print(
            "",
            "#################%s##" % ("#" * len(self.__repr__())),
            "# Let's practice %s #" % self.__repr__(),
            "#################%s##" % ("#" * len(self.__repr__())),
            "Answer format: %s" % self.__class__.ANSWER_FORMAT,
            "",
            *shortcuts.getShortcuts(),
            "",
            sep="\n",
        )
        while True:
            q = self.generateExercise()
            print(
                "Please answer the following question (%s)." % self.__class__.ANSWER_FORMAT,
                q,
                sep="\n",
            )
            nAttempts = 0
            while True:
                inp = input(">>> ")
                shortcut = shortcuts.parseShortcuts(inp)
                if shortcut == shortcuts.RESTART:
                    self.score = 0
                    self.level = 0
                    break
                elif shortcut == shortcuts.EXIT_APP:
                    sys.exit()
                elif shortcut == shortcuts.GO_BACK:
                    return
                elif shortcut == shortcuts.CHECK_SCORE:
                    print("Check XP score is not ready yet.")
                elif shortcut is not None:
                    print("Unknown shortcuts", shortcut)
                else:
                    code = self.__class__.validateAnswer(q, inp)
                    if code == -1:
                        print("Invalid input, the answer needs to be {}, please try again.".format(
                            self.__class__.ANSWER_FORMAT,
                        ))
                    elif code == 1:
                        nAttempts += 1
                        if nAttempts >= self.__class__.MAX_N_ATTEMPTS:
                            if self.level > 0:
                                self.level -= 1
                                print("Incorrect answer, you will be demoted to level %d." % (self.level+1))
                                self.score = self.__class__.INIT_SCORE_AF_DEMOTION
                            else:
                                print("Incorrect answer, your level score is reset to 0")
                                self.score = 0
                            break
                        else:
                            print("Incorrect answer, please try again.")
                    else:
                        print("\nGreat job!\n")
                        # add 1 to score
                        self.score += 1
                        if self.score >= self.__class__.SCORE_TO_ADVANCE:
                            # advance to next level
                            if self.level < self.nLevels - 1:
                                self.score = 0
                                self.level += 1
                                print("Congrats!  You are promoted to level %d" % (self.level+1))
                        break
