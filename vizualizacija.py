import matplotlib.pyplot as plt
import numpy as np

def vizualiziraj_rezultate(poredak, sve_igre, directory = './output') -> None:

    
    # 1. Grafikon konačnog poretka
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Poredak igrača
    imena = [ig.ime for ig in poredak]
    bodovi = [ig.ukupni_bodovi for ig in poredak]
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(imena)))
    bars = axes[0, 0].barh(imena, bodovi, color=colors)
    axes[0, 0].set_xlabel('Ukupni bodovi', fontsize=12)
    axes[0, 0].set_title('Konačni poredak strategija', fontsize=14, fontweight='bold')
    axes[0, 0].invert_yaxis()
    

    
    # Heatmat[]
    n = len(poredak)
    matrica = np.zeros((n, n))
    
    for igra_info in sve_igre:
        i_idx = next(i for i, ig in enumerate(poredak) if ig.ime == igra_info['prvi'])
        j_idx = next(j for j, ig in enumerate(poredak) if ig.ime == igra_info['drugi'])
        matrica[i_idx, j_idx] = igra_info['bodovi_prvi']
        if i_idx != j_idx:
            matrica[j_idx, i_idx] = igra_info['bodovi_drugi']
    
    im = axes[0, 1].imshow(matrica, cmap='RdYlGn', aspect='auto')
    axes[0, 1].set_xticks(range(n))
    axes[0, 1].set_yticks(range(n))
    axes[0, 1].set_xticklabels([ig.ime for ig in poredak], rotation=45, ha='right', fontsize=8)
    axes[0, 1].set_yticklabels([ig.ime for ig in poredak], fontsize=8)
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
    plt.savefig(f'{directory}/tournament_results.png', dpi=300, bbox_inches='tight')
    print("\n✓ Vizualizacije spremljene u 'tournament_results.png'")
    plt.show()