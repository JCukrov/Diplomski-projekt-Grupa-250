# 1 je kooperacija, 0 je izdaja
import random
import matplotlib.pyplot as plt
import numpy as np

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
    
    # Potezi: 1oboje suradivali, 2 samo prvi igrac suradivao, 3  samo drugi igrac suradivao, 4 nitko nije suradivao  
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

def vizualiziraj_rezultate(igraci, sve_igre):

    
    # 1. Grafikon konačnog poretka
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Poredak igrača
    poredak = sorted(igraci, key=lambda x: x.ukupni_bodovi, reverse=True)
    imena = [ig.ime for ig in poredak]
    bodovi = [ig.ukupni_bodovi for ig in poredak]
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(imena)))
    bars = axes[0, 0].barh(imena, bodovi, color=colors)
    axes[0, 0].set_xlabel('Ukupni bodovi', fontsize=12)
    axes[0, 0].set_title('Konačni poredak strategija', fontsize=14, fontweight='bold')
    axes[0, 0].invert_yaxis()
    

    
    # Heatmat[]
    n = len(igraci)
    matrica = np.zeros((n, n))
    
    for igra_info in sve_igre:
        i_idx = next(i for i, ig in enumerate(igraci) if ig.ime == igra_info['prvi'])
        j_idx = next(j for j, ig in enumerate(igraci) if ig.ime == igra_info['drugi'])
        matrica[i_idx, j_idx] = igra_info['bodovi_prvi']
        if i_idx != j_idx:
            matrica[j_idx, i_idx] = igra_info['bodovi_drugi']
    
    im = axes[0, 1].imshow(matrica, cmap='RdYlGn', aspect='auto')
    axes[0, 1].set_xticks(range(n))
    axes[0, 1].set_yticks(range(n))
    axes[0, 1].set_xticklabels([ig.ime for ig in igraci], rotation=45, ha='right', fontsize=8)
    axes[0, 1].set_yticklabels([ig.ime for ig in igraci], fontsize=8)
    axes[0, 1].set_title('Matrica bodova (redak vs stupac)', fontsize=14, fontweight='bold')
    plt.colorbar(im, ax=axes[0, 1])
    
    # 3.kooperativnosti
    kooperativnost = {}
    for igra_info in sve_igre:
        potezi = igra_info['potezi']
        # 1 = oboje kooperirali, 2 = prvi kooperirao, 3 = drugi kooperirao, 4 = nitko
        
        prvi = igra_info['prvi']
        drugi = igra_info['drugi']
        
        if prvi not in kooperativnost:
            kooperativnost[prvi] = {'koop': 0, 'total': 0}
        if drugi not in kooperativnost:
            kooperativnost[drugi] = {'koop': 0, 'total': 0}
        
        for potez in potezi:
            kooperativnost[prvi]['total'] += 1
            kooperativnost[drugi]['total'] += 1
            
            if potez == 1:  # oboje kooperirali
                kooperativnost[prvi]['koop'] += 1
                kooperativnost[drugi]['koop'] += 1
            elif potez == 2:  # samo prvi kooperirao
                kooperativnost[prvi]['koop'] += 1
            elif potez == 3:  # samo drugi kooperirao
                kooperativnost[drugi]['koop'] += 1
    
    strategije = list(kooperativnost.keys())
    postotak_koop = [100 * kooperativnost[s]['koop'] / kooperativnost[s]['total'] 
                     for s in strategije]
    
    bars = axes[1, 0].bar(range(len(strategije)), postotak_koop, color=colors)
    axes[1, 0].set_xticks(range(len(strategije)))
    axes[1, 0].set_xticklabels(strategije, rotation=45, ha='right', fontsize=8)
    axes[1, 0].set_ylabel('Postotak kooperacije (%)', fontsize=12)
    axes[1, 0].set_title('Kooperativnost strategija', fontsize=14, fontweight='bold')
    axes[1, 0].set_ylim([0, 105])
    
    # Dodaj vrijednosti
    for i, (bar, pct) in enumerate(zip(bars, postotak_koop)):
        axes[1, 0].text(i, pct + 2, f'{pct:.1f}%', ha='center', fontsize=8)
    
    # 4. Primjer igre tft defec
    primjer_igra = next((ig for ig in sve_igre 
                        if ig['prvi'] == 'Tit for Tat' and ig['drugi'] == 'Always defect'), None)
    
    if primjer_igra:
        potezi = primjer_igra['potezi'][:50]  # Prvih 50 poteza
        
        # Mapiranje poteza u boje
        boje_poteza = []
        for p in potezi:
            if p == 1: boje_poteza.append('green')      # oboje kooperirali
            elif p == 2: boje_poteza.append('orange')   # samo prvi kooperirao
            elif p == 3: boje_poteza.append('blue')     # samo drugi kooperirao
            else: boje_poteza.append('red')             # nitko nije kooperirao
        
        axes[1, 1].scatter(range(len(potezi)), potezi, c=boje_poteza, s=30, alpha=0.7)
        axes[1, 1].set_xlabel('Runda', fontsize=12)
        axes[1, 1].set_ylabel('Tip poteza', fontsize=12)
        axes[1, 1].set_yticks([1, 2, 3, 4])
        axes[1, 1].set_yticklabels(['Oboje\nkoop.', 'Prvi\nkoop.', 'Drugi\nkoop.', 'Nitko\nne koop.'], fontsize=8)
        axes[1, 1].set_title(f'{primjer_igra["prvi"]} vs {primjer_igra["drugi"]}\n(Prvih 50 rundi)', 
                            fontsize=14, fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('tournament_results.png', dpi=300, bbox_inches='tight')
    print("\n✓ Vizualizacije spremljene u 'tournament_results.png'")
    plt.show()

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
    
    sve_igre = []

    with open('./igre.csv', 'w+', encoding='UTF-8') as output:
        output.write('#Prvi igrac;Bodovi Prvog;Drugi igrac;Bodovi drugog;Potezi\n')

        for i in range(len(igraci)):
            for j in range(i, len(protivnici)):
                potezi = igra(igraci[i], protivnici[j])
                
                # Spremi podatke za vizualizaciju
                sve_igre.append({
                    'prvi': igraci[i].ime,
                    'drugi': protivnici[j].ime,
                    'bodovi_prvi': igraci[i].bodovi,
                    'bodovi_drugi': protivnici[j].bodovi,
                    'potezi': potezi
                })
                
                output.write(f'{igraci[i].ime};{igraci[i].bodovi};{protivnici[j].ime};{protivnici[j].bodovi};{potezi}\n')

    poredak = sorted(igraci, key=lambda x: x.ukupni_bodovi, reverse=True)

    with open('./poredak.csv', 'w+', encoding='UTF-8') as output:
        output.write(f'Rank;Ime;Bodovi\n')

        print("\n===== TABLICA PORETKA =====")
        for idx, ig in enumerate(poredak, start=1):
            print(f"{idx}. {ig.ime} - {ig.ukupni_bodovi} bodovi")
            output.write(f'{idx};{ig.ime};{ig.ukupni_bodovi}\n')

    # Kreiraj vizualizacije
    print("\n===== KREIRANJE VIZUALIZACIJA =====")
    vizualiziraj_rezultate(igraci, sve_igre)