from random import randrange
import json
import os
from pathlib import Path

class cromozom:
    def __init__(self, lista_obiecte: list, greutate_max: int, crom: str|None = None) -> None:
        self.lista_obiecte = lista_obiecte
        self.lungime = len(lista_obiecte[0])
        self.greutate_max = greutate_max
        
        if crom:
            if self.este_valid(crom):
                self._crom = crom
            else:
                self._crom = self.corecteaza_cromozom(crom)
        else:
            self._crom = self.genereaza_cromozom()

    def este_valid(self, crom: str|None = None) -> bool:
        if len(crom) != self.lungime:
            return False

        greutate = 0

        if not crom:
            crom = self._crom

        for i in range(0, self.lungime):
            if crom[i] == '1':
                greutate += lista_obiecte[0][i]
        
        if greutate <= self.greutate_max:
            return True
        else:
            return False
    
    def corecteaza_cromozom(self, crom: str|None = None) -> str:
        while not self.este_valid(crom):
            i =  randrange(self.lungime)

            if crom[i] == '1':
                crom = crom[:i] + '0' + crom[i+1:]
        
        return crom

    def genereaza_cromozom(self) -> str:
        crom = ""

        for i in range(0, self.lungime):
            crom += str(randrange(2))
        
        return self.corecteaza_cromozom(crom)

    @property
    def crom(self) -> str:
        return self._crom

    @property
    def valoare(self) -> int:
        val = 0

        for i in range(0, self.lungime):
            if self._crom[i] == '1':
                val += self.lista_obiecte[1][i]
        
        return val
    
    @property
    def greutate(self) -> int:
        val = 0

        for i in range(0, self.lungime):
            if self._crom[i] == '1':
                val += self.lista_obiecte[0][i]
        
        return val

class populatie:
    def __init__(self, lista_obiecte: list, greutate_max: int, nr_pop: int, proc_cross: int, proc_elitism: int):
        self.lista_obiecte = lista_obiecte
        self.lungime = len(lista_obiecte[0])
        self.greutate_max = greutate_max
        self.nr_pop = nr_pop

        self.proc_cross = proc_cross
        self.proc_elitism = proc_elitism

        self.populatie = list()
        self.genereaza_populatie()

    def genereaza_populatie(self) -> None:
        for i in range(nr_pop):
            self.populatie.append(cromozom(self.lista_obiecte, self.greutate_max))
    
    @property
    def scor_pop(self) -> int:
        scor = 0

        for i in range(nr_pop):
            scor += self.populatie[i].valoare
        
        return scor

    def crossover(self) -> cromozom:
        i_crom1 = randrange(nr_pop)
        crom1 = self.populatie[i_crom1]
        
        i_crom2 = randrange(nr_pop)
        crom2 = self.populatie[i_crom2]
        
        i_crom3 = randrange(nr_pop)
        crom3 = self.populatie[i_crom3]
        
        best = crom1
        if crom2.valoare <= best.valoare and crom2.valoare >= crom3.valoare:
            second_best = crom2
        else:
            second_best = crom3

        if crom2.valoare >= best.valoare:
            second_best = best
            best = crom2
        
        if crom3.valoare >= best.valoare:
            second_best = best
            best = crom3
        
        punct_de_taiere = randrange(1, self.lungime)

        return cromozom(self.lista_obiecte, self.greutate_max, best.crom[:punct_de_taiere] + second_best.crom[punct_de_taiere:])
    
    def elitism(self) -> cromozom:
        i_crom1 = randrange(nr_pop)
        crom1 = self.populatie[i_crom1]
        
        i_crom2 = randrange(nr_pop)
        crom2 = self.populatie[i_crom2]
        
        i_crom3 = randrange(nr_pop)
        crom3 = self.populatie[i_crom3]
        
        if crom1.valoare >= crom2.valoare and crom1.valoare >= crom3.valoare:
            return crom1
        elif crom2.valoare >= crom1.valoare and crom2.valoare >= crom3.valoare:
            return crom2
        elif crom3.valoare >= crom1.valoare and crom3.valoare >= crom2.valoare:
            return crom3

    def mutatie(self) -> cromozom:
        i_crom1 = randrange(nr_pop)
        crom1 = self.populatie[i_crom1]
        
        i_crom2 = randrange(nr_pop)
        crom2 = self.populatie[i_crom2]
        
        i_crom3 = randrange(nr_pop)
        crom3 = self.populatie[i_crom3]

        best = crom1

        if crom2.valoare >= best.valoare:
            best = crom2
        
        if crom3.valoare >= best.valoare:
            best = crom3

        i_mutatie = randrange(0, self.lungime)

        if best.crom[i_mutatie] == '1':
            return cromozom(self.lista_obiecte, self.greutate_max, best.crom[:i_mutatie] + '0' + best.crom[i_mutatie+1:])
        else:
            return cromozom(self.lista_obiecte, self.greutate_max, best.crom[:i_mutatie] + '1' + best.crom[i_mutatie+1:])

    def urm_generatie(self) -> None:
        populatie_noua = list()

        nr_pop_cross = (self.proc_cross // 100) * self.nr_pop
        nr_pop_elitism = (self.proc_elitism // 100) * self.nr_pop
        nr_pop_mutatie = self.nr_pop - nr_pop_cross - nr_pop_elitism

        for i in range(nr_pop_cross):
            populatie_noua.append(self.crossover())

        for i in range(nr_pop_elitism):
            populatie_noua.append(self.elitism())
        
        for i in range(nr_pop_mutatie):
            populatie_noua.append(self.mutatie())
        
        self.populatie = populatie_noua

if __name__ == "__main__":
    greutate_max = 30
    lista_obiecte = [
        [3, 4, 10, 2, 9, 1, 8, 4, 2, 6],
        [20, 34, 10, 3, 50, 3, 15, 23, 31, 45]
    ]
    nr_pop = 1000
    proc_cross = 80
    proc_elitism = 15
    stagnare_limit = 10

    pop = populatie(lista_obiecte, greutate_max, nr_pop, proc_cross, proc_elitism)
    scor = pop.scor_pop
    print(f"Gen 1: {scor}")
    prev_scor = scor
    stagnare = 0

    for i in range(1, 101):
        pop.urm_generatie()
        scor = pop.scor_pop

        diff_procent = round((abs(scor - prev_scor)/((scor + prev_scor)/2)) * 100, 3)

        if diff_procent < 2:
            stagnare += 1

        print(f"Gen {i}: {scor}, diff ~{diff_procent}")
        prev_scor = scor

        if stagnare >= stagnare_limit:
            lista_cromozomi = dict()
            lista_cromozomi["scor"] = scor
            lista_cromozomi["populatie"] = dict()
            for crom in pop.populatie:
                lista_cromozomi["populatie"][crom.crom] = dict()
                lista_cromozomi["populatie"][crom.crom]["valoare"] = crom.valoare
                lista_cromozomi["populatie"][crom.crom]["greutate"] = crom.greutate
            with open(Path(os.path.dirname(os.path.realpath(__file__)), f"gen_{i}.json"), 'w') as f:
                json.dump(lista_cromozomi, f, indent=4)
            break
        