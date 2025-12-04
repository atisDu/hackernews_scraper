import requests
from bs4 import BeautifulSoup


def scrape():
    nr = 1 #lapas numurs, frontendā varēs mainīt
    url = f'https://news.ycombinator.com/?p={nr}' #/?p= lapas numurs, frontendā noderēs
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    #Tituliem un linkiem
    for title_span in soup.select('.titleline > a'):
       title = title_span.get_text(strip=True) if title_span else 'No title'
       url = title_span['href']
       print(title)
       print(url)

    #Punktiem un vecumam
    for subtitles in soup.select('.subline'):
        #punkti
        score_span = subtitles.select_one('[class^="score"]')
        score = score_span.get_text(strip=True) if score_span else '0 points'
        print(score)
        #  vecums
        age_span = subtitles.select_one('.age')
        # iekšā .get_text ir formāts "3 hours ago", savukārt title klasē ir timestamps ar kkādu id,
        # tāpēc ņemam tikai pirmos 19 simbolus. 
        age = age_span.get('title')[:19] if age_span else 'unknown age'
        print(age)



if __name__ == '__main__':
    scrape()
