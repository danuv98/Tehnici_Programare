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
# print(len(suid), "SUID,", len(mari), "cu risc mare")
# print(sorted(c["nume"] for c in mari))


# A4

def sudo_constatari(cale):
    out = []
    
    for ln in citeste_linii(cale):
        user, drept = ln.split(" : ", 1)
    
        out.append({
            "user": user.strip(),
            "drept": drept.strip(),
            "risc": "mare" if "NOPASSWD" in drept else "normal"
        })

    return out


def cron_constatari(cale):
    out = []

    for ln in citeste_linii(cale):
        campuri = ln.split()
        user = campuri[5]
        comanda = " ".join(campuri[6:])

        out.append({
            "user": user,
            "comanda": comanda
        })

    return out

def enumereaza(d):
    return {
        "suid": suid_constatari(os.path.join(d, "suid.txt")),
        "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
        "cron": cron_constatari(os.path.join(d, "crontab.txt"))
    }


# raport = enumereaza("arsenal/privesc/start")

# for categorie, lista in raport.items():
#    print(categorie, len(lista))


# A5

def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    raport = enumereaza(a.capturi)

    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return

    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")

    utilizatori = (
        {c["user"] for c in raport["sudo"]}
        | {c["user"] for c in raport["cron"]}
    )

    with open("enum.json", "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)

    print("Raport salvat in enum.json")


if __name__ == "__main__":
    main()
