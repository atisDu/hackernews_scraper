import requests
from bs4 import BeautifulSoup
import os
import django

#django setups, lai varētu izmantot models.py db šeit
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from app.models import Post

page_nr = 1  #sākuma lapas numurs

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
        
        #salīdzina ar DB un atjaunina, ja maiņājies
        try:
            post = Post.objects.get(id=int(id_now))
            new_score = int(score_now.split()[0])
            
            if post.score != new_score:
                post.score = new_score
                post.save()
                print(f'Updated entry with ID {id_now} to new score {score_now}')
            else:
                print(f'No score change for ID {id_now}, skipping update.')
        except Post.DoesNotExist:
            print(f'Post with ID {id_now} not found in database.')

    

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
        #print(title + ' | ' + url + ' | ' + score + ' | ' + age + ' | ID: ' + id)
        
        #saglabājam db - get_or_create neatstāj duplicātus
        try: 
            post, created = Post.objects.get_or_create( #tgd izmanto get_or_create, kas ļauj atbrīvoties no lokālā mappinga, kā iepriekš
                id=int(id),
                defaults={
                    'title': title,
                    'score': int(score.split()[0]),  # noņem points daļu, atstāj tikai skaitli
                    'url': url,
                    'posted_at': age
                }
            )
            if created:
                print(f'Created new entry with ID {id}.')
            else:
                pass#print(f'Entry with ID {id} already exists in database.')
        except Exception as e:
            print(f'Error saving entry with ID {id}: {e}')
        

if __name__ == '__main__':
    
    while True:
        scrape(page_nr)
    #šis tiek izsaukts no frontenda, kad refresho punktus
        update_score(page_nr)
    
    #ķip kad frontendā refresho, tad abas tiek izsauktas
