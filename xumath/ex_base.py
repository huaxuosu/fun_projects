# internal modules
# import os, sys
#
# from os.path import dirname, join, abspath
# sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from algo.tools.str_fmt import framedStr
from ui import shortcuts
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

    ###
    # constants
    ###
    ANSWER_FORMAT = "integer number"
    # if SCORE_TO_ADVANCE number of questions are correct, advance to next level
    SCORE_TO_ADVANCE = 5
    # MAX_SCORE is the highest score (i.e. # of qs correct) for the highest level
    MAX_SCORE = 100
    # your score for the level starts at 0.  If you are demoted to the level, the score starts at 2
    INIT_SCORE_AF_DEMOTION = 2
    # you can fail up to 1 times without score reduction
    MAX_N_ATTEMPTS = 2
    # [xp for 1st level, xp for 2nd level, xp for 3rd level,
    #  xp for 4th level or higher,
    #  xp for highest level when score > SCORE_TO_ADVANCE]
    XP_DISTRIBUTION = [5, 10, 10, 20, 40]

    ###
    # class vars
    ###
    __USR_PROF = None

    @classmethod
    def initUsrProf(cls, usrProf: UserProfile):
        """
        initialize the class with user profile data
        """
        assert(isinstance(usrProf, UserProfile))
        cls.__USR_PROF = usrProf

    def __init__(self, *args, **kwargs):
        if self.__USR_PROF is None:
            raise Exception("You have to call ExerciseBase.initUsrProf before calling its constructor.")
        self.nLevels = 4
        exerciseData = self.__USR_PROF.setdefault(self.name, {})
        self.level = exerciseData.setdefault("level", 0)
        self.score = exerciseData.setdefault("score", 0)

    def generateExercise(self):
        raise NotImplementedError

    def validateAnswer(self, q, a):
        raise NotImplementedError

    @property
    def name(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.name

    def main(self):
        """
        Main for loop to generate the exercises and score them
        """
        print(
            "",
            framedStr("Let's practice " + self.name),
            self.__USR_PROF.getStreakXPInfo(),
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
                    print(self.__USR_PROF.getStreakXPInfo(), self._getScoreInfo(), sep="\n")
                elif shortcut is not None:
                    print("Unknown shortcuts", shortcut)
                else:
                    err = self.validateAnswer(q, inp)
                    if err == 0:
                        print("\nGreat job!\n")
                        mssg = self.__addScore()
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
                            mssg = self.__addScore(demote=True)
                            print("Incorrect answer. %s" % mssg)
                            break
                        else:
                            print("Incorrect answer, please try again.")
                    else:
                        raise NotImplementedError

    def _getScoreInfo(self):
        return "{}: level {}/{}, score {}/{}".format(
            self.name,
            # level starts at 0 in data, but it starts at 1 in display
            self.level + 1,
            self.nLevels,
            self.score,
            self.SCORE_TO_ADVANCE if self.level < self.nLevels-1 else self.MAX_SCORE,
        )

    def __addScore(self, demote=False):
        mssg = None
        if not demote:
            # scored a question
            # calculate XP
            self.__USR_PROF.addXP(self.__calcXP())
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
        self.__saveUsrProf()
        return mssg

    def __calcXP(self):
        if self.level == self.nLevels - 1:
            return self.XP_DISTRIBUTION[-1 if self.score >= self.SCORE_TO_ADVANCE else -2]
        return self.XP_DISTRIBUTION[min(self.level, len(self.XP_DISTRIBUTION)-2)]

    def __saveUsrProf(self):
        self.__USR_PROF[self.name]["level"] = self.level
        self.__USR_PROF[self.name]["score"] = self.score
        self.__USR_PROF.dump()
