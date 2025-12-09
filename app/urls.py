from django.urls import path
from app.views import ReactView

urlpatterns = [
    path('', ReactView.as_view(), name="react-view"),
]