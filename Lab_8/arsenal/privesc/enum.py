import argparse, json, os
 

# A1

def citeste_linii(cale):
    ''' Intoarce lista liniilor .strip(), fara cele goale si fara cele cu # '''
    with open(cale, encoding="utf-8") as f:
        return [
            linie.strip()
            for linie in f
            if linie.strip() and not linie.strip().startswith("#")
        ]
        
# cai = citeste_linii("arsenal/privesc/start/suid.txt")
# print("linii SUID:", len(cai))


# A2

def nume(cale):
    ''' intoarce ce e dupa ultimul "/" '''  
    return cale.rsplit("/" , 1)[-1]

# nume_unice = {nume(c) for c in cai}    
# print("SUID distincte:", len(nume_unice))


# A3

GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash",
        "less", "awk", "python3", "perl"}
 
def suid_constatari(cale):
    cai = citeste_linii(cale)
    rezultat = []
    ''' for every unique path , in sorted order , dict cale/risc '''
    
    for c in sorted(set(cai)):
        rezultat.append({
            "cale": c,
            "nume": nume(c),
            "risc": "mare" if nume(c) in GTFO else "normal"
        })
    
    return rezultat

 
suid = suid_constatari("arsenal/privesc/start/suid.txt")
mari = [c for c in suid if c["risc"] == "mare"]
print(len(suid), "SUID,", len(mari), "cu risc mare")
print(sorted(c["nume"] for c in mari))
