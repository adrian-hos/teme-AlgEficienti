import datetime
import random
import json

# Genereaza o data aleatoare utilizand intervalul de ani, de_la, pana_la.
def data_aleatoare(de_la: int, pana_la: int):
    if de_la > pana_la:
        de_la, pana_la = pana_la, de_la
    
    an = random.randint(de_la, pana_la)
    luna = random.randint(1, 12)

    match luna:
        case 1:
            zi = random.randint(1, 31)
        case 2:
            if an % 4 == 0 and (an % 100 != 0 or an % 400 == 0):
                zi = random.randint(1, 29)
            else:
                zi = random.randint(1, 28)
        case 3:
            zi = random.randint(1, 31)
        case 4:
            zi = random.randint(1, 30)
        case 5:
            zi = random.randint(1, 31)
        case 6:
            zi = random.randint(1, 30)
        case 7:
            zi = random.randint(1, 31)
        case 8:
            zi = random.randint(1, 31)
        case 9:
            zi = random.randint(1, 30)
        case 10:
            zi = random.randint(1, 31)
        case 11:
            zi = random.randint(1, 30)
        case 12:
            zi = random.randint(1, 31)

    return zi, luna, an

# Genereaza un CNP
def generator_cnp(este_masc: bool, zi: int, luna: int, an: int, cod_judet: str, nnn: int):
    # S
    if este_masc:
        if an >= 2000 and an <= 2099:
            s = "5"
        elif an >= 1900 and an <= 1999:
            s = "1"
        elif an >= 1800 and an <= 1899:
            s = "3"
    else:
        if an >= 2000 and an <= 2099:
            s = "6"
        elif an >= 1900 and an <= 1999:
            s = "2"
        elif an >= 1800 and an <= 1899:
            s = "4"

    # AA
    aa = str(an)[2:]

    # LL
    if luna <= 9:
        ll = "0" + str(luna)
    else:
        ll = str(luna)

    # ZZ
    if zi <= 9:
        zz = "0" + str(zi)
    else:
        zz = str(zi)

    # JJ
    jj = str(cod_judet)

    # NNN
    if nnn <= 9:
        nnn = "00" + str(nnn)
    elif nnn <= 99:
        nnn = "0" + str(nnn)
    else:
        nnn = str(nnn)

    # C
    constanta = "279146358279"
    cnp = s + aa + ll + zz + jj + nnn
    suma = 0

    for i in range(0, 12):
        suma += int(cnp[i]) * int(constanta[i])

    c = suma % 11

    if c == 10:
        c = 1

    cnp = cnp + str(c)

    return cnp

# Genereaza un CNP aleatoriu
def generator_cnp_random(de_la: int, pana_la: int, este_masc: bool, cod_judet: str):
    # Alege o data random in intervalul specificat
    zi, luna, an = data_aleatoare(de_la, pana_la)

    nnn = random.randint(0, 999)

    return generator_cnp(este_masc, zi, luna, an, cod_judet, nnn)

def generator_cnp_statistici(nr_cnp: int):
    # Citim statisticile
    f = open('statistici.json')
    statistici = json.load(f)
    f.close()

    # Citim prenume masculin
    f = open('firstnames_m.json')
    prenume_m = json.load(f)
    f.close()

    # Citim prenume feminin
    f = open('firstnames_f.json')
    prenume_f = json.load(f)
    f.close()

    # Citim nume de familie
    f = open('surnames.json')
    nume = json.load(f)
    f.close()

    # Intervalul de varste
    varste = [
        [2024, 2019], 
        [2018, 2013], 
        [2012, 2007], 
        [2006, 2001], 
        [2000, 1995], 
        [1994, 1989], 
        [1988, 1983], 
        [1982, 1977], 
        [1976, 1971], 
        [1970, 1965], 
        [1964, 1959], 
        [1958, 1953], 
        [1952, 1947], 
        [1946, 1941], 
        [1940, 1935], 
        [1934, 1929], 
        [1928, 1923], 
        [1922, 1917]
        ]

    # Impartim nr_cnp pe judete
    jud_chei = list(statistici)
    ultima_cheie = jud_chei[-1]
    suma_pop = 0
    cnp_dict = dict()

    # Calculam populatia fiecarui judet
    for key, value in statistici.items():
        if key != ultima_cheie:
            pop_jud = int(round(nr_cnp * value["dupa_total"] / 100, 0))
            suma_pop += pop_jud
        else:
            pop_jud = nr_cnp - suma_pop

        cod_judet = value["cod"]

        if isinstance(cod_judet, list):
            cod_judet = random.choice(cod_judet)

        # Impartim populatia judetelor pe sex masculin si feminin
        pop_mas = int(round(pop_jud * value["mas"] / 100, 0))
        pop_fem = pop_jud - pop_mas

        suma_pop_varste = 0

        # Impartim populatia sexului masculin pe grupe de varste
        for v in range(0, 18):
            varsta = varste[v]
            if v != 17:
                # Aflam populatia pentru o anumita grupa de varste
                pop_varsta = int(round(pop_mas * value["varste"][v] / 100, 0))
                suma_pop_varste += pop_varsta
            else:
                pop_varsta = pop_mas - suma_pop_varste

            for i_cnp in range(pop_varsta):
                # Generam CNP dupa criteriile persoanei
                cnp = generator_cnp_random(varsta[1], varsta[0], True, cod_judet)

                while(cnp in cnp_dict):
                    cnp = generator_cnp_random(varsta[1], varsta[0], True, cod_judet)

                cnp_dict[cnp] = random.choice(nume) + " " + random.choice(prenume_m)

        suma_pop_varste = 0

        # Impartim populatia sexului feminin pe grupe de varste
        for v in range(0, 18):
            varsta = varste[v]
            if v != 17:
                # Aflam populatia pentru o anumita grupa de varste
                pop_varsta = int(round(pop_fem * value["varste"][v] / 100, 0))
                suma_pop_varste += pop_varsta
            else:
                pop_varsta = pop_fem - suma_pop_varste

            for i_cnp in range(pop_varsta):
                # Generam CNP dupa criteriile persoanei
                cnp = generator_cnp_random(varsta[1], varsta[0], False, cod_judet)

                while(cnp in cnp_dict):
                    cnp = generator_cnp_random(varsta[1], varsta[0], False, cod_judet)

                cnp_dict[cnp] = random.choice(nume) + " " + random.choice(prenume_f)

    # Luam CNP-urile din dictionar, le punem in lista si le amestecam aleatoriu
    # dupa care le punem inapoi in dictionar
    cnp_dict_random = list(cnp_dict.items())
    random.shuffle(cnp_dict_random)
    cnp_dict_random = dict(cnp_dict_random)

    # Scriem CNP-urile in fisier.
    with open('cnp.json', 'w') as f:
        json.dump(cnp_dict_random, f, indent=4)

generator_cnp_statistici(1000000)