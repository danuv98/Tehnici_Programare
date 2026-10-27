import re
import base64
from urllib.parse import unquote


# A1

s = "danu"
b = s.encode()

# print(b, b[0])
# print(b.hex())
# print(bytes.fromhex(b.hex()))

# A2

def ghici_strat(s):
    if re.search(r"%[0-9A-Fa-f]{2}", s):
        return "url"

    if len(s) % 2 == 0 and re.fullmatch(r"[0-9A-Fa-f]+", s):
        return "hex"

    if len(s) % 4 == 0 and re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s):
        return "base64"

    return "necunoscut"


# print(ghici_strat("%2Fetc"))
# print(ghici_strat("48656c6c6f"))
# print(ghici_strat("U2FsdXQ="))


# A3

def desfa(s):
    strat = ghici_strat(s)

    if strat == "base64":
        rezultat = base64.b64decode(s)

    elif strat == "hex":
        rezultat = bytes.fromhex(s)

    elif strat == "url":
        rezultat = unquote(s).encode()

    else:
        rezultat = s.encode()

    return strat, rezultat


# print(desfa("U2FsdXQ="))
# print(desfa("48656c6c6f"))
# print(desfa("%2Fetc"))


# A4

def citibil(b):
    return all(32 <= c < 127 for c in b)


val = "NTM1OTU3NTk="

for _ in range(8):
    strat = ghici_strat(val)

    if strat == "necunoscut":
        break

    strat, b = desfa(val)

    if not citibil(b):
        break

    val = b.decode()

# print(val)


# A5

date = open("probe/xor.bin", "rb").read()

def sparge_xor(date):
    gasite = []
    for k in range(256):
        clar = bytes(b ^ k for b in date)
        if citibil(clar):
            gasite.append((k, clar.decode()))
    return gasite


# --------- FLAG{xor_un_octet} ------------


# A6

import hashlib
tinta = open("probe/hashuri.txt").readline().strip()
def sparge_hash(tinta, cale_wordlist="probe/wordlist.txt"):
    for cuv in open(cale_wordlist, encoding="latin1"):
        cuv = cuv.strip()
        if hashlib.md5(cuv.encode()).hexdigest() == tinta:
            return cuv
    return None

# 32
# gasit: password


# A7

import argparse
import json

def desfa_straturi(val, max_pasi=8):
    straturi = []
    for _ in range(max_pasi):
        if ghici_strat(val) == "necunoscut":
            break
        strat, b = desfa(val)
        if not citibil(b):
            break
        straturi.append(strat)
        val = b.decode()
    return straturi, val

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("intrare")
    p.add_argument("--fisier", action="store_true")
    a = p.parse_args()

    if a.fisier:
        val = open(a.intrare, "rb").read().decode().strip()
    else:
        val = a.intrare

    straturi, rezultat = desfa_straturi(val)
    print(straturi, rezultat)

    fisa = {"strat": straturi, "rezultat": rezultat}
    json.dump(fisa, open("arsenal/forensics/fisa.json", "w"), indent=2)

# {
#   "strat": [
#     "base64",
#     "base64",
#     "hex"
#   ],
#   "rezultat": "FLAG{straturi_de_encoding}"
# }
