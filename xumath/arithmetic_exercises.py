import random
# internal modules
import shortcuts
from user_profile import UserProfile


class ExerciseBase:
    """
    There are n levels
    You start at level 1
    You will need to get 5 questions correctly answered in a row to move to the next level
    If you get a question incorrect, you will be demoted to previous level, and
    you will need to get 3 more questions right to move back.
    If you reach the highest level, you can keep practicing as much as you want.

    User level info and XP scores are stored in a dictionary that is pickled to a file
    the userProf dictionary needs to have
        Exercise Name: {
            level: current level
            score: score of the current level
        }
    """

    ANSWER_FORMAT = "integer number"
    SCORE_TO_ADVANCE = 5
    MAX_SCORE = 100
    INIT_SCORE_AF_DEMOTION = 2
    MAX_N_ATTEMPTS = 2
    XP_DISTRIBUTION = [5, 10, 10, 20, 40]

    @classmethod
    def validateAnswer(cls, q, a):
        if a.isdigit() or (a.startswith("-") and a[1:].isdigit()):
            return 0 if int(a) == eval(q) else 1
        return -1

    def __init__(self, usrProf: UserProfile):
        self.usrProf = usrProf
        assert(isinstance(self.usrProf, UserProfile))
        self.nLevels = 4
        exerciseData = self.usrProf.setdefault(self.name, {})
        self.level = exerciseData.setdefault("level", 0)
        self.score = exerciseData.setdefault("score", 0)

    def generateTwoOperands(self, n1Ranges=None, n2Ranges=None):
        n1Ranges = n1Ranges or [
            [1, 1, 10, 100],
            [9, 9, 99, 999_999],
        ]
        n2Ranges = n2Ranges or [
            [1, 10, 10, 100],
            [9, 99, 99, 999_999],
        ]
        assert(len(n1Ranges) == len(n2Ranges) == 2)
        assert(len(n1Ranges[0]) == len(n1Ranges[1]) == self.nLevels)
        assert(len(n2Ranges[0]) == len(n2Ranges[1]) == self.nLevels)
        n1 = random.randint(n1Ranges[0][self.level], n1Ranges[1][self.level])
        n2 = random.randint(n2Ranges[0][self.level], n2Ranges[1][self.level])
        return n1, n2

    def generateExercise(self):
        raise NotImplementedError

    @property
    def name(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.name

    def main(self):
        print(
            "",
            "#################%s##" % ("#" * len(self.__repr__())),
            "# Let's practice %s #" % self.__repr__(),
            "#################%s##" % ("#" * len(self.__repr__())),
            self.usrProf.getStreakXPInfo(),
            self._getScoreInfo(),
            "Answer format: %s" % self.ANSWER_FORMAT,
            "",
            *shortcuts.getShortcuts(),
            "",
            sep="\n",
        )
        while True:
            q = self.generateExercise()
            print(
                "Please answer the following question (%s)." % self.ANSWER_FORMAT,
                q,
                sep="\n",
            )
            nAttempts = 0
            while True:
                inp = input(">>> ")
                shortcut = shortcuts.parseShortcuts(inp)
                if shortcut == shortcuts.GO_BACK:
                    return
                elif shortcut == shortcuts.CHECK_SCORE:
                    print(self.usrProf.getStreakXPInfo(), self._getScoreInfo(), sep="\n")
                elif shortcut is not None:
                    print("Unknown shortcuts", shortcut)
                else:
                    err = self.validateAnswer(q, inp)
                    if err == 0:
                        print("\nGreat job!\n")
                        mssg = self._addScore()
                        if mssg:
                            print(mssg)
                        break
                    elif err == -1:
                        print("Invalid input, the answer needs to be {}, please try again.".format(
                            self.ANSWER_FORMAT,
                        ))
                    elif err == 1:
                        nAttempts += 1
                        if nAttempts >= self.MAX_N_ATTEMPTS:
                            mssg = self._addScore(demote=True)
                            print("Incorrect answer. %s" % mssg)
                            break
                        else:
                            print("Incorrect answer, please try again.")
                    else:
                        raise NotImplementedError

    def _getScoreInfo(self):
        return "{}: level {}/{}, score {}/{}".format(
            self.name,
            self.level + 1,
            self.nLevels,
            self.score,
            self.SCORE_TO_ADVANCE if self.level < self.nLevels-1 else self.MAX_SCORE,
        )

    def _addScore(self, demote=False):
        mssg = None
        if not demote:
            # scored a question
            # calculate XP
            self.usrProf.addXP(self._calcXP())
            # add 1 to score
            self.score += 1
            if self.level == self.nLevels - 1 and self.score == self.MAX_SCORE:
                mssg = "Congrats! You have achieved the highest score for the highest level."
            elif self.score >= self.SCORE_TO_ADVANCE and self.level < self.nLevels - 1:
                # advance to next level
                self.score = 0
                self.level += 1
                mssg = "Congrats! You are promoted to level %d" % (self.level + 1)
        elif self.score > self.SCORE_TO_ADVANCE:
            # subtract 1 from score
            self.score -= 1
            mssg = self._getScoreInfo()
        elif self.level > 0:
            self.level -= 1
            mssg = "You are demoted to level %d." % (self.level + 1)
            self.score = self.INIT_SCORE_AF_DEMOTION
        else:
            mssg = "Your level score is reset to 0."
            self.score = 0
        self._saveUsrProf()
        return mssg

    def _calcXP(self):
        if self.level == self.nLevels - 1:
            return self.XP_DISTRIBUTION[-1 if self.score >= self.SCORE_TO_ADVANCE else -2]
        return self.XP_DISTRIBUTION[min(self.level, len(self.XP_DISTRIBUTION)-2)]

    def _saveUsrProf(self):
        self.usrProf[self.name]["level"] = self.level
        self.usrProf[self.name]["score"] = self.score
        self.usrProf.dump()


class Addition(ExerciseBase):
    def generateExercise(self):
        return "{} + {}".format(*self.generateTwoOperands())


class Subtraction(ExerciseBase):
    def generateExercise(self):
        return "{1:} - {0:}".format(*self.generateTwoOperands())


class Multiplication(ExerciseBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nLevels = 5

    def generateExercise(self):
        n1Ranges = [
            [1, 1, 11, 111, 111],
            [9, 9, 99, 999, 999],
        ]
        n2Ranges = [
            [1, 11, 111, 111, 1111],
            [9, 99, 999, 999, 999_999],
        ]
        return "{1:} * {0:}".format(*self.generateTwoOperands(n1Ranges, n2Ranges))


class Division(ExerciseBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nLevels = 5

    def generateExercise(self):
        n1Ranges = [
            [1, 1, 1, 11, 11],
            [9, 9, 9, 99, 99],
        ]
        n2Ranges = [
            [1, 11, 111, 111, 1111],
            [9, 99, 999, 999, 999_999],
        ]
        return "{1:} // {0:}".format(*self.generateTwoOperands(n1Ranges, n2Ranges))
