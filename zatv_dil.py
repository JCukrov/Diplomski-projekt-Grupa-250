# 1 je kooperacija, 0 je izdaja
import random
class ACO:
    def __init__(self):
        self.ime = "Always cooperate"
        self.potez = 0
        self.bodovi = 0
        self.ukupni_bodovi = 0

    def igraj(self,i, protivnik_prosli):
        potez = 1
        return potez

class ADE:
    def __init__(self):
        self.ime = "Always defect"
        self.potez = 0
        self.bodovi = 0
        self.ukupni_bodovi = 0

    def igraj(self,i, protivnik_prosli):
        potez = 0
        return potez

class TFT:
    def __init__(self):
        self.ime = "Tit for Tat"
        self.potez = 0
        self.bodovi = 0
        self.ukupni_bodovi = 0

    def igraj(self, i, protivnik_prosli):
        if i == 0:
            potez = 1
        else:
            potez = protivnik_prosli

        return potez
    
class TF2T:
    def __init__(self):
        self.ime = "Tit for 2 Tats"
        self.potez = 0
        self.bodovi = 0
        self.counter = 0
        self.ukupni_bodovi = 0

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

class STFT:
    def __init__(self):
        self.ime = "Suspicious TFT"
        self.potez = 0
        self.bodovi = 0
        self.ukupni_bodovi = 0

    def igraj(self, i, protivnik_prosli):
        if i == 0:
            return 0
        return protivnik_prosli

class TTFT:
    def __init__(self):
        self.ime = "Two Tits for Tat"
        self.potez = 0
        self.bodovi = 0
        self.kazna = 0
        self.ukupni_bodovi = 0

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

class WSLS:
    def __init__(self):
        self.ime = "Pavlov (WSLS)"
        self.potez = 0
        self.bodovi = 0
        self.moj_prosli = 1
        self.ukupni_bodovi = 0

    def igraj(self, i, protivnik_prosli):
        if i == 0:
            self.moj_prosli = 1
            return 1
        if self.moj_prosli == protivnik_prosli:
            return self.moj_prosli
        self.moj_prosli = 1 - self.moj_prosli
        return self.moj_prosli

    
class JOSS:
    def __init__(self):
        self.ime = "JOSS"
        self.potez = 0
        self.bodovi = 0
        self.ukupni_bodovi = 0

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
    
class FRIEDMAN:
    def __init__(self):
        self.ime = "FRIEDMAN"
        self.potez = 0
        self.bodovi = 0
        self.flag = 0
        self.ukupni_bodovi = 0

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
    
class RANDOM:
    def __init__(self):
        self.ime = "RANDOM"
        self.potez = 0
        self.bodovi = 0
        self.ukupni_bodovi = 0

    def igraj(self, i, protivnik_prosli):
        if random.random() < 0.5:
            potez = 1
        else:
            potez = 0

        return potez

def igra(prvi, drugi):
    prosli1 = 1
    prosli2 = 1
    prvi.bodovi = 0
    drugi.bodovi = 0
    
    ### Potezi: 1 - oboje suradivali, 2 - samo prvi igrac suradivao, 3 - samo drugi igrac suradivao, 4 - nitko nije suradivao  
    potezi = []

    for i in range(200):
        potez1 = prvi.igraj(i, prosli2)
        potez2 = drugi.igraj(i, prosli1)

        prosli1 = potez1
        prosli2 = potez2

        if(potez1 == 1 and potez2 == 1):
            potezi.append(1)
            prvi.bodovi = prvi.bodovi + 3
            drugi.bodovi = drugi.bodovi + 3
        elif(potez1 == 1 and potez2 == 0):
            potezi.append(2)
            drugi.bodovi = drugi.bodovi + 5
        elif(potez1 == 0 and potez2 == 1):
            potezi.append(3)
            prvi.bodovi = prvi.bodovi + 5
        else:
            potezi.append(4)
            prvi.bodovi = prvi.bodovi + 1
            drugi.bodovi = drugi.bodovi + 1

    if prvi.bodovi > drugi.bodovi:
        prvi.ukupni_bodovi += 3
    elif drugi.bodovi == prvi.bodovi:
        prvi.ukupni_bodovi += 1
        drugi.ukupni_bodovi += 1
    else: drugi.ukupni_bodovi +=3


    print("Igra zavrsena")
    print(f"Igrac {prvi.ime} osvojio je {prvi.bodovi} bodova")
    print(f"Igrac {drugi.ime} osvojio je {drugi.bodovi} bodova")
    return potezi
        

if __name__ == "__main__":
    igraci = []
    igraci.append(TFT())
    igraci.append(TF2T())
    igraci.append(JOSS())
    igraci.append(FRIEDMAN())
    igraci.append(RANDOM())
    igraci.append(ADE())
    igraci.append(ACO())
    igraci.append(STFT())
    igraci.append(TTFT())
    igraci.append(WSLS())

    protivnici = [type(i)() for i in igraci]

    with open('./igre.csv', 'w+', encoding='UTF-8') as output:
        output.write('#Prvi igrac;Bodovi Prvog;Drugi igrac;Bodovi drugog;Potezi\n')

        for i in range(len(igraci)):
            for j in range(i, len(protivnici)):
                potezi = igra(igraci[i], protivnici[j])
                
                output.write(f'{igraci[i].ime};{igraci[i].bodovi};{protivnici[j].ime};{protivnici[j].bodovi};{potezi}\n')


    poredak = sorted(igraci, key=lambda x: x.ukupni_bodovi, reverse=True)

    print("\n===== TABLICA PORETKA =====")
    for idx, ig in enumerate(poredak, start=1):
        print(f"{idx}. {ig.ime} - {ig.ukupni_bodovi} bodovi")

    with open('./poredak.csv', 'w+', encoding='UTF-8') as output:
        output.write('#Rank;Ime;Ostvareni bodovi\n')
        for idx, ig in enumerate(poredak, start=1):
            output.write(f'{idx};{ig.ime};{ig.ukupni_bodovi}\n')