import requests
from checker import build_url, is_https, show_response, check_site, scan_sites, check_headers, retry_check, SITES

#PART1

print(build_url(SITES[0], "login"))
print(is_https(SITES[1]))

#PART2

print(show_response(SITES[2]))

#PART3

print(check_site(SITES[2]))

#PART4

print(scan_sites())

#PART5

print(check_headers(SITES[1]))

#PART6

print(retry_check(SITES[4]))