import random

class Strategija:
    def __init__(self):
        self.potez = 0
        self.bodovi = 0
        self.ukupni_bodovi = 0


class ACO(Strategija):
    def __init__(self):
        self.ime = "Always cooperate"
        super().__init__()

    def igraj(self,i, protivnik_prosli):
        potez = 1
        return potez

class ADE(Strategija):
    def __init__(self):
        self.ime = "Always defect"
        super().__init__()


    def igraj(self,i, protivnik_prosli):
        potez = 0
        return potez

class TFT(Strategija):
    def __init__(self):
        self.ime = "Tit for Tat"
        super().__init__()


    def igraj(self, i, protivnik_prosli):
        if i == 0:
            potez = 1
        else:
            potez = protivnik_prosli

        return potez
    
class TF2T(Strategija):
    def __init__(self):
        self.ime = "Tit for 2 Tats"
        self.counter = 0
        super().__init__()

    def igraj(self, i, protivnik_prosli):
        if i == 0:
            potez = 1
        else:
            if protivnik_prosli == 1:
                potez = 1
                self.counter = 0
            else:
                if self.counter == 0:
                    self.counter = self.counter + 1
                    potez = 1
                else:
                    potez = 0
                    self.counter = 0
        return potez

class STFT(Strategija):
    def __init__(self):
        self.ime = "Suspicious TFT"
        super().__init__()


    def igraj(self, i, protivnik_prosli):
        if i == 0:
            return 0
        return protivnik_prosli

class TTFT(Strategija):
    def __init__(self):
        self.ime = "Two Tits for Tat"
        self.kazna = 0
        super().__init__()


    def igraj(self, i, protivnik_prosli):
        if i == 0:
            return 1

        if self.kazna > 0:
            self.kazna -= 1
            return 0

        if protivnik_prosli == 0:
            self.kazna = 2
            return 0

        return 1

class WSLS(Strategija):
    def __init__(self):
        self.ime = "Pavlov (WSLS)"
        self.moj_prosli = 1
        super().__init__()


    def igraj(self, i, protivnik_prosli):
        if i == 0:
            self.moj_prosli = 1
            return 1
        if self.moj_prosli == protivnik_prosli:
            return self.moj_prosli
        self.moj_prosli = 1 - self.moj_prosli
        return self.moj_prosli

    
class JOSS(Strategija):
    def __init__(self):
        self.ime = "JOSS"
        super().__init__()


    def igraj(self, i, protivnik_prosli):
        if i == 0:
            potez = 1
        elif protivnik_prosli == 0:
            potez = protivnik_prosli
        else:
            if random.random() < 0.9:
                potez = protivnik_prosli
            else:
                potez = 0

        return potez
    
class FRIEDMAN(Strategija):
    def __init__(self):
        self.ime = "FRIEDMAN"
        self.flag = 0
        super().__init__()


    def igraj(self, i, protivnik_prosli):
        if i == 0:
            potez = 1
        elif not self.flag:
            potez = protivnik_prosli
            if protivnik_prosli == 0:
                self.flag = 1
        else:
            potez = 0
       

        return potez
    
class RANDOM(Strategija):
    def __init__(self):
        self.ime = "RANDOM"
        super().__init__()


    def igraj(self, i, protivnik_prosli):
        if random.random() < 0.5:
            potez = 1
        else:
            potez = 0

        return potez