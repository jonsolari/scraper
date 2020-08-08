import sys
import requests
import json
from bs4 import BeautifulSoup


def get_page(url):
    r = requests.get(url)

    if not r.ok:
        print("Server responded with: ", r.status_code)
    else:
        soup = BeautifulSoup(r.text, 'lxml')
    return soup

def get_detail_data(soup):
    nope = soup.findAll(text='No exact matches found')
    
    h3 = soup.find('h3', class_="s-item__title").text
    span = soup.find('span', class_="s-item__price").text
    href = soup.find('a', class_="s-item__link", href=True).get('href')

    total = { 'price': 0, 'url' : '' }

    if nope != []:
        return None
    else:
        total['price'] = span[1:]
        total['url'] = href
        return total


# TODO loop over list of releases to search for, update JSON / remove things no longer available 

# make sure account for plain black pressings of BPT and MCB
releaselist = ["mountain goats zopilote machine lp", "mountain goats sweden lp", "mountain goats nothing for juice lp", "mountain goats full force galesburg lp", "mountain goats coroner's gambit lp", "mountain goats new asian cinema", "mountain goats isopanisad radio hour", "mountain goats devil in the shortwave", "mountain goats black pear tree", "mountain goats satanic messiah", "mountain goats moon colony bloodbath", "mountain goats taboo cassette", "mountain goats come come to the sunset tree", "mountain goats on juhu beach", "mountain goats life of the world to come dvd", "mountain goats songs for pierre chuvin", "mountain goats jam eater blues", "mountain goats all survivors pack", "mountain goats steal smoked fish"]

discogsurls = ['https://api.discogs.com/releases/1601354', 'https://api.discogs.com/releases/1191772', 'https://api.discogs.com/releases/744810', 'https://api.discogs.com/releases/523351', 'https://api.discogs.com/releases/1217804', 'https://api.discogs.com/releases/1625208', 'https://api.discogs.com/releases/1625203', 'https://api.discogs.com/releases/1210894', 'special', 'https://api.discogs.com/releases/1516102','special', 'https://api.discogs.com/releases/2767923', 'https://api.discogs.com/releases/769960', 'https://api.discogs.com/releases/2873969', 'https://api.discogs.com/releases/2732093', 'special', 'https://api.discogs.com/releases/2306617', 'https://api.discogs.com/releases/2797105', 'https://api.discogs.com/releases/3916742']

ebaydata = {}
discogsdata= {}


def ebayget(release):
    search = release.replace(" ", "+")
    url = 'https://www.ebay.com/sch/176985/i.html?_from=R40&_nkw={}&LH_TitleDesc=0&_sop=15'.format(search)
    return get_detail_data(get_page(url))

def discogsget(release):
    if release == 'special':
        total = { 'price' : '', 'url' : ''}    
    else:
        total = { 'price' : '', 'url' : ''}
        r = requests.get(release).json()
        price1 = r['lowest_price']
        total['price'] = price1
        total['url'] = 'http://www.discogs.com/sell/release/' + str(r['id'])
        return total

high = 1000000

def dcompare(master):
    total = { 'price' : high, 'url' : ''}
    i = 0
    while i < len(master):
        temp = discogsget(master[i])
        if temp['price'] is not None and float(temp['price']) < float(total['price']):
            total['price'] = temp['price']
            total['url'] = temp['url']
        else:
            total['url'] = temp['url']
        i += 1
    if total['price'] == high:
        total['price'] = None
    return total

i = 0
while i < len(releaselist):
    ebaydata[i] = ebayget(releaselist[i])
    print(ebaydata[i])
    i += 1

j = 0
while j < len(discogsurls):
    discogsdata[j] = discogsget(discogsurls[j])
    j += 1

discogsdata[8] = dcompare(['https://api.discogs.com/releases/1526609', 'https://api.discogs.com/releases/4880289'])

discogsdata[10] = dcompare(['https://api.discogs.com/releases/1763341', 'https://api.discogs.com/releases/5118937'])

discogsdata[15] = dcompare(['https://api.discogs.com/releases/15516873', 'https://api.discogs.com/releases/15517693', 'https://api.discogs.com/releases/15517068', 'https://api.discogs.com/releases/15506961'])

k = 0
while k < len(ebaydata):
    if ebaydata[k] is not None and discogsdata[k]['price'] is not None:
        if float(ebaydata[k]['price']) > discogsdata[k]['price']:
            ebaydata[k] = discogsdata[k]
    elif ebaydata[k] is None:
        ebaydata[k] = discogsdata[k]
    else:
        pass
    k += 1

json_object = json.dumps(ebaydata, indent = 4)

with open('data.json', 'w') as outfile:
    outfile.seek(0)
    outfile.write(json_object)