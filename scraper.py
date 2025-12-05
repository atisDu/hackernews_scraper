import requests
from bs4 import BeautifulSoup


id_n_score_map = {}

def update_score(page_nr):
    # temp mappings, lai salīdzinātu vecā requesta un jaunā requesta punktus pie attiecīgā ID
    temp_map = {}
    #vēlreiz aizsūta get request uz to pašu lapu
    url = f'https://news.ycombinator.com/?p={page_nr}' #/?p= lapas numurs, frontendā noderēs
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for row in soup.select('tr.athing'):
        #id tagad
        id_now = row['id']

        #punkti tagad (atkal iterējas caur visām tabulas rindām)
        score_span = row.find_next_sibling('tr').select_one('[class^="score"]')
        score_now = score_span.get_text(strip=True) if score_span else '0 points'
        #pievieno temp mapam
        temp_map[id_now] = score_now

    #salīdzina vecos un jaunus punktus pēc ID (1-ja ir temp mapē, tad tas ir jau eksistējoš un ir jāatjaunina),
    #2 - paņem un overwrite vecos punktus ar jaunajiem pie tā paša ID
    #iterē to visiem id, kas ir vecajā mapē
    for id_before in list(id_n_score_map.keys()):    
        if id_before in temp_map: # ja vecais id ir jaunajā mapē
            # vēlviens checks, lai nebūtu lieki db writes
            if id_n_score_map[id_before] == temp_map[id_before]:
                #print(f'No score change for ID {id_before}, skipping update.')
                continue
            else:
                id_n_score_map[id_before] = temp_map[id_before] 
                print(f'Updated entry with ID {id_before} to new score {temp_map[id_before]}')
        else:
            #jauns ieraksts - ignorējam, lai main scrape funkcija to apstrādā
            print(f'New entry found with ID {id_now} and score {score_now}')

    

def scrape(page_nr):
     #lapas numurs, frontendā varēs mainīt
    url = f'https://news.ycombinator.com/?p={page_nr}' #/?p= lapas numurs, frontendā noderēs
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    #Vienas cilpas risinājums
    for row in soup.select('tr.athing'):
        #id
        id = row['id']
        
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
        print(title + ' | ' + url + ' | ' + score + ' | ' + age + ' | ID: ' + id)
        
        #lai izvairītos no liekiem db writes, pārbaudām vai jau neeksistē
        if id in id_n_score_map:
            #print(f'Entry with ID {id} already exists. Skipping database write.')
            pass
        else:
            #saglabājam id un score mapingā
            id_n_score_map[id] = score
        
if __name__ == '__main__':
    page_nr = 1
    while True:
        scrape(page_nr)
    #šis tiek izsaukts no frontenda, kad refresho punktus
        update_score(page_nr)
    
    #ķip kad frontendā refresho, tad abas tiek izsauktas
