import random

class Strategija:
    def __init__(self):
        self.potez = 0
        # broj bodova u jednoj igri
        self.bodovi = 0
        # ukupni ostvareni broj bodova kroz sve igre
        self.kumulativni_bodovi = 0
        # match-win sistem dodjele bodova
        self.ukupni_bodovi = 0

    def reset(self):
        self.potez = 0
        self.bodovi = 0
        # Reset strategy-specific state
        if hasattr(self, 'moj_prosli'):  # WSLS
            self.moj_prosli = 1
        if hasattr(self, 'counter'):  # TF2T, NYDEGGER, SHUBIK
            self.counter = 0
        if hasattr(self, 'kazna'):   # TTFT, SHUBIK
            self.kazna = 0
        if hasattr(self, 'flag'):    # FRIEDMAN
            self.flag = 0
        if hasattr(self, 'punish'):
            self.punish = False
        if hasattr(self, 'nakonC_total'): #DOWNING
            self.nakonC_total = 0
            self.nakonC_C = 0
            self.nakonD_total = 0
            self.nakonD_C = 0
            self.zadnji = 0
        if hasattr(self, 'zadnji'): #NYDEGGER
            self.zadnji = 0
            

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
        super().__init__()
        self.ime = "JOSS"


    def igraj(self, i, protivnik_prosli):
        if i == 0:
            potez = 1
        elif not protivnik_prosli:
            potez = 0
        else:
            if random.random() < 0.9:
                potez = 1
            else:
                potez = 0

        return potez
    
class FRIEDMAN(Strategija):
    def __init__(self):
        self.ime = "FRIEDMAN (Grim Trigger)"
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
    
class DOWNING(Strategija):
    def __init__(self):
        super().__init__()
        self.ime = "DOWNING"
        self.nakonC_total = 0
        self.nakonC_C = 0
        self.nakonD_total = 0
        self.nakonD_C = 0
        self.zadnji = 0

    def procjena(self):
        if  self.nakonC_total > 0:
            pC = self.nakonC_C / self.nakonC_total
        else:
            pC = 0.5

        if self.nakonD_total > 0:
            pD = self.nakonD_C / self.nakonD_total
        else:
            pD = 0.5
        
        return pC, pD

    def odaberi_potez(self):
        pC, pD = self.procjena()

        eC = pC * 3
        eD = pD * 5 + (1 - pD)

        if eC > eD:
            potez = 1
        else:
            potez = 0

        self.zadnji = potez
        return potez
    
    def igraj(self, i, protivnik_prosli):
        if i != 0:
            if self.zadnji:
                self.nakonC_total += 1
                if protivnik_prosli:
                    self.nakonC_C += 1
            else:
                self.nakonD_total += 1
                if protivnik_prosli:
                    self.nakonD_C += 1

        potez = self.odaberi_potez()
        return potez
    
class FELD(Strategija):
    def __init__(self):
        super().__init__()
        self.ime = "FELD"
    
    def igraj(self, i, protivnik_prosli):
        if i == 0:
            potez = 1
        else:
            if not protivnik_prosli:
                potez = 0
            else:
                p = 1.0 - 0.5 * (i - 1) / 199
                if random.random() < p:
                    potez = 1
                else: 
                    potez = 0
        return potez

class SHUBIK(Strategija):
    def __init__(self):
        super().__init__()
        self.ime = "SHUBIK"
        self.kazna = 0
        self.counter = 0
    
    def igraj(self, i , protivnik_prosli):
        if i == 0:
            potez = 1
        else:
            if self.kazna > 0:
                potez = 0
                self.kazna -= 1
            else:
                if protivnik_prosli:
                    potez = 1
                else:
                    self.counter += 1
                    self.kazna = self.counter
                    potez = 0
                    self.kazna -= 1
        return potez
    
class NYDEGGER(Strategija):
    def __init__(self):
        super().__init__()
        self.ime = "NYDEGGER"
        self.counter = 0
        self.zadnji = 0

    def igraj(self, i, protivnik_prosli):
        if not self.zadnji and not protivnik_prosli:
            self.counter += 1
        else:
            self.counter = 0

        if i == 0:
            potez = 1
        else:
            if self.counter == 3:
                potez = 1
                self.counter = 0
            else:
                if protivnik_prosli:
                    potez = 1
                else:
                    potez = 0

        self.zadnji = potez
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
