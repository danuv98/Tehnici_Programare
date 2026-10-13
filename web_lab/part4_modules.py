# Laborator: funcții, metode și importuri pe web
# Student: Danuta Daniel

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# --Ex35--

from urllib.parse import urlparse

url = "https://cybercor.org/path?x=1#top"
parts = urlparse(url)

print(parts.scheme)
print(parts.netloc)
print(parts.path)
print(parts.query)
print(parts.fragment)

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

