"""webtools: funcții reutilizabile pentru analiza paginilor web."""

import requests
import time
import json
import re
import socket
import ssl
import time
from typing import Optional
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

TIMEOUT = 5

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
]

DEFAULT_HEADERS = {"User-Agent": "WebLab-danu"}

def fetch(url: str, timeout: int = TIMEOUT) -> requests.Response:
    """Întoarce obiectul Response pentru url, trimițând DEFAULT_HEADERS."""
    return requests.get(url, timeout=timeout, headers=DEFAULT_HEADERS)


def get_status(url: str) -> int:
    """Întoarce codul de stare HTTP al paginii."""
    return fetch(url).status_code


#def get_title(html: str) -> str:
    """Întoarce titlul paginii dintr-un șir HTML."""
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    return html[start:end].strip()

def get_title(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    return soup.title.get_text(strip=True) if soup.title else ""


def security_headers(url: str) -> dict:
    """Întoarce {antet: True/False} pentru cele cinci antete de securitate."""
    response = fetch(url)
    return {name: name in response.headers for name in SECURITY_HEADERS}

#if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))
    print(__name__)

def check_paths(base: str, paths: list) -> dict:
    """Întoarce un dicționar {cale: cod_de_stare} pentru fiecare cale dată."""
    results = {}
    for path in paths:
        results[path] = get_status(base + path)
        time.sleep(1)
    return results

#def extract_links(html: str) -> list:
    """Întoarce legăturile (href) din HTML, fără duplicate."""
    links = re.findall(r'href="([^"]+)"', html)
    return list(dict.fromkeys(links))

def extract_links(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    links = [tag["href"] for tag in soup.find_all(href=True)]
    return list(dict.fromkeys(links))


def split_links(links: list, base: str) -> tuple:
    """Întoarce (interne, externe) față de domeniul lui base."""
    domain = urlparse(base).netloc
    internal, external = [], []
    for link in links:
        full = urljoin(base, link)
        if urlparse(full).netloc == domain:
            internal.append(full)
        else:
            external.append(full)
    return internal, external


def fetch_robots(base: str) -> Optional[str]:
    """Întoarce textul /robots.txt sau None dacă lipsește."""
    try:
        response = fetch(base + "/robots.txt")
    except requests.RequestException:
        return None
    if response.status_code != 200:
        return None
    return response.text


def disallowed_paths(robots_text: Optional[str]) -> list:
    """Întoarce valorile Disallow: din robots.txt."""
    if robots_text is None:
        return []
    paths = []
    for line in robots_text.splitlines():
        if line.strip().lower().startswith("disallow:"):
            value = line.split(":", 1)[1].strip()
            if value:
                paths.append(value)
    return paths


def score_headers(results: dict) -> str:
    """Întoarce scorul antetelor, de forma "3/5"."""
    return f"{sum(results.values())}/{len(results)}"


def resolve(hostname: str) -> str:
    """Întoarce adresa IPv4 a unui domeniu."""
    return socket.gethostbyname(hostname)


def cert_days_left(hostname: str) -> int:
    """Întoarce zilele rămase până la expirarea certificatului TLS."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as tls:
            cert = tls.getpeercert()
    expires = ssl.cert_time_to_seconds(cert["notAfter"])
    return int((expires - time.time()) // 86400)


def site_report(url: str) -> dict:
    """Colectează informații despre site, le afișează și le salvează în report.json."""
    hostname = urlparse(url).netloc
    response = fetch(url)
    html = response.text

    # Lanțul de redirecționări pornește de la http://, nu de la url-ul dat
    http_response = fetch("http://" + hostname)
    redirects = [f"{r.status_code} -> {r.headers.get('Location', '?')}"
                 for r in http_response.history]

    internal, external = split_links(extract_links(html), url)

    report = {
        "url": url,
        "status": response.status_code,
        "final_url": response.url,
        "title": get_title(html),
        "ip": resolve(hostname),
        "redirects": redirects,
        "security_score": score_headers(security_headers(url)),
        "cert_days_left": cert_days_left(hostname),
        "internal_links": len(internal),
        "external_links": len(external),
        "disallowed": disallowed_paths(fetch_robots(url)),
    }

    print(f"=== Raport site: {url} ===")
    print(f"Cod de stare:      {report['status']}")
    print(f"URL final:         {report['final_url']}")
    print(f"Titlu:             {report['title']}")
    print(f"Adresă IP:         {report['ip']}")
    print(f"Redirecționări:    {', '.join(redirects) if redirects else 'niciuna'}")
    print(f"Scor securitate:   {report['security_score']}")
    print(f"Certificat:        {report['cert_days_left']} de zile rămase")
    print(f"Legături:          {report['internal_links']} interne, {report['external_links']} externe")
    print(f"Căi interzise:     {', '.join(report['disallowed']) if report['disallowed'] else 'niciuna'}")

    with open("report.json", "w") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)
    print("Salvat în report.json")
    return report