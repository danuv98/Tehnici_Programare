import re
from PIL import Image
from PIL.ExifTags import TAGS
import zipfile

# B1

def tip_real(cale):
    cap = open(cale, "rb").read(8)
    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\xff\xd8"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "jpeg"
    return cap.hex()


# B2

# date = open("probe/ascuns.png", "rb").read()
# for m in re.findall(rb"[ -~]{4,}", date):
#     print(m.decode())

# FLAG{ascuns_prin_carving}


# B3

def arata_exif(cale):
    exif = Image.open(cale)._getexif() or {}
    for id, val in exif.items():
        print(TAGS.get(id, id), "=", val)


def dms_in_zecimal(dms, emisfera):
    grade, minute, secunde = dms
    zecimal = float(grade) + float(minute) / 60 + float(secunde) / 3600
    if emisfera in ("S", "W"):
        zecimal = -zecimal
    return zecimal

def gps_zecimal(cale):
    exif = Image.open(cale)._getexif() or {}
    gps = exif.get(34853)
    if not gps:
        return None
    lat = dms_in_zecimal(gps[2], gps[1])
    lon = dms_in_zecimal(gps[4], gps[3])
    return (lat, lon)

 # if __name__ == "__main__":
 #     print(gps_zecimal("probe/foto.jpg"))

# B4

def carve_zip(cale, iesire="gasit.zip"):
    date = open(cale, "rb").read()
    i = date.find(b"PK\x03\x04")
    if i == -1:
        return i
    open(iesire, "wb").write(date[i:])
    return i



if __name__ == "__main__":
    poz = carve_zip("probe/ascuns.png")
    print(carve_zip("probe/ascuns.png"))

if poz != -1:
    with zipfile.ZipFile("gasit.zip") as z:
        print(z.namelist())
        for nume in z.namelist():
            print(nume, "->", z.read(nume).decode())

# FLAG{ascuns_prin_carving}