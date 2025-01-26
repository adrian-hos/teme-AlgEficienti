import json
from itertools import repeat
import time

# Functie simpla care afla minimul intr-o lista
# ignorand elementul none
def min_num(lista):
    _min_num = None
    _min_i = None

    for i in range(len(lista)):
        if lista[i] != None:
            _min_num = lista[i]
            _min_i = i
            break
    
    for i in range(len(lista)):
        if lista[i] != None and lista[i] < _min_num:
            _min_num = lista[i]
            _min_i = i

    return _min_i, _min_num


def transport_min_pe_linie(num_depozit, num_magazine, capacitate_depozite, cereri, costuri):
    # Generam tabelul in care v-om stoca numarul de iteme transportate
    item_transportate = [[0 for i in repeat(None, num_magazine)] for i in repeat(None, num_depozit)]

    cost = 0

    l = 0

    pasi = 0

    # Retinem costurile pentru prima linie
    linie = costuri[l]

    # Iteram prin prima linie pentru a calcula numarul de iteme luate
    # Linia 1 este luata separat deoarace toate valorile sunt luate in considerare
    # (Nu se anuleaza coloane ca si la liniile urmatoare)
    for c in range(num_magazine):
        i, num = min_num(linie)
        # Setam costul ca None ca sa marcam faptul ca am trecut prin acest cost
        linie[i] = None

        # Calculam numarul de iteme pe care sa le scadem
        cap_curnt = capacitate_depozite[l]
        cer_curnt = cereri[i]
        min_cap_cer = min(cap_curnt, cer_curnt)
        
        # Reducem numarul de iteme din capacitate depozit
        # si cerere
        capacitate_depozite[l] -= min_cap_cer
        cereri[i] -= min_cap_cer

        # Retinem cate iteme am transportat pe un drum
        item_transportate[l][i] = min_cap_cer

        # Retinem costul itemelor
        cost += min_cap_cer * num

        # Adaugam un pas
        pasi += 1

    # Daca cumva toate cererile au fost indeplinite (adica sunt 0), atunci returnam valorile
    if not any(cereri):
        return cost, pasi, True, item_transportate

    # Iteram la fel prin costuri ca si la linia unu
    # dar acum verificam daca cumva ceva cerere a fost indeplinita
    # iar daca da, o setam ca fiind "None"
    for l in range(1, num_depozit):
        linie = list()
        num_costuri = 0

        for i in range(len(costuri[l])):
            if cereri[i] == 0:
                linie.append(None)
            else:
                linie.append(costuri[l][i])
                num_costuri += 1

        # Aici v-om intera toate costurile
        for c in range(num_costuri):
            i, num = min_num(linie)

            linie[i] = None

            cap_curnt = capacitate_depozite[l]
            cer_curnt = cereri[i]
            min_cap_cer = min(cap_curnt, cer_curnt)

            capacitate_depozite[l] -= min_cap_cer
            cereri[i] -= min_cap_cer

            item_transportate[l][i] = min_cap_cer

            cost += min_cap_cer * num

            pasi += 1

            # Daca cumva toate cererile au fost indeplinite (adica sunt 0), atunci returnam valorile
            if not any(cereri):
                return cost, pasi, True, item_transportate

    return cost, pasi, False, item_transportate

if __name__ == '__main__':
    afisare_item_transportate = False

    # Citim totate instantele din fisier
    f = open("Lab_simple_instances.json")
    data = json.load(f)
    f.close()

    date_finale = dict()

    for key, item in data.items():
        print('')

        print(f"Instance: {key}")

        # Calculam timpul de executare
        start = time.time()
        cost, pasi, finalizat, item_transportate = transport_min_pe_linie(item["d"], item["r"], item["SCj"], item["Dk"], item["costuri"])
        end = time.time()

        timp = end - start

        # Printam datele
        print(f"Cost: {cost}")
        print(f"Pasi: {pasi}")
        print(f"Timp: {timp:.8f}")
        print(f"Finalizat: {finalizat}")

        # Stocam statisticile in dictionar
        date_finale[key] = dict()
        date_finale[key]["cost"] = cost
        date_finale[key]["pasi"] = pasi
        date_finale[key]["timp"] = timp
        date_finale[key]["finalizat"] = finalizat
        date_finale[key]["item_transportate"] = item_transportate
        
        # Daca afisare_item_transportate este true atunci afisam si tabelul cu iteme transportate
        if afisare_item_transportate:
            for i in range(len(item_transportate)):
                print(item_transportate[i])

    # Salvam datele
    with open('rezultate.json', 'w') as f:
        json.dump(date_finale, f, indent=4)

