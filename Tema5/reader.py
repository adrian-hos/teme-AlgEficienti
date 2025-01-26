import json
from pathlib import Path
import sys
import ast

data = dict()

tipuri = ["small", "medium", "large"]

for tip in tipuri:
    for i in range(1, 26):
        if i < 10:
            num = "0" + str(i)
        else:
            num = i

        loc = Path(sys.path[0] + "/Lab_FCR_instances/" + f"Lab01_FCR_{tip}_{num}.dat")

        print(loc)

        txt = loc.read_text()
        txt = txt.replace("\n", "")

        # Nume
        j = txt.find("instance_name = ")
        txt = txt.replace("instance_name = \"", "")
        c = txt[j]

        nume = ""

        while c != '"':
            nume += c
            j += 1
            c = txt[j]

        # Numar depozite
        j = txt.find("d = ")
        txt = txt.replace("d = ", "")
        c = txt[j]

        num_d = ""

        while c != ';':
            num_d += c
            j += 1
            c = txt[j]

        num_d = int(num_d)

        # Numar magazine
        j = txt.find("r = ")
        txt = txt.replace("r = ", "")
        c = txt[j]

        num_r = ""

        while c != ';':
            num_r += c
            j += 1
            c = txt[j]

        num_r = int(num_r)

        # Capacitate depozite
        j = txt.find("SCj = ")
        txt = txt.replace("SCj = ", "")
        c = txt[j]

        cap_d = ""

        while c != ';':
            cap_d += c
            j += 1
            c = txt[j]

        cap_d = cap_d.replace(" ", ", ")
        cap_d = ast.literal_eval(cap_d)

        # Cerere magazine
        j = txt.find("Dk = ")
        txt = txt.replace("Dk = ", "")
        c = txt[j]

        cer_m = ""

        while c != ';':
            cer_m += c
            j += 1
            c = txt[j]

        cer_m = cer_m.replace(" ", ", ")
        cer_m = ast.literal_eval(cer_m)

        # Costuri
        j = txt.find("Cjk = ")
        txt = txt.replace("Cjk = ", "")
        c = txt[j]

        costuri = ""

        while c != ';':
            costuri += c
            j += 1
            c = txt[j]

        costuri = costuri.replace("  ", " ")
        costuri = costuri.replace(" ", ", ")
        costuri = ast.literal_eval(costuri)

        # Costuri fixe magazin
        j = txt.find("Fjk = ")
        txt = txt.replace("Fjk = ", "")
        c = txt[j]

        costuri_fixe_mag = ""

        while c != ';':
            costuri_fixe_mag += c
            j += 1
            c = txt[j]

        costuri_fixe_mag = costuri_fixe_mag.replace("  ", " ")
        costuri_fixe_mag = costuri_fixe_mag.replace(" ", ", ")
        costuri_fixe_mag = costuri_fixe_mag.replace("[,", "[")
        costuri_fixe_mag = ast.literal_eval(costuri_fixe_mag)

        data[nume] = dict()
        data[nume]["d"] = num_d
        data[nume]["r"] = num_r
        data[nume]["SCj"] = cap_d
        data[nume]["Dk"] = cer_m
        data[nume]["costuri"] = costuri
        data[nume]["costuri_fixe_mag"] = costuri_fixe_mag

with open('Lab_FCR_instances.json', 'w') as f:
    json.dump(data, f, indent=4)

