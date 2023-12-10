import os
import pickle
import datetime


class UserProfile:
    pickleProtocol = 5

    def __init__(self, f):
        self.__f = f
        self.data = {}
        if os.path.isfile(self.__f):
            with open(self.__f, "rb") as fin:
                self.data = pickle.load(fin)
        else:
            self.dump()
        self.setdefault("streak", Streak())
        if self.data["streak"].update(xp=False):
            self.dump()

    def __getitem__(self, item):
        return self.data.get(item, None)

    def __setitem__(self, key, value):
        self.data[key] = value

    def setdefault(self, k, v):
        if k not in self.data:
            self.data[k] = v
            self.dump()
        return self.data[k]

    def addXP(self, xp):
        self.data["xp"] = self.data.get("xp", 0) + xp
        self.data["streak"].update(xp=True)

    def dump(self):
        with open(self.__f, "wb") as fout:
            pickle.dump(self.data, fout, protocol=UserProfile.pickleProtocol)

    def getStreakXPInfo(self):
        return "{}, XP: {}.".format(
            self.data.get("streak", Streak()),
            self.data.get("xp", 0),
        )


class Streak:
    """
    If you miss a day in 30 days, you still keep your streak.
    Otherwise, streak will be reset to 0
    """
    def __init__(self):
        self.lastActive = datetime.date(2000, 1, 1)
        self.freeze = 0
        self.lastMiss = datetime.date(2000, 1, 1)
        self.streakDays = 0
        self.reset()

    def reset(self):
        self.lastActive = datetime.date.today()
        self.freeze = 1
        self.lastMiss = None
        self.streakDays = 0

    def update(self, xp=True):
        today = datetime.date.today()
        daysInactive = (today - self.lastActive).days
        updated = False
        if daysInactive - self.freeze > 1:
            if self.streakDays > 0:
                print("Your streak has been reset!")
            self.reset()
            updated = True
        if xp:
            if self.streakDays == 0:
                self.reset()
                self.streakDays = 1
                updated = True
            elif daysInactive > 0:
                self.lastActive = today
                self.streakDays += 1
                if daysInactive > 1:
                    self.freeze = 0
                    self.lastMiss = today - datetime.timedelta(1)
                elif self.freeze == 0 and (today - self.lastMiss).days >= 30:
                    self.freeze = 1
                updated = True

        return updated

    def __repr__(self):
        return "Streak: {} days".format(self.streakDays)
