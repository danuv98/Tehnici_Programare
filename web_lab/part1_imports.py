# Laborator: funcții, metode și importuri pe web
# Student: Danuta Daniel

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde


# --Ex1--

import requests
#print(requests.__version__)

import urllib.request

# libraria "request" este una third party
# pe cand libraria urllib este una ce vine deja inclusa
# in interpretatorul python si este o librarie standard

# Output: 2.32.5


# --Ex2--

#print(requests.get(BASE_URL))

#<Response [200]>

#from requests import get
#response = get(BASE_URL)
#print(response)

#<Response [200]>

# Stilul unu este usor de inteles deoarece se vede imediat de unde
# vine functia "requests.get" si nu poate fi confundat

# Stilul doi are avantajul ca apelam direct la get
# fara prefixul request , folositor cand folosim functia
# de mai multe ori


# --Ex3--

#import requests as rq
#print(rq.get(BASE_URL))

# Un alias face codul mai usor de citit cand numele librariei
# este unul lung sau cand evita confuzia intre mai multe functii

# Un alias face codul mai greu cand acelasi alias inseamna alte
# lucruri sau cand numele original este deja scurt si aliasul nu ajuta


# --Ex4--

#with urllib.request.urlopen(ECHO_URL) as response:
    #print(response.status)
    #body = response.read(200).decode('utf-8')
    #print(body)

# Output: 200
# <!DOCTYPE html>
# <html lang="en">
#
# <head>
#     <meta charset="UTF-8">
#     <title>httpbin.org</title>
#     <link href="https://fonts.googleapis.com/css?family=Open+Sans:400,700|Source+Code+Pro:300,600|Tit


# --Ex5--

#print(dir(requests))

# Class: Session, folosita ca requests.Session(),
# pastreaza cookieurile si setarile dintro sesiune

# Function: get, se apeleaza cu requests.get()

# Module: adapters, un fisier .py din pachetul requests care
# contine clase si functii


# --Ex6--

#help(requests.get)
#requests.get(BASE_URL, timeout=5)
# Parametrul care seteaza timpul maxim de asteptare
# este timeout care este folosit in modelul de mai sus .get(url, param)


# --Ex7--

# import time
# start = time.perf_counter()
# response = requests.get(BASE_URL, timeout=TIMEOUT)
# end = time.perf_counter()
#
# print(end - start)
# print(response.elapsed.total_seconds())


#0.830484208 - time.perf_counter()
#0.810986 - elapsed.total_seconds()


# --Ex8--

# try:
#     import bs4
#
# except ImportError:
#     print("Instalați modulul cu: pip install beautifulsoup4")


# -----------

