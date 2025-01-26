import json
import threading
import os
import zlib

class HashTable:
    # Initializam HashTable-ul
    def __init__(self, marime: int):
        self.marime = marime
        self.buckets = [None] * marime
        
        self.total_threads = os.cpu_count()
        self.valoare_gasita = None

        self.pasi = 0

    # Genereaza hash-ul utilizand algoritmul crc32
    def _hash(self, key: str):
        return zlib.crc32(bytes(key, encoding='utf-8')) % self.marime

    # Utilizat pentru a cauta un item in hashtable
    def __getitem__(self, key):
        key = str(key)
        i = self._hash(key)

        indice, value = self.search(key, i)

        return value

    # Utilizat pentru a adauga un element in hashtable
    def __setitem__(self, key, new_value):
        key = str(key)
        i = self._hash(key)

        if self.buckets[i] == None:
            self.buckets[i] = list()
            self.buckets[i].append([key, new_value])
        else:
            self.buckets[i].append([key, new_value])

    # Functia responsabila pentru a cauta o cheie in lista specificata
    def worker(self, lista: list, key: str, indice_value: int):
        for i in range(len(lista)):
            if lista[i][0] == key:
                self.valoare_gasita = (indice_value + i, lista[i][1])
                self.pasi = i
                break
    
    # Functia care foloseste toate thread-urile dintr-un calculator sa caute
    # in paralel cheia.
    def search(self, key: str, i: int):
        threads = list()

        self.pasi = 0
        
        # Daca bucket-ul e gol atunci nu exista acea cheie
        if self.buckets[i] == None:
            return None

        # Numarul de elemente in bucket-ul i
        num_elemente = len(self.buckets[i])

        # Daca numerul de elemente este mai mic decat numarul de thread-uri atunci folosim
        # atatea thread-uri cat sunt num_elemente in bucket-ul i
        if num_elemente <= self.total_threads:
            for t in range(num_elemente):
                # Initializam thread-urile ruland functia worker.
                threads.append(threading.Thread(target=self.worker, args=([self.buckets[i][t]], key, t)))
                # Pornim thread-urile
                threads[t].start()

            for t in range(num_elemente):
                # Asteptam pana cand toate thread-urile au finalizat cautarea
                threads[t].join()
        else:
            inceput = num_elemente // self.total_threads

            for t in range(self.total_threads):
                # Initializam thread-urile ruland functia worker.
                if t != self.total_threads - 1:
                    # La fiecare thread ii v-om da o portiune din lista aflata in bucket-ul la pozitia i
                    threads.append(threading.Thread(target=self.worker, args=(self.buckets[i][inceput * t:inceput * (t + 1)], key, inceput * t)))
                else:
                    # Daca ne aflam la ultima portiune din lista din bucket atunci v-om cauta cheia in restul elementelor
                    threads.append(threading.Thread(target=self.worker, args=(self.buckets[i][inceput * t:], key, inceput * t)))
                
                # Pornim thread-urile
                threads[t].start()

            for t in range(self.total_threads):
                # Asteptam pana cand toate thread-urile au finalizat cautarea
                threads[t].join()

        # Daca un worker gaseste cheia, ea va stoca indicele si valoarea in self.valoare_gasita
        # Daca self.valoare_gasita ramane None atunci nu s-a gasit cheia si returnam None
        if self.valoare_gasita != None:
            indice, value = self.valoare_gasita
            self.valoare_gasita = None
            return indice, value
        else:
            return None