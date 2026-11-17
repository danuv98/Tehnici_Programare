
import argparse
import json

from arsenal.aparare.parse_auth import citeste_esecuri, pe_ip


# B1


def suspecti(counts, prag=10):
    if prag < 1:
        raise ValueError(
            f"prag invalid: {prag} (cel putin 1)"
        )

    return [
        (ip, n)
        for ip, n in counts.most_common()
        if n >= prag
    ]


# B3


def main():
    p = argparse.ArgumentParser()

    p.add_argument("log")
    p.add_argument("--prag", type=int, default=10)
    p.add_argument("--json", action="store_true")

    a = p.parse_args()

    try:
        esecuri = citeste_esecuri(a.log)
        counts = pe_ip(esecuri)
        sus = suspecti(counts, a.prag)

    except ValueError as e:
        p.error(str(e))

    if a.json:
        raport = {
            "esecuri": len(esecuri),
            "pe_ip": dict(counts),
            "suspecti": [
                {"ip": ip, "incercari": n}
                for ip, n in sus
            ]
        }

        print(json.dumps(raport, indent=4))

    else:
        print("Esecuri de autentificare:", len(esecuri))

        for ip, n in counts.most_common():
            print(f" {ip}: {n}")

        print(f"Suspecti (prag {a.prag}):")

        for ip, n in sus:
            print(f" {ip} ({n} incercari) BRUTE FORCE")


if __name__ == "__main__":
    main()
