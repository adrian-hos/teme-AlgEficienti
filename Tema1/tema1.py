import json
import itertools
import random

from hashtable import HashTable

if __name__ == '__main__':
    # Citim toate cnp-urile din fisier
    f = open('cnp.json')
    cnp = json.load(f)
    f.close()

    # Transformam dict de CNP-uri in lista
    lista_cnp = list(cnp.items())

    # Initializam un hashtable cu 1000 bucket-uri
    hasht = HashTable(1000)

    # Adaugam toate cnp-urile in hashtable
    for key, value in cnp.items():
        hasht[key] = value

    print("Adaugat!")

    lista_cauta = list()

    # Cautam 1000 cnp-uri aleatoriu din fisier in hashtable.
    # Daca toate au fost gasite atunci se printeaza un mesaj
    pasi = list()

    for i in range(1000):
        key, value = random.choice(lista_cnp)

        if hasht[key] == value:
            lista_cauta.append(True)
        else:
            lista_cauta.append(False)
        
        # Calculam avg numar de pasi
        pasi.append(hasht.pasi)


    if all(lista_cauta):
        print("Toate elementele au fost cautate corect!")
        print(f"Avg pasi: {sum(pasi) // len(pasi)}")