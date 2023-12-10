import os
import pickle


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

    def dump(self):
        with open(self.__f, "wb") as fout:
            pickle.dump(self.data, fout, protocol=UserProfile.pickleProtocol)

    def getScoreInfo(self):
        return "Streak: {} days. XP: {}".format(
            self.data.get("streak", 0),
            self.data.get("xp", 0),
        )
