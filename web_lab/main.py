import webtools
import argparse
import csv
from datetime import datetime
from webtools import get_title, security_headers, DEFAULT_HEADERS
from webtools import fetch
from webtools import check_paths
from bs4 import BeautifulSoup

BASE_URL = "https://cybercor.org"

# --Ex44--

# print(webtools.get_title(webtools.fetch(BASE_URL).text))


# --Ex45--

# Daca main.py ar avea o functie proprie get_title, functiile sar
# ciocni, python tine un singur get_title in fisier, cel care este definit
# ultimul. Astfel daca def get_title apare dupa import el ar fi cel folosit
# si vice versa. Folosinf import webtools si webtools.get_title, problema nu apare


# --Ex46--

# Testerul ruleaza doar in webtools deoarece if-ul veririfica daca
# programul in care este rulat este programul principal.
# Acesta nu ruleaza in main.py deoarece este un import si nu indeplineste conditia.


# --Ex47--

# print(DEFAULT_HEADERS)
# print(get_title(fetch(BASE_URL).text))


# --Ex48--

parser = argparse.ArgumentParser(description="Analizează o pagină web.")
parser.add_argument("url", help="adresa paginii, de exemplu https://cybercor.org")
args = parser.parse_args()

url = args.url

# print(get_title(fetch(url).text))
# print(security_headers(url))


# Output:

# danu1@Danus-MacBook-Air web_lab % python main.py https://cybercor.org
# CYBERCOR
# {'Strict-Transport-Security': False, 'Content-Security-Policy': False, 'X-Frame-Options': True, 'X-Content-Type-Options': True, 'Referrer-Policy': True}


# --Ex49--

# parser = argparse.ArgumentParser(description="Verifică căi de pe un site.")
# parser.add_argument("url", help="adresa site-ului, de exemplu https://cybercor.org")
# args = parser.parse_args()
#
# statuses = check_paths(args.url, ["/", "/robots.txt", "/sitemap.xml"])
#
# with open("report.csv", "w", newline="") as file:
#     writer = csv.writer(file)
#     writer.writerow(["path", "status", "checked_at"])
#     for path, status in statuses.items():
#         writer.writerow([path, status, datetime.now().isoformat()])
#
# print("Raport salvat în report.csv")


# --Ex50--

from webtools import site_report

parser = argparse.ArgumentParser(description="Raport despre un site web.")
parser.add_argument("url")
args = parser.parse_args()

site_report(args.url)


# --BONUS--

def get_title(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    return soup.title.get_text(strip=True) if soup.title else ""

def extract_links(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    links = [tag["href"] for tag in soup.find_all(href=True)]
    return list(dict.fromkeys(links))



#-------------------------------