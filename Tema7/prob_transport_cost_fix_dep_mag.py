import json
from itertools import repeat
import time
import matplotlib.pyplot as plt

# d - nr_dep
# r - nr_mag
# SCj - cap depozite
# Dk - cereri

class transport_min_pe_mat:
    def __init__(self, d, r, SCj, costuri_fixe_dep, Dk, costuri, costuri_fixe_mag):
        self.d = d
        self.r = r
        self.SCj = SCj
        self.Dk = Dk
        self.costuri = costuri
        self.costuri_fixe_dep = costuri_fixe_dep
        self.costuri_fixe_mag = costuri_fixe_mag

        self.num_costuri = d * r
        self.item_transportate = [[0 for i in repeat(None, self.r)] for i in repeat(None, self.d)]

        self.pasi = 0
        self.cost_total = 0

    def rezultat(self):
        cereri_indeplinite = 0
        
        # Resetam variabilele
        self.item_transportate = [[0 for i in repeat(None, self.r)] for i in repeat(None, self.d)]
        self.pasi = 0
        self.cost_total = 0        

        # Aflam d * r costuri minime
        for cost_min_i in range(self.num_costuri):
            # Daca am indeplinit toate cererile, incheiem for-ul devreme
            if cereri_indeplinite == self.r:
                break

            cost_min = None
            cost_min_pos = list()

            # Luam fiecare cost si vedem care este cel mai mic
            for dep_i in range(self.d):
                for mag_i in range(self.r):
                    cost = self.calculeaza_cost(dep_i, mag_i)

                    # Daca primim un cost atunci il comparam cu cost_min
                    if cost:
                        if cost_min == None or cost < cost_min:
                            cost_min = cost
                            cost_min_pos = (dep_i, mag_i)

            # Daca cost_min returneaza o valoare atunci am gasit un cost minim
            if cost_min:
                # Adunam cost_min la costul total pentru statistici
                self.cost_total += cost_min
                num_item = min(self.SCj[cost_min_pos[0]], self.Dk[cost_min_pos[1]])
                # Xjk
                self.item_transportate[cost_min_pos[0]][cost_min_pos[1]] = num_item

                # Daca num_item este egal cu cererea magazinului inseamna ca am indeplinit cererea acestui magazin
                if num_item == self.Dk[cost_min_pos[1]]:
                    cereri_indeplinite += 1

                # Reducem din SCj si Dk itemele transportate
                self.SCj[cost_min_pos[0]] -= num_item
                self.Dk[cost_min_pos[1]] -= num_item
                
                # Setam costul ca fiind None pentru ca sa nu mai fie folosit
                self.costuri[cost_min_pos[0]][cost_min_pos[1]] = None

                # Setam costul fix la depozit la 0 daca a fost folosit depozitul de catre un magazin
                self.costuri_fixe_dep[cost_min_pos[0]] = 0
            else:
                break

        if cereri_indeplinite == self.r:
            finalizat = True
        else:
            finalizat = False

        print(cereri_indeplinite)

        return (finalizat, self.cost_total, self.pasi, self.item_transportate, self.SCj, self.Dk)

    def calculeaza_cost(self, dep_i, mag_i):
        # Verificam prima data, daca cumva depozitul a fost epuizat, daca cererea a fost indeplinita
        # sau daca costul este None (in cazul in care am terminat cu el inainte)
        # iar daca da returnam None
        if self.SCj[dep_i] == 0 or self.Dk[mag_i] == 0 or self.costuri[dep_i][mag_i] == None:
            return None
        
        # min(item_in_depozit, cerere) * cost + cost_fix_magazin
        cost = min(self.SCj[dep_i], self.Dk[mag_i]) * self.costuri[dep_i][mag_i] + self.costuri_fixe_mag[dep_i][mag_i] + self.costuri_fixe_dep[dep_i]

        self.pasi += 1

        return cost

if __name__ == '__main__': 
    afisare_item_transportate = True

    f = open("Lab_FCD_FCR_instances.json")
    data = json.load(f)
    f.close()

    date_finale = dict()

    lista_costuri = list()

    for key, item in data.items():
        alg = None

        print('')

        print(f"Instance: {key}")

        start = time.time()
        alg = transport_min_pe_mat(item['d'], item['r'], item['SCj'], item['costuri_fixe_dep'], item['Dk'], item['costuri'], item['costuri_fixe_mag'])
        finalizat, cost, nr_pasi, Xjk, Uj, Dk = alg.rezultat()
        end = time.time()

        timp = end - start

        # Printam datele
        print(f"Cost: {cost}")
        print(f"Pasi: {nr_pasi}")
        print(f"Timp: {timp:.8f}")
        print(f"Finalizat: {finalizat}")

        # Stocam statisticile in dictionar
        date_finale[key] = dict()
        date_finale[key]["Xjk"] = Xjk
        date_finale[key]["Uj"] = Uj
        date_finale[key]["Dk"] = Dk
        date_finale[key]["cost"] = cost
        date_finale[key]["nr_pasi"] = nr_pasi
        date_finale[key]["timp"] = timp
        date_finale[key]["finalizat"] = finalizat

        # Daca afisare_item_transportate este true atunci afisam si tabelul cu iteme transportate
        if afisare_item_transportate:
            for i in range(len(Xjk)):
                print(Xjk[i])

        lista_costuri.append(cost)

    # Salvam datele
    with open('rezultate.json', 'w') as f:
        json.dump(date_finale, f, indent=4)

    plt.plot(range(len(lista_costuri)), lista_costuri,'bo-')

    for x,y in zip(range(len(lista_costuri)), lista_costuri):
        label = str(y)

        plt.annotate(label, (x,y), textcoords="offset points", xytext=(0,20), ha='center')

    date_optime = [15497, 10251, 9546, 52483, 59361, 46886, 135560, 153334, 153032]
    date_optime_pos = [0, 1, 2, 25, 26, 27, 50, 51, 52]

    for i in range(len(date_optime)):
        x = date_optime_pos[i]
        y = date_optime[i]

        plt.plot(x, y, "or")

        proc = (lista_costuri[x] - y) / y * 100

        label = str(y) + " (~ {:.2f}%)".format(proc)
        plt.annotate(label, (x, y), textcoords="offset points", xytext=(0,-20), ha='center')

    plt.show()