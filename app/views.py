from django.shortcuts import render, redirect
from django.urls import reverse
from .services import scraper
from .models import Post


def index(request):
    # Lapu nr maiņa un nodošana scriptam 
    page = request.GET.get("page", 1)
    scraper.page_nr = int(page)
    
    # Pogu triggeri
    action = request.GET.get("action")
    if action == "scrape":
        scraper.scrape(scraper.page_nr)
        return redirect(f"{reverse('index')}?page={scraper.page_nr}")
    elif action == "update":
        scraper.update_score(scraper.page_nr)
        return redirect(f"{reverse('index')}?page={scraper.page_nr}")

    #Pirmie 30 ieraksti no DB, tkā hacker news dod 30 ierakstus lapā, ar pagination
    page_size = 10
    start = (scraper.page_nr - 1) * page_size
    end = start + page_size
    posts = Post.objects.all().order_by('-posted_at')[start:end]    

    context = {
        "posts": posts, #konteksts tiek nodots uz templatu, lai varētu attēlot datus, vienkārši nodod mainīgo 
        "current_page": scraper.page_nr,
    }
    return render(request, "index.html", context)      