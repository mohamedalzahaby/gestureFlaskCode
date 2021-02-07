class Dataset:
    def getDataset(self, **entries):
        self.__dict__.update(entries)

    def setDataset(self, dribbling, right_pass, right_v, walking, wrong_pass_1, wrong_pass_2):
        self.dribbling = dribbling
        self.right_pass = right_pass
        self.right_v = right_v
        self.walking = walking
        self.wrong_pass_1 = wrong_pass_1
        self.wrong_pass_2 = wrong_pass_2

    def setWindowDataset(self, dribbling, right_pass, right_v, walking, wrong_pass_1, wrong_pass_2):
        self.dribbling = dribbling
        self.right_pass = right_pass
        self.right_v = right_v
        self.walking = walking
        self.wrong_pass_1 = wrong_pass_1
        self.wrong_pass_2 = wrong_pass_2