from PIL import Image

# B5

def ascunde(cale_gazda, mesaj, cale_iesire="stego.png"):
    img = Image.open(cale_gazda).convert("RGB")
    canale = [c for px in img.getdata() for c in px]       # r,g,b,r,g,b,...
    biti = "".join(f"{x:08b}" for x in mesaj + b"\x00")    # \x00 = sfarsit de mesaj

    if len(biti) > len(canale):
        raise ValueError("Mesaj prea lung!")

    for i, bit in enumerate(biti):
        canale[i] = (canale[i] & ~1) | int(bit)

    px_nou = [tuple(canale[i:i + 3]) for i in range(0, len(canale), 3)]
    img.putdata(px_nou)
    img.save(cale_iesire)

# B6

def dezvaluie(cale):
    img = Image.open(cale).convert("RGB")
    canale = [c for px in img.getdata() for c in px]

    biti = "".join(str(c & 1) for c in canale)

    octeti = bytearray()
    for i in range(0, len(biti) - 7, 8):
        octet = int(biti[i:i + 8], 2)
        if octet == 0:
            break
        octeti.append(octet)
    return octeti.decode()
