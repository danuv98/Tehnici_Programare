from os.path import join

import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    path = path.lstrip("/")
    return "https://" + host + "/" + path
    pass

def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    if url.startswith("https://"):
          return True
    else:
         return False
    pass


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    r = requests.get(url)
    print(f"Status: {r.status_code}")
    print(f"Content-Type: {r.headers.get('Content-Type')}")
    return
    pass


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    r = requests.get(url)
    return {
        "status": r.status_code,
        "content_type": r.headers.get('Content-Type'),
        "length" : len(r.content),
        "server" : r.headers.get('Server'),
    }
    pass


def scan_sites():
    verified_sites = []
    for site in SITES:
        try:
            r = requests.get(site, timeout=5)
            if r.status_code == 200:
                verified_sites.append(site)
        except requests.RequestException:
            continue
    print("Siteuri care merg:")
    for site in verified_sites:
        print(f" - {site}")
    print(f"Summary: {len(verified_sites)} din {len(SITES)} merg")
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    pass



def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    r = requests.get(url)
    return {
        "prezente": [header for header in SECURITY_HEADERS if header in r.headers],
        "lipsa": [header for header in SECURITY_HEADERS if header not in r.headers],
        "score": len([header for header in SECURITY_HEADERS if header in r.headers]) / len(SECURITY_HEADERS) * 100
    }
    pass



def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    retry_check = 0
    while retry_check < attempts:
        try:
            r = requests.get(url, timeout=5)
            return {
                "status": r.status_code,
                "attempts": retry_check + 1
            }
        except requests.RequestException:
            retry_check += 1
    return {
        "status": None,
        "attempts": 0
    }

