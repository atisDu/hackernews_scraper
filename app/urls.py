from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import PostViewSet, ReactView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('', ReactView.as_view(), name='react-view'),  # GET / returns all posts
    path('', include(router.urls)),  # /posts/ endpoints with scrape/ and update_scores/
]