# Hacker News Scraper
A simple, fully-dockerized scraper for Hacker News with a **Django backend** and a **React + Vite frontend** using **DataTables** to display scraped posts.
---

The Django backend runs on the scraper.py service script, which handles the scraping logic with two main functions:

- `scrape()` — Scrapes titles, links, points, and timestamps from Hacker News.  
- `update_score()` — Refreshes the points of already-saved posts.

The frontend displays a slider for selecting the Hacker News pages to scrape and shows the results in a dynamic DataTables table with pagination, sorting, and full-text search

## Deployment via Docker

### Requirements
```docker docker-compose```

### Installation
1. Clone the repo
```git clone https://github.com/atisDu/hackernews_scraper.git```

3. Enter into the project directory
```cd /path/to/hackernews_scraper```

4. Run docker-compose
```docker-compose up -d```

### Access the site
Frontend is available at
http://localhost:5173/

## Project structure
```
hackernews_scraper/
│
├── back/
│   ├── core/                        # Django project (settings, URLs, main serializer)
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── serializer.py            # Main data serializer for API <-> frontend
│   │   └── ...
│   │
│   ├── app/                         # Main Django app
│   │   ├── models.py                # Post model
│   │   ├── views.py                 # API endpoints
│   │   ├── management/
│   │   │   └── commands/
│   │   │       ├── scrape.py        # Management command wrapper for scraper
│   │   │       └── update_score.py
│   │   ├── services/
│   │   │   └── scraper.py           # **Main scraping logic**
│   │   └── ...
│   │
│   └── requirements.txt
│
├── front/                        # React + Vite UI
│   ├── src/
│   │   ├── components/
│   │   └── ...
│   ├── index.html
|   └── ...
│
├── docker-compose.yml
└── README.md
```
