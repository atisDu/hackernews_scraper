from django.urls import path
from app.views import ReactView, ScrapeView, UpdateScoresView

urlpatterns = [
    path('', ReactView.as_view(), name="react-view"),
    path('scrape/', ScrapeView.as_view(), name="scrape-view"),
    path('update-scores/', UpdateScoresView.as_view(), name="update-scores-view"),
]