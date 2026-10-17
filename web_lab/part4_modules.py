# Laborator: funcții, metode și importuri pe web
# Student: Danuta Daniel
from part3_functions import fetch

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import socket
from urllib.parse import urlparse , urljoin
import requests
import time
import json
import ssl

# --Ex35--

url = "https://cybercor.org/path?x=1#top"
parts = urlparse(url)

# print(parts.scheme)
# print(parts.netloc)
# print(parts.path)
# print(parts.query)
# print(parts.fragment)

# Output:
# https
# cybercor.org
# /path
# x=1
# top


# --Ex36--

# from urllib.parse import urljoin
#
# for link in ["/about", "contact.html", "../index.html"]:
#     print(urljoin(BASE_URL, link))


# --Ex37--

import re

def extract_links(html):
    links = re.findall(r'href="([^"]+)"', html)
    unique = []
    for link in links:
        if link not in unique:
            unique.append(link)
    return unique

# response = fetch(BASE_URL)
# print(extract_links(response.text))

# Output: ['/assets/index-CErP0EKt.css']

# --Ex38--

def split_links(links: list, domain: str) -> tuple:
    """Întoarce (interne, externe): legăturile de pe același domeniu și cele către alte site-uri."""
    internal = []
    external = []
    for link in links:
        full = urljoin(BASE_URL, link)       # 1. legătura devine URL complet
        netloc = urlparse(full).netloc       # 2. extragem domeniul
        if netloc == domain:
            internal.append(full)
        else:
            external.append(full)
    return internal, external


# links = extract_links(fetch(BASE_URL).text)
# internal, external = split_links(links, "cybercor.org")
# print("Interne:", internal)
# print("Externe:", external)


# --Ex39--

from html.parser import HTMLParser


class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)

# test_html = """
# <html><body>
#   <img src="/logo.png" alt="Logo">
#   <IMG SRC="poza.jpg">
#   <img alt="imagine fără src">
#   <img src="https://justcats.ie/wp-content/uploads/2024/10/Untitled-design-1.webp" />
#   <a href="/despre">Aceasta nu este o imagine</a>
# </body></html>
# """
#
# finder = ImageFinder()
# finder.feed(test_html)
# print(finder.images)
#
# assert finder.images == [
#     "/logo.png",
#     "poza.jpg",
#     "https://justcats.ie/wp-content/uploads/2024/10/Untitled-design-1.webp",  # tag care se închide singur
# ], "Parserul nu a găsit exact imaginile așteptate"
# print("Testul a trecut!")
#
# response = requests.get(BASE_URL, timeout=TIMEOUT)
# finder = ImageFinder()
# finder.feed(response.text)
# print(len(finder.images), "imagini găsite")
# for src in finder.images:
#     print(src)
#
# print("Apariții de <img în HTML:", response.text.lower().count("<img"))


# --Ex40--

import hashlib

def page_fingerprint(url: str) -> str:
    response = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(response.content).hexdigest()


# first = page_fingerprint(BASE_URL)
# time.sleep(1)
# second = page_fingerprint(BASE_URL)
#
# print(first)
# print(second)
# print("Identice" if first == second else "Diferite")

# Amprenta depinde de continutul paginii , acelasi continut
# o sa rezulte on aceasi amprenta, dar orice modificare ar schimbao
# cybercor.org este o pagina statica astfel amprentele sunt indentice.
# Ca sa obtinem uo amprenta noua pagina trebuie sa fie modificata , ori
# trebuie noi sa modificam requestul spre pagina (alti parametrii de cerere)


# --Ex41--

response = requests.get(BASE_URL, timeout=TIMEOUT)

with open("headers.json", "w") as file:
    json.dump(dict(response.headers), file, indent=2)

with open("headers.json") as file:
    loaded = json.load(file)

# print(loaded.get("Content-Type", "lipsește"))

# Output: text/html; charset=utf-8


# --Ex42--

import socket

def resolve(hostname):
    return socket.gethostbyname(hostname)

# print(resolve("cybercor.org"))


# --Ex43--

def cert_days_left(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as tls:
            cert = tls.getpeercert()
    expires = ssl.cert_time_to_seconds(cert["notAfter"])
    return int((expires - time.time()) // 86400)


# print(cert_days_left("cybercor.org"))


#------------------------------