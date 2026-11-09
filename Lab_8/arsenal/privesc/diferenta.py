
# A1

from arsenal.privesc.enum import citeste_linii

def cai(fisier):
    return set(citeste_linii(fisier))

baza = cai("arsenal/privesc/start/baza_suid.txt")
acum = cai("arsenal/privesc/start/suid.txt")

# print("baza:", len(baza), " acum:", len(acum))


# A2

noi = acum - baza
print(len(noi), "SUID noi fata de sistemul curat")
for c in sorted(noi):
    print(" ", c)


# A3

from arsenal.privesc.enum import nume, GTFO
 
risc = {nume(c): ("mare" if nume(c) in GTFO else "normal") for c in noi}
periculoase = [c for c in sorted(noi) if nume(c) in GTFO]
print("periculoase NOI:", periculoase)


# A4

def test_doar_ce_e_nou():
    acum = {"a", "b", "c"}
    baza = {"a", "b"}
    assert acum - baza == {"c"}
