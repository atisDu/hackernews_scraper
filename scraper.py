import requests
from bs4 import BeautifulSoup


def scrape():
    nr = 1 #lapas numurs, frontendā varēs mainīt
    url = f'https://news.ycombinator.com/?p={nr}' #/?p= lapas numurs, frontendā noderēs
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    #Vienas cilpas risinājums
    for row in soup.select('tr.athing'):
        #Tituls un linki
        title_span = row.select_one('.titleline > a')
        title = title_span.get_text(strip=True) if title_span else 'No title'
        url = title_span['href']

        #subline klase ir nākamjā tr (rindā) tabulā
        subline_tr = row.find_next_sibling('tr')
        
        #punkti 
        score_span = subline_tr.select_one('[class^="score"]')
        score = score_span.get_text(strip=True) if score_span else '0 points'
        #  vecums
        age_span = subline_tr.select_one('.age')
        # iekšā .get_text ir formāts "3 hours ago", savukārt title klasē ir timestamps ar kkādu id,
        # tāpēc ņemam tikai pirmos 19 simbolus. 
        age = age_span.get('title')[:19] if age_span else 'unknown age'
        
        #visu izprintējam
        print(title + ' | ' + url + ' | ' + score + ' | ' + age)
        
if __name__ == '__main__':
    scrape()
