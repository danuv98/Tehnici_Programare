# Laborator: funcții, metode și importuri pe web
# Student: Danuta Daniel

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import requests

# --Ex9--

# response = requests.get(BASE_URL, timeout=TIMEOUT)
#
# print(response.status_code)  # atribut
# print(response.ok)           # atribut
# print(response.url)          # atribut
# print(response.encoding)     # atribut
#
# 200
# True
# https://cybercor.org/
# utf-8


# --Ex10--

import requests

response = requests.get(BASE_URL, timeout=TIMEOUT)
# response.raise_for_status()
#
# try:
#     response = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
#     response.raise_for_status()
# except requests.HTTPError as e:
#     print("Aceasta pagina nu a fost gasita sau serverul a raspuns cu o eroare.")
#     print("Detalii:", e)


# --Ex11--

# for name, value in response.headers.items():
#     print(f"{name}: {value}")

# --Ex12--

# print(response.headers.get("Server", "lipsește"))
# print(response.headers.get("Content-Type", "lipsește"))
#
# print(response.headers.get("content-type", "lipsește"))

# Observam ca response.headers este un dictionar care nu este
# case sensitive si poate fi folosit cu atat litere mari cat si cu
# litere mici


# --Ex13--

# print(response.text.lower().count("cyber"))

# Putem inlantuii aceste comenzi deoarece fara .lower
# cuvantul cyber cu alte capitalizari nu ar fi contate la .count()

# --Ex14--

# html = response.text
#
# start = html.find("<title>") + len("<title>")
# end = html.find("</title>")
#
# title = html[start:end].strip()
# print(title)


# Output: CYBERCOR


# --Ex15--

# lines = response.text.splitlines()
#
# print("Nr de linii:", len(lines))
#
# longest = max(lines, key=len)
# print("Lungimea celei mai lungi linii:", len(longest))


# --Ex16--

# if response.url.startswith("https://"):
#     print("Conexiune securizată")
# else:
#     print("Conexiune nesecurizată")

# Output: Conexiune securizată


# --Ex17--

# response2 = requests.get("http://cybercor.org", timeout=TIMEOUT)
#
# for redirect in response2.history:
#     print(redirect.status_code, redirect.url)
#
# print("URL fin:", response2.url)

# Output: 301 http://cybercor.org/
# URL fin: https://cybercor.org/


# --Ex18--

# head_response = requests.head(BASE_URL, timeout=TIMEOUT)
# get_response = requests.get(BASE_URL, timeout=TIMEOUT)
#
# print("HEAD:", len(head_response.content))
# print("GET: ", len(get_response.content))

# HEAD cere doar informatia despre pagina , nu si pagina
# GET aduce si corpul astfel arata dimensiunea reala


# --Ex19--

# if response.cookies:
#     for cookie in response.cookies:
#         print(cookie.name, cookie.secure)
# else:
#     print("Niciun cookie setat")


# --Ex20--

# session = requests.Session()
# session.headers.update({"User-Agent": "WebLab-Daniel"})
#
# response = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
# print(response.json())
# print(response.text)

#--------------------------------