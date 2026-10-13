# Laborator: funcții, metode și importuri pe web
# Student: Danuta Daniel
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde
import requests
import time
# --Ex21--

# def fetch(url):
#     return requests.get(url, timeout=TIMEOUT)
#
# response = fetch(BASE_URL)
# print(response.status_code)


# --Ex22--

def get_status(url: str) -> int:
    return requests.get(url, timeout=TIMEOUT).status_code
#
# for path in ["/", "/robots.txt", "/sitemap.xml"]:
#     print(path, get_status(BASE_URL + path))
#     time.sleep(1)

# Output: / 200
# /robots.txt 200
# /sitemap.xml 200


# --Ex23--

def fetch(url, timeout=10) -> requests.Response:
    return requests.get(url, timeout=timeout)


# response1 = fetch(BASE_URL)
# print(response1.status_code)
#
# response2 = fetch(BASE_URL, timeout=3)
# print(response2.status_code)


# --Ex24--

# def get_title(html):
#     start = html.find("<title>") + len("<title>")
#     end = html.find("</title>")
#     return html[start:end].strip
#
#
# response = fetch(BASE_URL)
# print(get_title(response.text))


# --Ex25--

def get_title(html:str) -> str:
    """Extrage titlul paginii dintr-un sir html
    Primeste codul html ca sir de caractere si extrage
    doar textul intre <title> si </title> , iar .striped
    elimina spatiile in cazul in care sunt prezente.
    """
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    return html[start:end].strip

# help(get_title)


# --Ex26--

# print(get_status(123))

# Adnotarile nu ne opresc , adnotarile sunt dor indice
# python nu le verifica la rulare


# --Ex27--

def page_exists(url: str) -> bool:
    try:
        return get_status(url) == 200
    except requests.RequestException:
        return False

# print(page_exists(BASE_URL))
# print(page_exists("https://this-domain-does-not-exist.invalid"))

# Output: True
# False


# --Ex28--

def check_paths(base, paths):
    results = {}
    for path in paths:
        results[path] = get_status(base + path)
        time.sleep(1)
    return results


# statuses = check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"])
# print(statuses)


# --Ex29--

def get_header(url, name, default = "lipsește"):
    response = requests.get(url, timeout=TIMEOUT)
    return response.headers.get(name, default)


# print(get_header(BASE_URL, name="Server"))


# --Ex30--

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
]


def security_headers(url: str) -> dict:
    response = requests.get(url, timeout=TIMEOUT)
    return {name: name in response.headers for name in SECURITY_HEADERS}

#result = security_headers(BASE_URL)
# print(result)


# --Ex31--

def score_headers(results: dict) -> str:
    present = sum(results.values())
    total = len(results)
    return f"{present}/{total}"

# print(score_headers(security_headers(BASE_URL)))

# Output = 3/5


# --Ex32--

def fetch_robots(base):
    response = requests.get(base + "/robots.txt", timeout=TIMEOUT)
    if response.status_code != 200:
        return None
    return response.text

def disallowed_paths(robots_text):
    if robots_text is None:
        return []
    paths = []
    for line in robots_text.splitlines():
        if line.startswith("Disallow:"):
            paths.append(line.split(":")[1].strip())
    return paths

# robots = fetch_robots(BASE_URL)
# print(disallowed_paths(robots))
# print(robots)


# --Ex33--

def response_times(*urls):
    times = {}
    for url in urls:
        response = requests.get(url, timeout=TIMEOUT)
        times[url] = response.elapsed.total_seconds()
    return times

# print(response_times(BASE_URL, ECHO_URL))

# Output: {'https://cybercor.org': 0.287727, 'https://httpbin.org': 0.534556}


# --Ex34--

def log(message, **details):
    parts = [message]
    for key, value in details.items():
        parts.append(f"{key}={value}")
    print(" | ".join(parts))

# log("verificat", url=BASE_URL, status=200)

# print() arata valoarea pe ecran pentru utilizator , dupa afisare
# valoarea nu ajunge la codul care a apelat functia

# return trimite valoarea inapoi catre codul care a apelat functia
# astfel poate fi salvata intro variabila , folosita de alte functii






