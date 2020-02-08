import sys
import requests
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
    if nope != []:
        return
    else:
        print(h3)
        print(span[1:])
        print(href)

def main():
    title = sys.argv[1]
    search = title.replace(" ", "+")
    url = 'https://www.ebay.com/sch/176985/i.html?_from=R40&_nkw={}&LH_TitleDesc=0&_sop=15'.format(search)
    get_detail_data(get_page(url))

if __name__ == '__main__': 
    main() 
