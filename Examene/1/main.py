import requests
from checker import build_url, is_https, show_response, check_site, scan_sites, check_headers, retry_check, SITES

#PART1

print("PART1:", build_url(SITES[0], "login"))
print("PART1:", is_https(SITES[1]))

#PART2

print("PART2:", show_response(SITES[2]))

#PART3

print("PART3:", check_site(SITES[2]))

#PART4

print("PART4:", scan_sites())

#PART5

print("PART5:", check_headers(SITES[1]))

#PART6

print("PART6:", retry_check(SITES[4]))